from datetime import datetime
import logging
from sqlalchemy.orm import Session

from ..models.product import ProductInCreate, ProductInDB, ProductInUpdate


async def get_product(conn: Session, code: str):
    return conn.query(ProductInDB).filter(ProductInDB.product_code == code).first()


async def get_products(conn: Session, code_like: str) -> list[ProductInDB]:
    return conn.query(ProductInDB).filter(ProductInDB.product_code.like(f'{code_like}%')).all()


async def get_product_by_name(conn: Session, name_like: str):
    return conn.query(ProductInDB).filter(ProductInDB.name.like(f'{name_like}%')).first()


async def get_products_by_name(conn: Session, name_like: str) -> list[ProductInDB]:
    return conn.query(ProductInDB).filter(ProductInDB.name.like(f'{name_like}%')).all()


async def get_all_products(conn: Session):
    return conn.query(ProductInDB).all()


async def get_products_by_owner(conn: Session, owner_id: int):
    return conn.query(ProductInDB).filter(ProductInDB.owner_id == owner_id).all()


async def create_product(conn: Session, product: ProductInCreate, owner_id: str) -> ProductInDB:

    dbproduct = ProductInDB(**product.model_dump(), owner_id=owner_id)

    conn.add(dbproduct)
    conn.commit()
    conn.refresh(dbproduct)

    return dbproduct


async def update_product(conn: Session, code: str, product: ProductInUpdate):
    dbproduct = await get_product(conn, code)

    dbproduct.name = product.name or dbproduct.name
    dbproduct.price = product.price or dbproduct.price
    dbproduct.amount = product.amount or dbproduct.amount
    dbproduct.description = product.description or dbproduct.description
    dbproduct.image = product.image or dbproduct.image

    conn.flush()
    conn.commit()
    conn.refresh(dbproduct)

    return dbproduct


async def remove_product(conn: Session, code: str):
    dbproduct = await get_product(conn, code)
    conn.delete(dbproduct)
    conn.commit()
