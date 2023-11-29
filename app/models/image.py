from typing import Optional

from .dbmodel import DBModelMixin
from .rwmodel import RWModel


class ImageBase(RWModel):
    owner_id: str
    image_base64: str


class ImageInDB(ImageBase):
    pass


class Image(ImageBase):
    id: str


class ImageInCreate(ImageBase):
    pass


class ImageInResponse(RWModel):
    id: str
    image_base64: str
