from asyncio import current_task
from contextlib import asynccontextmanager
from functools import lru_cache

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_scoped_session, create_async_engine)
from sqlalchemy.orm import configure_mappers, declarative_base, sessionmaker

host = "cart_api_example_db"
user = "cart-api-example-user"
password = "ultra-secret-password123"
db_name = "cart-api-example-db"
Base = declarative_base()


class DBSession:
    def __init__(self, writer: bool = False):
        self.writer = writer

    async def __call__(self):
        async with self.get_db_session() as session:
            yield session

    @lru_cache
    def get_async_engine(self) -> AsyncEngine:
        async_engine = create_async_engine(
            f"postgresql+asyncpg://{user}:{password}@{host}/{db_name}", echo=True
        )
        configure_mappers()
        return async_engine

    @asynccontextmanager
    async def get_db_session(self) -> AsyncSession:
        session_factory = async_scoped_session(
            sessionmaker(
                self.get_async_engine(),
                expire_on_commit=False,
                class_=AsyncSession,
            ),
            scopefunc=current_task,
        )
        async_session = session_factory()

        try:
            yield async_session
            await async_session.commit()
        except Exception as e:
            print(f"Session rollback because of exception: {e}")
            await async_session.rollback()
            raise
        finally:
            await async_session.close()


db_session = DBSession()
