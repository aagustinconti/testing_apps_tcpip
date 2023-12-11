from pydantic import EmailStr
from sqlalchemy.orm import Session

from ..models.user import UserInCreate, UserInDB, UserInDB, UserInUpdate


async def get_user(conn: Session, id: int) -> UserInDB | None:
    return conn.query(UserInDB).filter(UserInDB.id == id).first()


async def get_user_by_email(conn: Session, email: EmailStr) -> UserInDB | None:
    return conn.query(UserInDB).filter(UserInDB.email == email).first()


async def create_user(conn: Session, user: UserInCreate) -> UserInDB:

    dbuser = UserInDB(email=user.email)
    dbuser.change_password(user.password)

    conn.add(dbuser)
    conn.commit()

    return dbuser


async def update_user(conn: Session, id: int, user: UserInUpdate) -> UserInDB:
    dbuser = await get_user(conn, id)

    dbuser.email = user.email or dbuser.email

    if user.password:
        dbuser.change_password(user.password)

    conn.commit()
    conn.refresh(dbuser)

    return dbuser
