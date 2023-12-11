from datetime import datetime
import logging
from sqlalchemy.orm import Session
from base64 import b64encode

from ..models.image import ImageBase, ImageInCreate, ImageInDB


async def get_image(conn: Session, id: str):
    return conn.query(ImageInDB).filter(ImageInDB.id == id).first()


async def get_images_by_owner(conn: Session, owner_id: str):
    return conn.query(ImageInDB).filter(ImageInDB.owner_id == owner_id).all()


async def create_image(conn: Session, new_image: ImageInCreate, owner_id: str):

    new_image_db = ImageInDB(
        image_base64=new_image.image_base64.encode(), owner_id=owner_id)

    conn.add(new_image_db)
    conn.commit()
    conn.refresh(new_image_db)

    return new_image_db.id


async def remove_image(conn: Session, id: str):
    db_image = await get_image(conn, id)
    conn.delete(db_image)
    conn.commit()
