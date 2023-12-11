from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import MYSQL_DB, MYSQL_HOST, MYSQL_MOTOR, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD

DATABASE_URL = f'{MYSQL_MOTOR}://{MYSQL_USER}{ ( f":{MYSQL_PASSWORD}" if len(MYSQL_PASSWORD) > 0 else "" ) }@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'

engine = create_engine(DATABASE_URL)

SesionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
