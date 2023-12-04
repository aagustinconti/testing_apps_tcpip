from typing import List, Optional

from .dbmodel import DBModelMixin
from .rwmodel import RWModel


class ImageBase(RWModel):
    owner_id: str
    image_base64: str


class ImageInDB(ImageBase):
    id: str


class Image(ImageBase):
    id: str


class ImageInCreate(RWModel):
    image_base64: str
