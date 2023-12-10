from .mysqldb import engine, SesionLocal, Base
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()
