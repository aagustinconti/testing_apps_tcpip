from typing import Optional
from sqlalchemy import Column, Integer, String, Float, Text

from .rwmodel import RWModel
from ..db.mysqldb import Base


class ProductBase(RWModel):
    product_code: str
    name: str
    price: float
    amount: int
    image: Optional[str] = None
    description: Optional[str] = None
    owner_id: str


class ProductInDB(Base):
    __tablename__ = 'products'

    product_code = Column(String(15), primary_key=True,
                          autoincrement=False, index=True)
    name = Column(String(255), primary_key=True,
                  autoincrement=False, index=True)
    price = Column(Float(2))
    amount = Column(Integer)
    image = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    owner_id = Column(Integer)


class Product(ProductBase):
    pass


class ProductInResponse(RWModel):
    product_code: str
    name: str
    price: float
    amount: int
    image: Optional[str] = None
    description: Optional[str] = None


class ProductInCreate(RWModel):
    product_code: str
    name: str
    price: float
    amount: int
    image: Optional[str] = None
    description: Optional[str] = None


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
