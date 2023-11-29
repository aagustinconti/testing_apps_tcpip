from datetime import datetime
from ..db.mongodb import AsyncIOMotorClient
from bson.objectid import ObjectId

from ..core.config import database_name, images_collection_name
from ..models.image import ImageInCreate, ImageInDB


async def get_image(conn: AsyncIOMotorClient, id: str):
    row = await conn[database_name][images_collection_name].find_one({'_id': id})
    if row:
        return ImageInDB(**row)


async def create_image(conn: AsyncIOMotorClient, new_image: ImageInCreate):

    new_image_db = ImageInDB(**new_image.model_dump())

    result = await conn[database_name][images_collection_name].insert_one(new_image_db.model_dump())
    return result.inserted_id


async def remove_image(conn: AsyncIOMotorClient, id: str):
    await conn[database_name][images_collection_name].delete_one({'_id': id})
