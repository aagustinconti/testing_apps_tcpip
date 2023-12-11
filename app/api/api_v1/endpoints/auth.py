from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from sqlalchemy.orm import Session

from app.crud.shortcuts import check_free_email
from app.db.mysqlutils import get_db

from ....core.config import ACCESS_TOKEN_EXPIRE_MINUTES, AUTH_ENDPOINT
from ....core.jwt import create_access_token
from ....crud.user import create_user, get_user_by_email
from ....models.user import User, UserInCreate, UserInResponse
from ....models.token import Token

router = APIRouter()


@router.post(AUTH_ENDPOINT, response_model=Token, tags=["auth"])
async def login(
        user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    dbuser = await get_user_by_email(db, user.username)
    if not dbuser or not dbuser.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )

    token = create_access_token(data={"email": dbuser.email})

    return Token(access_token=token, token_type='bearer')


@router.post(
    "/auth/register",
    response_model=UserInResponse,
    tags=["auth"],
    status_code=HTTP_201_CREATED,
)
async def register(
        user: UserInCreate = Body(..., embed=True), db: Session = Depends(get_db)
):
    await check_free_email(db, user.email)

    dbuser = await create_user(db, user)
    token = create_access_token(data={"email": dbuser.email, "id": dbuser.id})

    return UserInResponse(user=User(**dbuser.__dict__, token=token))
