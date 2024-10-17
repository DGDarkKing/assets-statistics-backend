from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column

from database import ModelBase


# COINS = Table(
#     'coins',
#     metadata,
#     Column('symbols', String(length=10), primary_key=True),
#     Column('price', Float),
#     Column('updated_at', DateTime),
# )


class CoinOrm(ModelBase):
    __tablename__ = 'coins'

    symbols: Mapped[str] = mapped_column(String(10), primary_key=True)
    price: Mapped[float | None] = mapped_column(default=None)
    price_updated_at: Mapped[datetime | None] = mapped_column(default=None)

