from fastapi import APIRouter

from .endpoints.auth import router as auth_router
from .endpoints.product import router as product_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(product_router)