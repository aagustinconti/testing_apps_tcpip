from .rwmodel import RWModel


class TokenPayload(RWModel):
    email: str = ""
    id: int = 0


class Token(RWModel):
    access_token: str
    token_type: str
