from datetime import timedelta

from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.crud.shortcuts import check_free_username_and_email

from ....core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from ....core.jwt import create_access_token, get_current_user_authorizer
from ....crud.user import create_user, get_user_by_email
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.user import User, UserInCreate, UserInLogin, UserInResponse

router = APIRouter()


@router.post("/users/login", response_model=UserInResponse, tags=["auth"])
async def login(
        user: UserInLogin = Body(..., embed=True), db: AsyncIOMotorClient = Depends(get_database)
):
    dbuser = await get_user_by_email(db, user.email)
    if not dbuser or not dbuser.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"username": dbuser.username}, expires_delta=access_token_expires
    )
    return UserInResponse(user=User(**dbuser.model_dump(), token=token))


@router.post(
    "/users/add",
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
            access_token_expires = timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            token = create_access_token(
                data={"username": dbuser.username}, expires_delta=access_token_expires
            )

            return UserInResponse(user=User(**dbuser.model_dump(), token=token))
