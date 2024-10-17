from typing_extensions import Callable, Any, Awaitable

from events.intefaces.i_event import IEvent
from schemas.transaction import TransactionEntity


class CreatedTransactions(IEvent):
    transactions: list[TransactionEntity]
