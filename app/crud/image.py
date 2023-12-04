from datetime import datetime
import logging
from ..db.mongodb import AsyncIOMotorClient
from bson.objectid import ObjectId

from ..core.config import database_name, images_collection_name
from ..models.image import ImageBase, ImageInCreate, ImageInDB


async def get_image(conn: AsyncIOMotorClient, id: str):
    row = await conn[database_name][images_collection_name].find_one({'_id': ObjectId(id)})
    if row:
        row['id'] = str(row['_id'])
        return ImageInDB(**row)


async def get_images_by_owner(conn: AsyncIOMotorClient, owner_id: str):
    cursor = conn[database_name][images_collection_name].find(
        {"owner_id": owner_id})
    images = await cursor.to_list(length=None)
    return [ImageInDB(**image, id=str(image['_id'])) for image in images]


async def create_image(conn: AsyncIOMotorClient, new_image: ImageInCreate, owner_id: str):

    new_image_db = ImageBase(
        image_base64=new_image.image_base64, owner_id=owner_id)

    result = await conn[database_name][images_collection_name].insert_one(new_image_db.model_dump())
    return str(result.inserted_id)


async def remove_image(conn: AsyncIOMotorClient, id: str):
    await conn[database_name][images_collection_name].delete_one({'_id': id})
