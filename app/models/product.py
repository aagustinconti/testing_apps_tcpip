from typing import ClassVar, Optional

from pydantic import AnyUrl

from .dbmodel import DBModelMixin
from .rwmodel import RWModel


class ProductBase(RWModel):
    product_code: str
    name: str
    price: int
    amount: int
    image: Optional[AnyUrl] = None
    description: Optional[str] = None


class ProductInDB(DBModelMixin, ProductBase):
    owner_id: str = ""


class Product(ProductBase):
    pass


class ProductInResponse(RWModel):
    name: str
    price: int
    amount: int
    image: Optional[AnyUrl] = None
    description: Optional[str] = None


class ProductInCreate(ProductBase):
    owner_id: str


class ProductInUpdate(RWModel):
    product_code: str
    name: Optional[str] = None
    price: Optional[int] = None
    amount: Optional[int] = None
    image: Optional[AnyUrl] = None
    description: Optional[str] = None
