from datetime import timedelta
import logging
from typing import List, Optional

from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from sqlalchemy.orm import Session

from app.db.mysqlutils import get_db
from app.crud.shortcuts import check_free_product_code, check_is_product_owner, check_is_valid_amout, check_is_valid_code, check_is_valid_name, check_is_valid_price
from app.models.user import User

from ....core.jwt import get_current_user
from ....crud.product import create_product, get_all_products, get_product, get_products, get_product_by_name, get_products_by_name, get_products_by_owner, remove_product, update_product
from ....models.product import ProductInResponse, ProductInCreate, ProductInUpdate

router = APIRouter()


@router.get("/products/get/", response_model=List[ProductInResponse], tags=["products", "search"])
async def products(code: Optional[str] = None, name: Optional[str] = None, db: Session = Depends(get_db)):

    products = []

    if code and len(code) > 2:

        dbproducts_by_code = await get_products(db, code)

        if dbproducts_by_code:
            for product in dbproducts_by_code:
                products.append(ProductInResponse(**product.__dict__))

    if name and len(name) > 2:

        dbproducts_by_name = await get_products_by_name(db, name)

        if dbproducts_by_name:
            for product in dbproducts_by_name:
                products.append(ProductInResponse(**product.__dict__))

    return products


@router.get("/products/get/all", response_model=List[ProductInResponse], tags=["products", "search"])
async def products_all(db: Session = Depends(get_db)):
    products = await get_all_products(db)
    return [ProductInResponse(**product.__dict__) for product in products]


@router.get("/products/get/own", response_model=List[ProductInResponse], tags=["products", "search"])
async def products_all(user=Depends(get_current_user), db: Session = Depends(get_db)):
    products = await get_products_by_owner(db, user.id)
    return [ProductInResponse(**product.__dict__) for product in products]


@router.post(
    "/product/add",
    response_model=ProductInResponse,
    tags=["products"],
    status_code=HTTP_201_CREATED,
)
async def product_add(
        new_product: ProductInCreate = Body(..., embed=True),
        user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    check_is_valid_name(new_product.name)
    check_is_valid_code(new_product.product_code)
    check_is_valid_amout(new_product.amount)
    check_is_valid_price(new_product.price)

    new_product.price = round(new_product.price, 2)

    await check_free_product_code(db, new_product.product_code)

    dbproduct = await create_product(db, new_product, user.id)
    return ProductInResponse(**dbproduct.__dict__)


@router.post(
    "/product/update",
    response_model=ProductInResponse,
    tags=["products"],
    status_code=HTTP_201_CREATED,
)
async def product_update(
        product: ProductInUpdate = Body(..., embed=True),
        user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    check_is_valid_name(product.name)
    check_is_valid_amout(product.amount)
    check_is_valid_price(product.price)

    await check_is_product_owner(db, user_id=user.id, product_code=product.product_code)

    if product.price:
        product.price = round(product.price, 2)

    updated_product = await update_product(db, product.product_code, product=product)

    return ProductInResponse(**updated_product.__dict__)


@router.post('/product/remove', tags=["products"], status_code=HTTP_200_OK)
async def product_remove(
    product_code=str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    await check_is_product_owner(db, user_id=user.id, product_code=product_code, scope='remove')
    await remove_product(db, product_code)

    return f'Product {product_code} removed'
