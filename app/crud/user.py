from ..db.mongodb import AsyncIOMotorClient
from pydantic import EmailStr
from bson.objectid import ObjectId

from ..core.config import database_name, users_collection_name
from ..models.user import UserInCreate, UserInDB, UserInDBId, UserInUpdate


async def get_user(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"username": username})
    if row:
        return UserInDBId(**row, id=str(row['_id']))


async def get_user_by_email(conn: AsyncIOMotorClient, email: EmailStr) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"email": email})
    if row:
        return UserInDBId(**row, id=str(row['_id']))


async def create_user(conn: AsyncIOMotorClient, user: UserInCreate) -> UserInDB:
    dbuser = UserInDB(**user.model_dump())
    dbuser.change_password(user.password)

    result = await conn[database_name][users_collection_name].insert_one(dbuser.model_dump())
    inserted_id = result.inserted_id

    dbuser.created_at = ObjectId(inserted_id).generation_time
    dbuser.updated_at = ObjectId(inserted_id).generation_time

    return UserInDBId(**dbuser.model_dump(), id=str(inserted_id))


async def update_user(conn: AsyncIOMotorClient, username: str, user: UserInUpdate) -> UserInDB:
    dbuser = await get_user(conn, username)

    dbuser.username = user.username or dbuser.username
    dbuser.email = user.email or dbuser.email

    if user.password:
        dbuser.change_password(user.password)

    updated_at = await conn[database_name][users_collection_name]\
        .update_one({"username": dbuser.username}, {'$set': dbuser.model_dump()})
    dbuser.updated_at = updated_at

    return UserInDBId(**dbuser.model_dump(), id=str(dbuser["_id"]))
