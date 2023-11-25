from datetime import timedelta
from typing import List, Optional

from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.crud.shortcuts import check_free_username_and_email, check_free_product_code, check_is_product_owner

from ....core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from ....core.jwt import get_current_user_authorizer
from ....crud.product import create_product, get_product, get_products, get_product_by_name, get_products_by_name, update_product
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.product import ProductInResponse, ProductInCreate, ProductInUpdate

router = APIRouter()


@router.get("/products/get/", response_model=List[ProductInResponse], tags=["products", "search"])
async def get_products(code: Optional[str] = None, name: Optional[str] = None, _db_: AsyncIOMotorClient = Depends(get_database)):

    products = []

    if code and len(code) > 2:

        dbproducts_by_code = await get_products(_db_, code)

        if dbproducts_by_code:
            for product in dbproducts_by_code:
                products.append(ProductInResponse(**product.model_dump()))

    if name and len(name) > 2:

        dbproducts_by_name = await get_products_by_name(_db_, code)

        if dbproducts_by_name:
            for product in dbproducts_by_name:
                products.append(ProductInResponse(product.model_dump()))

    return products


@router.post(
    "/product/add",
    response_model=ProductInResponse,
    tags=["products"],
    status_code=HTTP_201_CREATED,
)
async def product_update(
        new_product: ProductInCreate = Body(..., embed=True),
        user=Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database)
):

    await check_free_product_code(db, new_product.product_code)

    async with await db.start_session() as s:
        async with s.start_transaction():
            new_product.owner_id = user._id
            dbproduct = await create_product(db, new_product)

            return ProductInResponse(dbproduct.model_dump())


@router.post(
    "/product/update",
    response_model=ProductInResponse,
    tags=["products"],
    status_code=HTTP_201_CREATED,
)
async def product_update(
        new_product: ProductInUpdate = Body(..., embed=True),
        user=Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database)
):

    await check_is_product_owner(db, user_id=user._id, product_code=new_product.product_code)
    updated_product = await update_product(db, new_product.product_code, product=new_product)
    return ProductInResponse(updated_product.model_dump())
