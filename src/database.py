from datetime import datetime
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from typing_extensions import Annotated

from settings import app_settings

async_engine = create_async_engine(
    app_settings.db_async_url,
)
async_session_maker = async_sessionmaker(
    async_engine,
    expire_on_commit=False
)

IntPk = Annotated[int, mapped_column(primary_key=True)]
UuidPk = Annotated[UUID, mapped_column(primary_key=True)]
DateTimeServerNow = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class ModelBase(DeclarativeBase):
    pass


class ModelBaseInt(ModelBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class ModelBaseUuid(ModelBase):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True)


def create_tables():
    ModelBase.metadata.create_all(async_engine.engine)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
