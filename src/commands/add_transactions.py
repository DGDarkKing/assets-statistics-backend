from uuid import uuid4

from pydantic import parse_obj_as

from events.created_transactions import CreatedTransactions
from models import TransactionOrm
from schemas.transaction import Transaction, TransactionEntity
from utils.event_dispatcher import EventDispatcher
from utils.unit_of_work import UnitOfWork


class AddTransactionsCommand:
    def __init__(
            self,
            uow: UnitOfWork,
            event_dispatcher: EventDispatcher,
    ):
        self.__event_dispatcher = event_dispatcher
        self.__uow = uow
        self.__transaction_repo = self.__uow.transaction_repo

    async def __call__(self, transactions: list[Transaction]) -> list[TransactionEntity]:
        entities = [
            TransactionOrm(id=str(uuid4()), **trans.model_dump())
            for trans in transactions
        ]

        # open db transaction
        async with self.__uow:
            #   get similar transactions
            #   if exist then
            #       mark up potential duplicates

            #   save transactions
            self.__transaction_repo.add(entities)
            await self.__uow.flush()
            #   call event update transaction history
            created_transactions = CreatedTransactions(
                transactions=parse_obj_as(list[TransactionEntity], entities)
            )
            await self.__event_dispatcher.dispatch(created_transactions)
            await self.__uow.commit()

        return created_transactions.transactions
