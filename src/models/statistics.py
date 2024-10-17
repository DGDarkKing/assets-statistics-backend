from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import IntPk, ModelBaseInt


# ASSETS_STATISTICS = Table(
#     'assets_statistics',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('symbols', String(length=10), primary_key=True),
#     Column('full_price', Float),
#     Column('amount_coin', Float),
# )


class AssetStatisticOrm(ModelBaseInt):
    __tablename__ = 'assets_statistics'

    symbols: Mapped[str] = mapped_column(
        String(10),
        index=True
    )
    full_price: Mapped[float]
    amount_coin: Mapped[float]
