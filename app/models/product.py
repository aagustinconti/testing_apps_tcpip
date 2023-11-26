from typing import ClassVar, Optional

from pydantic import AnyUrl

from .dbmodel import DBModelMixin
from .rwmodel import RWModel


class ProductBase(RWModel):
    product_code: str
    name: str
    price: float
    amount: int
    image: Optional[str] = None
    description: Optional[str] = None


class ProductInDB(DBModelMixin, ProductBase):
    owner_id: str = ""


class Product(ProductBase):
    pass


class ProductInResponse(RWModel):
    product_code: str
    name: str
    price: float
    amount: int
    image: Optional[str] = None
    description: Optional[str] = None


class ProductInCreate(ProductBase):
    owner_id: str


class ProductInUpdate(RWModel):
    product_code: str
    name: Optional[str] = None
    price: Optional[float] = None
    amount: Optional[int] = None
    image: Optional[str] = None
    description: Optional[str] = None


class ProductInSearch(RWModel):
    code: Optional[str] = None
    name: Optional[str] = None
