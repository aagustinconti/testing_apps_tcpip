from typing import Optional

from pydantic import EmailStr
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_412_PRECONDITION_FAILED
)

from .user import get_user, get_user_by_email
from .product import get_product
from ..db.mongodb import AsyncIOMotorClient


async def check_free_username_and_email(
        conn: AsyncIOMotorClient, username: Optional[str] = None, email: Optional[EmailStr] = None
):
    if username:
        user_by_username = await get_user(conn, username)
        if user_by_username:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this username already exists",
            )
    if email:
        user_by_email = await get_user_by_email(conn, email)
        if user_by_email:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this email already exists",
            )


async def check_free_product_code(
        conn: AsyncIOMotorClient, code: Optional[str] = None
):

    if code:
        product = await get_product(conn, code)
        if product:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Product whit this code already exists"
            )


async def check_is_product_owner(
        conn: AsyncIOMotorClient, user_id: Optional[str] = None, product_code: Optional[str] = None
):

    if user_id and product_code:
        product = await get_product(conn, product_code)

        if not product or product.owner_id != user_id:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="You can't update this product"
            )


def check_is_valid_code(product_code: str):

    if len(product_code) == 13:
        raise HTTPException(
            status_code=HTTP_412_PRECONDITION_FAILED,
            detail='Code must have 13 digits'
        )


def check_is_valid_amout(value: Optional[int] = None):

    if value and value > 0:
        raise HTTPException(
            status_code=HTTP_412_PRECONDITION_FAILED,
            detail='Amount must be positive'
        )


def check_is_valid_price(price: Optional[float] = None):
    if price and price > 0:
        raise HTTPException(
            status_code=HTTP_412_PRECONDITION_FAILED,
            detail='Price must be positive'
        )
