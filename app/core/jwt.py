from datetime import datetime, timedelta
import logging
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from sqlalchemy.orm import Session

from app.db.mysqlutils import get_db

from ..crud.user import get_user, get_user_by_email
from ..models.token import TokenPayload
from ..models.user import User

from .config import ACCESS_TOKEN_EXPIRE_MINUTES, AUTH_ENDPOINT, SECRET_KEY

ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl=AUTH_ENDPOINT)


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)
) -> User:
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])

        exp = payload.get("exp", None)

        if exp is None or datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Token has expired or is invalid"
            )

        token_data = TokenPayload(**payload)

    except JWTError as err:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=f"Could not validate credentials {err}",
        )

    dbuser = await get_user_by_email(db, token_data.email)

    if not dbuser:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="User not found")

    user = User(**dbuser.__dict__, token=token)
    return user


def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt
