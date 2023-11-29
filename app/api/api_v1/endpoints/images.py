from datetime import timedelta
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST

from app.crud.shortcuts import check_is_image_owner

from ....core.jwt import get_current_user
from ....crud.image import get_image, create_image, remove_image
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.image import ImageInCreate

router = APIRouter()


@router.get("/image/get/", response_model=str, tags=["images"])
async def image(id: str, _db: AsyncIOMotorClient = Depends(get_database)):

    img = await get_image(_db, id)

    if not img:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Image does not exists"
        )

    return img.image_base64


@router.post(
    "/image/add",
    response_model=str,
    tags=["images"],
    status_code=HTTP_201_CREATED,
)
async def image_add(
        new_image: ImageInCreate = Body(..., embed=True),
        user=Depends(get_current_user),
        db: AsyncIOMotorClient = Depends(get_database)
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            new_image.owner_id = user.id
            create_id = await create_image(db, new_image)

            return create_id


@router.post('/image/remove', tags=["images"], status_code=HTTP_200_OK)
async def image_remove(
    id=str,
    user=Depends(get_current_user),
    db: AsyncIOMotorClient = Depends(get_database)
):

    await check_is_image_owner(db, user_id=user.id, image_id=id)
    await remove_image(db, id)

    return f'Image {id} removed'
