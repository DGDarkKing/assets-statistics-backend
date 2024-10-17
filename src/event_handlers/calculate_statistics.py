from collections import defaultdict

from typing_extensions import cast

from event_handlers.interfaces.i_event_handler import IEventHandler
from events.created_transactions import CreatedTransactions
from models import AssetStatisticOrm, TransactionOfStatisticOrm
from schemas.coin_statistics import CoinStatistics
from schemas.transaction import Direction, TransactionOfStatisticsEntity
from services.statistic_calculator import StatisticFifoCalculator
from utils.unit_of_work import UnitOfWork


class CalculateStatistics(IEventHandler[CreatedTransactions]):
    def __init__(
            self,
            uow: UnitOfWork,
            calculator: StatisticFifoCalculator
    ):
        self.__calculator = calculator
        self.__uow = uow

    async def __call__(self, created_transactions: CreatedTransactions):
        buy_orders: dict[str, list[TransactionOfStatisticsEntity]] = defaultdict(list)
        sell_orders: dict[str, list[TransactionOfStatisticsEntity]] = defaultdict(list)

        for transaction in created_transactions.transactions:
            trans = TransactionOfStatisticsEntity(
                remaining_coin=transaction.amount_coin,
                **transaction.model_dump()
            )
            if trans.direction == Direction.BUY:
                buy_orders[trans.symbol].append(trans)
            else:
                sell_orders[trans.symbol].append(trans)

        for val in buy_orders.values():
            val.sort(key=lambda x: x.dt)

        for val in sell_orders.values():
            val.sort(key=lambda x: x.dt)

        statistics: list[CoinStatistics] = []
        updated_buy_orders: list[TransactionOfStatisticsEntity] = []
        for k, val in buy_orders.items():
            stat, trans_stat = self.__calculator.calc(val, sell_orders[k])
            updated_buy_orders.extend(cast(list[TransactionOfStatisticsEntity], trans_stat))
            statistics.append(stat)
            statistics[-1].symbol = k

        statistics_models = [
            AssetStatisticOrm(**stat.model_dump())
            for stat in statistics
        ]
        trans_stat_models: list[TransactionOfStatisticOrm] = [
            TransactionOfStatisticOrm(**order.model_dump())
            for order in updated_buy_orders
        ]
        for key, sell_orders_of_coin in sell_orders.items():
            trans_stat_models.extend([
                TransactionOfStatisticOrm(**sell_order.model_dump())
                for sell_order in sell_orders_of_coin
            ])
        async with self.__uow:
            self.__uow.asset_statistic_repo.add(statistics_models)
            self.__uow.transaction_statistics_repo.add(trans_stat_models)
            await self.__uow.commit()
