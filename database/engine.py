from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from database.config import config

engine = create_engine(
    url=config.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10
)

session_factory = sessionmaker(engine)

class Base(DeclarativeBase):
    pass
