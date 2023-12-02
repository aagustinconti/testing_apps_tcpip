from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.crud.shortcuts import check_free_username_and_email

from ....core.config import ACCESS_TOKEN_EXPIRE_MINUTES, AUTH_ENDPOINT
from ....core.jwt import create_access_token
from ....crud.user import create_user, get_user_by_email
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.user import User, UserInCreate, UserInResponse
from ....models.token import Token

router = APIRouter()


@router.post(AUTH_ENDPOINT, response_model=Token, tags=["auth"])
async def login(
        user: OAuth2PasswordRequestForm = Depends(), db: AsyncIOMotorClient = Depends(get_database)
):
    dbuser = await get_user_by_email(db, user.username)
    if not dbuser or not dbuser.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )

    token = create_access_token(data={"username": dbuser.username})

    return Token(access_token=token, token_type='bearer')


@router.post(
    "/auth/register",
    response_model=UserInResponse,
    tags=["auth"],
    status_code=HTTP_201_CREATED,
)
async def register(
        user: UserInCreate = Body(..., embed=True), db: AsyncIOMotorClient = Depends(get_database)
):
    await check_free_username_and_email(db, user.username, user.email)

    async with await db.start_session() as s:
        async with s.start_transaction():
            dbuser = await create_user(db, user)
            token = create_access_token(data={"username": dbuser.username})

            return UserInResponse(user=User(**dbuser.model_dump(), id=dbuser._id, token=token))
