from collections import defaultdict
from itertools import groupby

from schemas.coin_statistics import CoinStatistics
from schemas.transaction import TransactionEntity, Direction
from services.statistic_calculator import StatisticFifoCalculator
from utils.unit_of_work import UnitOfWork


class RecalculateStatisticsCommand:
    def __init__(
            self,
            uow: UnitOfWork,
            calculator: StatisticFifoCalculator
    ):
        self.__calculator = calculator
        self.__uow = uow
        self.__statistic_repo = self.__uow.asset_statistic_repo
        self.__transaction_repo = self.__uow.transaction_repo

    async def __call__(
            self,
            coin_symbols: set[str]
    ) -> list[CoinStatistics]:
        if not coin_symbols:
            return []

        async with self.__uow:
            transactions = await self.__transaction_repo.get_all(
                SymbolIn(coin_symbols) & UniqueTransactions(),
                DtOrderAsc()
            )

            statistics = self.__calculate(transactions)
            self.__statistic_repo.add(statistics)
            await self.__uow.commit()
        return statistics

    def __calculate(
            self,
            transactions: list[TransactionEntity]
    ) -> list[CoinStatistics]:
        symbol: str
        transaction_list: list[TransactionEntity]
        results: list[CoinStatistics] = []
        for symbol, transaction_list in groupby(transactions, key=lambda x: x.symbol):
            buy_orders, sell_orders = [], []
            for order in transaction_list:
                if order.direction == Direction.BUY:
                    buy_orders.append(order)
                else:
                    sell_orders.append(order)

            coin_statistics = self.__calculator.calc(buy_orders, sell_orders)
            coin_statistics.symbol = symbol
            results.append(coin_statistics)
        return results
