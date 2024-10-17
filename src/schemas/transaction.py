from datetime import datetime, UTC
from enum import Enum

from pydantic import BaseModel, Field
from typing_extensions import Optional


class Direction(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class Transaction(BaseModel):
    symbol: str
    direction: Direction
    amount_usdt: float = Field(gt=0)
    amount_coin: float = Field(gt=0)
    dt: datetime = Field(default=lambda: datetime.now(UTC))

    @property
    def usdt_price(self) -> float:
        return self.amount_usdt / self.amount_coin


class TransactionEntity(Transaction):
    id: str
    similar_transaction: Optional['TransactionEntity'] = None


class TransactionOfStatistics(Transaction):
    remaining_coin: float = Field(ge=0)


class TransactionOfStatisticsEntity(TransactionOfStatistics):
    id: str
