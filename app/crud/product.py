from ..db.mongodb import AsyncIOMotorClient
from bson.objectid import ObjectId

from ..core.config import database_name, products_collection_name
from ..models.product import ProductInCreate, ProductInDB, ProductInUpdate

async def get_product(conn: AsyncIOMotorClient, id: str):
    row = await conn[database_name][products_collection_name].find_one({"_id": id})
    if row:
        return ProductInDB(**row)

async def get_product_by_name(conn: AsyncIOMotorClient, name_like: str):
    row = await conn[database_name][products_collection_name].find_one({"name": {"$regex": name_like, "$options": "i"} })
    if row:
        return ProductInDB(**row)

async def get_products_by_name(conn: AsyncIOMotorClient, name_like: str):
    row = await conn[database_name][products_collection_name].find({"name": {"$regex": name_like, "$options": "i"} })
    if row:
        products = []
        for product in row:
            products.append(ProductInDB(**product))

        return products


async def create_product(conn: AsyncIOMotorClient, product: ProductInCreate) -> ProductInDB:
    dbproduct = ProductInDB(**product.model_dump())

    await conn[database_name][products_collection_name].insert_one(dbproduct.model_dump())

    dbproduct.created_at = ObjectId(dbproduct._id).generation_time
    dbproduct.updated_at = ObjectId(dbproduct._id).generation_time

    return dbproduct


async def update_product(conn: AsyncIOMotorClient, id: str, product: ProductInUpdate):
    dbproduct = await get_product(conn, id)

    dbproduct.name = product.name or dbproduct.name
    dbproduct.price = product.price or dbproduct.price
    dbproduct.amount = product.amount or dbproduct.amount
    dbproduct.description = product.description or dbproduct.description
    dbproduct.image = product.image or dbproduct.image

    updated_at = await conn[database_name][products_collection_name]\
        .update_one({"_id": id}, {'$set': dbproduct.model_dump()})
    dbproduct.updated_at = updated_at
    return dbproduct


async def remove_product(conn: AsyncIOMotorClient, id: str):
    await conn[database_name][products_collection_name].delete_one({"_id": id})
