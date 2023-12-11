from typing import Optional
from pydantic import EmailStr
from sqlalchemy import Column, Integer, String

from .rwmodel import RWModel
from ..core.security import generate_salt, get_password_hash, verify_password
from ..db.mysqldb import Base


class UserInDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(320), unique=True)
    salt = Column(String(128))
    hashed_password = Column(String(128))

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)


class UserBase(RWModel):
    email: EmailStr


class User(UserBase):
    id: int
    token: str


class UserInResponse(RWModel):
    user: User


class UserInLogin(RWModel):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    pass


class UserInUpdate(RWModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
