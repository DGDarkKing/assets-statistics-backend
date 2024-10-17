from collections import defaultdict

from schemas.transaction import TransactionEntity
from utils.unit_of_work import UnitOfWork


class CalculateStatisticsCommand:
    def __init__(
            self,
            uow: UnitOfWork,

    ):
        self.__uow = uow
        self.__statistic_repo = self.__uow.asset_statistic_repo
        self.__transaction_repo = self.__uow.transaction_repo

    async def __call__(
            self,
            events: list[TransactionEntity]
    ) -> list[CoinStatistics]:
        if not events:
            return []

        group_by_pairs =


        async with self.__uow:



