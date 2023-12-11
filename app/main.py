from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
import logging

from .api.api_v1.api import router as api_router
from .core.config import API_V1_STR, PROJECT_NAME, ALLOWED_HOSTS
from app.core.errors import http_422_error_handler, http_error_handler

logging.basicConfig(
    level=logging.INFO,  # Set the desired log level
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)

app = FastAPI(title=PROJECT_NAME)

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(
    HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

app.include_router(api_router, prefix=API_V1_STR)
