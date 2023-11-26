from typing import Optional
from .rwmodel import RWModel


class TokenPayload(RWModel):
    username: str = ""


class Token(RWModel):
    access_token: str
    token_type: str
