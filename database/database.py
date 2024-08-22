from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from database.config import config

engine_async = create_async_engine(
    url=config.DATABASE_URL_async,
    echo=False,
    pool_size=5,
    max_overflow=10
)


async def get_async_query() -> None:
    async with engine_async.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        print(res.first())
