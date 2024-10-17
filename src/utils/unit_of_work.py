from sqlalchemy.ext.asyncio import AsyncSession

from repositories.sa_repositories import TransactionRepository, AssetStatisticsRepository, \
    TransactionOfStatisticRepository, CoinRepository, EventRepository


class UnitOfWork:
    transaction_repo: TransactionRepository
    asset_statistic_repo: AssetStatisticsRepository
    transaction_statistics_repo: TransactionOfStatisticRepository
    coin_repo: CoinRepository
    event_repo: EventRepository

    def __init__(
            self,
            session: AsyncSession
    ):
        self.__session = session
        self.__session_counter = 0
        self.__current = 0
        self.__transactions = []

    def __init(self):
        if self.__session_counter == 1:
            self.transaction_repo = TransactionRepository(self.__session)
            self.asset_statistic_repo = AssetStatisticsRepository(self.__session)
            self.transaction_statistics_repo = TransactionOfStatisticRepository(self.__session)
            self.coin_repo = CoinRepository(self.__session)
            self.event_repo = EventRepository(self.__session)

    async def __aenter__(self):
        self.__session_counter += 1
        self.__current += 1
        self.__init()

        if self.__session_counter == 2:
            self.__transactions.append(self.__session.begin())
        elif self.__session_counter > 2:
            self.__transactions.append(self.__session.begin_nested())

    def __del(self):
        if self.__session_counter == 0:
            del self.transaction_repo
            del self.asset_statistic_repo
            del self.transaction_statistics_repo
            del self.coin_repo
            del self.event_repo

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        if self.__session_counter - 1 == self.__current:
            self.__session_counter -= 1
            self.__del()

    async def commit(self):
        if self.__session_counter == self.__current:
            transaction = self.__get_transaction()
            await transaction.commit()
            self.__current -= 1

    async def rollback(self):
        if self.__session_counter == self.__current:
            transaction = self.__get_transaction()
            await transaction.rollback()
            self.__current -= 1

    async def flush(self):
        await self.__session.flush()

    def __get_transaction(self):
        return self.__transactions.pop() if self.__transactions else self.__session
