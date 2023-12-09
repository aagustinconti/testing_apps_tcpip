from sqlalchemy import Column, Integer, String, LargeBinary
import uuid

from .rwmodel import RWModel
from ..db.mysqldb import Base


class ImageBase(RWModel):
    owner_id: str
    image_base64: str


class ImageInDB(Base):
    __tablename__ = 'images'

    id = Column(String(36), nullable=False, primary_key=True,
                default=uuid.uuid4, index=True)
    owner_id = Column(Integer)
    image_base64 = Column(LargeBinary)


class Image(ImageBase):
    id: str


class ImageInCreate(RWModel):
    image_base64: str
