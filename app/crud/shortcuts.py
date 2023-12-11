from typing import Optional

from pydantic import EmailStr
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_412_PRECONDITION_FAILED,
    HTTP_400_BAD_REQUEST
)
from sqlalchemy.orm import Session

from .user import get_user, get_user_by_email
from .product import get_product
from .image import get_image


async def check_free_email(
        conn: Session, email: Optional[EmailStr] = None
):
    if email:
        user_by_email = await get_user_by_email(conn, email)
        if user_by_email:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this email already exists",
            )


async def check_free_product_code(
        conn: Session, code: Optional[str] = None
):

    if code:
        product = await get_product(conn, code)
        if product:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Product whit this code already exists"
            )


async def check_is_product_owner(
        conn: Session, user_id: Optional[str] = None, product_code: Optional[str] = None, scope: Optional[str] = "update"
):

    if user_id and product_code:
        product = await get_product(conn, product_code)

        if not product or product.owner_id != user_id:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f"You can't {scope} this product"
            )

        return

    raise HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail='Product not found'
    )


def check_is_valid_code(product_code: str):
    if len(product_code) < 8 or len(product_code) > 15:
        raise HTTPException(
            status_code=HTTP_412_PRECONDITION_FAILED,
            detail='Code must be between 8 and 15 digits'
        )


def check_is_valid_amout(value: Optional[int] = None):
    if value and value < 0:
        raise HTTPException(
            status_code=HTTP_412_PRECONDITION_FAILED,
            detail='Amount must be positive'
        )


def check_is_valid_price(price: Optional[float] = None):
    if price and price < 0:
        raise HTTPException(
            status_code=HTTP_412_PRECONDITION_FAILED,
            detail='Price must be positive'
        )


def check_is_valid_name(name: Optional[str] = None):
    if name and (len(name) < 3 or len(name) > 50):
        raise HTTPException(
            status_code=HTTP_412_PRECONDITION_FAILED,
            detail='Name must be between 3 and 50 digits'
        )


async def check_is_image_owner(
        conn: Session, user_id: Optional[str] = None, image_id: Optional[str] = None):

    if user_id and image_id:
        image = await get_image(conn, image_id)

        if not image or image.owner_id != user_id:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f"You can't remove this image"
            )

        return

    raise HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail='Image not found'
    )
