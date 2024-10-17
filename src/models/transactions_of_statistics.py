from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import ModelBaseInt


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


class TransactionOfStatisticOrm(ModelBaseInt):
    __tablename__ = 'transactions_of_statistics'

    symbols: Mapped[str] = mapped_column(
        String(10),
        index=True
    )
    direction: Mapped[bool]
    amount_usdt: Mapped[float]
    amount_coin: Mapped[float]
    remaining_coin: Mapped[float]
    dt: Mapped[datetime]
