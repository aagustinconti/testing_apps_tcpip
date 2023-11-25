from ..db.mongodb import AsyncIOMotorClient
from bson.objectid import ObjectId

from ..core.config import database_name, products_collection_name
from ..models.product import ProductInCreate, ProductInDB, ProductInUpdate


async def get_product(conn: AsyncIOMotorClient, code: str):
    row = await conn[database_name][products_collection_name].find_one({"product_code": code})
    if row:
        return ProductInDB(**row)


async def get_products(conn: AsyncIOMotorClient, code_like: str) -> list[ProductInDB]:
    cursor = conn[database_name][products_collection_name].find(
        {"product_code": {"$regex": str(code_like), "$options": "i"}})
    products = await cursor.to_list(length=None)
    return [ProductInDB(**product) for product in products]


async def get_product_by_name(conn: AsyncIOMotorClient, name_like: str):
    row = await conn[database_name][products_collection_name].find_one({"name": {"$regex": name_like, "$options": "i"}})
    if row:
        return ProductInDB(**row)


async def get_products_by_name(conn: AsyncIOMotorClient, name_like: str) -> list[ProductInDB]:
    cursor = conn[database_name][products_collection_name].find(
        {"name": {"$regex": str(name_like), "$options": "i"}})
    products = await cursor.to_list(length=None)
    return [ProductInDB(**product) for product in products]


async def create_product(conn: AsyncIOMotorClient, product: ProductInCreate) -> ProductInDB:
    dbproduct = ProductInDB(**product.model_dump())

    result = await conn[database_name][products_collection_name].insert_one(dbproduct.model_dump())
    inserted_id = result.inserted_id

    dbproduct.created_at = ObjectId(inserted_id).generation_time
    dbproduct.updated_at = ObjectId(inserted_id).generation_time

    return dbproduct


async def update_product(conn: AsyncIOMotorClient, code: str, product: ProductInUpdate):
    dbproduct = await get_product(conn, code)

    dbproduct.name = product.name or dbproduct.name
    dbproduct.price = product.price or dbproduct.price
    dbproduct.amount = product.amount or dbproduct.amount
    dbproduct.description = product.description or dbproduct.description
    dbproduct.image = product.image or dbproduct.image

    updated_at = await conn[database_name][products_collection_name]\
        .update_one({"product_code": code}, {'$set': dbproduct.model_dump()})
    dbproduct.updated_at = updated_at
    return dbproduct


async def remove_product(conn: AsyncIOMotorClient, code: str):
    await conn[database_name][products_collection_name].delete_one({"product_code": code})
