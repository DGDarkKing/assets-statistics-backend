from datetime import datetime

from sqlalchemy import Table, Column, String, Boolean, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database import ModelBase

# TRANSACTIONS = Table(
#     'transactions',
#     metadata,
#     Column('id', String(length=20), primary_key=True),
#     Column('symbols', String(length=10)),
#     Column('direction', Boolean),
#     Column('amount_usdt', Float),
#     Column('amount_coin', Float),
#     Column('dt', DateTime),
# )

class TransactionOrm(ModelBase):
    __tablename__ = 'transactions'

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    symbols: Mapped[str] = mapped_column(String(10))
    direction: Mapped[bool]
    amount_usdt: Mapped[float]
    amount_coin: Mapped[float]
    dt: Mapped[datetime]
