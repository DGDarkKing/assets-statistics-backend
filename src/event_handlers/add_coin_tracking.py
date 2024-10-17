from conditions.coins import CoinSymbolsInSpecification
from event_handlers.interfaces.i_event_handler import IEventHandler
from events.created_transactions import CreatedTransactions
from models import CoinOrm
from publication.interfaces.i_publisher import IPublisher
from publication.messages.new_symbols import NewSymbolsMessage
from utils.unit_of_work import UnitOfWork


class AddCoinTracking(IEventHandler[CreatedTransactions]):
    def __init__(
            self,
            uow: UnitOfWork,
            publisher: IPublisher,
    ):
        self.__publisher = publisher
        self.__uow = uow

    async def __call__(self, created_transactions: CreatedTransactions):
        coin_pairs = {
            transaction.symbol
            for transaction in created_transactions.transactions
        }

        async with self.__uow:
            exist_coins: list[CoinOrm] = await self.__uow.coin_repo.get_all(
                CoinSymbolsInSpecification(coin_pairs)
            )
            exist_symbols = {
                coin.symbols
                for coin in exist_coins
            }
            not_exist_coins = [
                CoinOrm(
                    symbols=symbols
                )
                for symbols in coin_pairs
                if symbols not in exist_symbols
            ]
            self.__uow.coin_repo.add(not_exist_coins)

            new_symbols = NewSymbolsMessage(symbols={coin.symbols for coin in not_exist_coins})
            await self.__publisher.publish(new_symbols)

            await self.__uow.commit()
