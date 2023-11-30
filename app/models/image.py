from typing import List, Optional

from .dbmodel import DBModelMixin
from .rwmodel import RWModel


class ImageBase(RWModel):
    id: str
    owner_id: str
    image_base64: str


class ImageInDB(ImageBase):
    pass


class Image(ImageBase):
    id: str


class ImageInCreate(RWModel):
    image_base64: str
