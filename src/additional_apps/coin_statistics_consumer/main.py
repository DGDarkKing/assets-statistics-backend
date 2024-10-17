import asyncio
from abc import ABC, abstractmethod
from typing import Callable, AsyncGenerator

from aio_pika import connect_robust
from aio_pika.abc import AbstractConnection, AbstractChannel

from database import async_session_maker
from settings import app_settings
from utils.unit_of_work import UnitOfWork


class IConsumer(ABC):
    @abstractmethod
    async def consume(self):
        ...

    @abstractmethod
    async def nack(self, tag, all):
        ...


class RabbitMqConsumer(IConsumer):
    def __init__(
            self,
            rabbit_dsn: str,
            queue: str,
            prefetch_count: int = 0
    ):
        self.__prefetch_count = prefetch_count
        self.__queue = queue
        self.__rabbit_dsn = rabbit_dsn
        self.__connection: AbstractConnection = None
        self.__channel: AbstractChannel = None

    async def _stop(self):
        if self.__connection is not None and not self.__connection.is_closed:
            await self.__connection.close()

    async def __connect(self):
        if self.__connection is None or self.__connection.is_closed:
            self.__connection = await connect_robust(self.__rabbit_dsn)
        if self.__channel is None or self.__channel.is_closed:
            self.__channel = await self.__connection.channel()
            await self.__channel.set_qos(self.__prefetch_count)

    async def consume(self):
        await self.__connect()
        # TODO
        pass

    async def nack(self, tag, all):
        await self.__connect()
        # TODO
        pass


class CoinStatisticsServer:
    def __init__(
            self,
            uow_create: Callable[[], AsyncGenerator[UnitOfWork, None]],
            consumer: IConsumer,
            max_message_fetch: int = 100
    ):
        self.__consumer = consumer
        self.__max_message_fetch = max_message_fetch
        self.__uow_create = uow_create

    async def run(self):
        # TODO
        pass






async def create_unit_of_work():
    async with async_session_maker() as session:
        uow = UnitOfWork(session)
        yield uow


async def main():
    consumer = RabbitMqConsumer(app_settings.mq_url, app_settings.queue)
    coin_statistics_server = CoinStatisticsServer(create_unit_of_work, consumer)
    await coin_statistics_server.run()


if __name__ == '__main__':
    asyncio.run(main())
