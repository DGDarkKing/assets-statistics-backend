import asyncio
import json
from abc import abstractmethod, ABC
from typing import Callable, AsyncGenerator, Sequence

from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractConnection, DeliveryMode, AbstractChannel

from conditions.events import UncompletedEventSpecification
from database import async_session_maker
from models import EventOrm
from orders.events import EventsCreatedAtAsc
from settings import app_settings
from utils.unit_of_work import UnitOfWork


# TODO run by "python -m additional_apps.db_consumer.main"

class OutboxService(ABC):
    def __init__(
            self,
            uow_create: Callable[[], AsyncGenerator[UnitOfWork, None]],
            max_message_fetch: int = 100
    ):
        self.__max_message_fetch = max_message_fetch
        self.__uow_create = uow_create

    async def run(self):
        generator = None

        try:
            while True:
                generator = self.__uow_create()
                uow = await generator.__anext__()
                await self.__process(uow)
                try:
                    await generator.__anext__()
                except StopIteration:
                    ...
                await asyncio.sleep(0.05)
        finally:
            try:
                if generator is not None:
                    await generator.__anext__()
            except StopIteration:
                ...

            await self._stop()

    async def __process(self, uow: UnitOfWork):
        num_messages = self.__max_message_fetch
        while num_messages >= self.__max_message_fetch:
            async with uow:
                try:
                    messages: Sequence[EventOrm] = await uow.event_repo.get_all(
                        condition=UncompletedEventSpecification(),
                        order=EventsCreatedAtAsc(),
                        limit=self.__max_message_fetch
                    )
                    num_messages = len(messages)
                    await self._handle_messages(messages)
                finally:
                    await uow.commit()

    @abstractmethod
    async def _handle_messages(self, messages: Sequence[EventOrm]):
        ...

    @abstractmethod
    async def _stop(self):
        ...


class RabbitMqOutboxService(OutboxService):
    def __init__(
            self,
            uow_create: Callable[[], AsyncGenerator[UnitOfWork, None]],
            rabbit_dsn: str,
            rabbitmq_publish_exchange: str,
            max_message_fetch: int = 100
    ):
        super().__init__(uow_create, max_message_fetch)

        self.__rabbitmq_publish_exchange = rabbitmq_publish_exchange
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

    async def _handle_messages(self, messages: Sequence[EventOrm]):
        await self.__connect()

        exchange = await self.__channel.get_exchange(self.__rabbitmq_publish_exchange)

        for event_msg in messages:
            message = event_msg.message
            routing_key: str = str(message['key'])
            rabbit_message = Message(
                body=json.dumps(message['body']).encode(),
                content_type="application/json",
                content_encoding="utf-8",
                delivery_mode=DeliveryMode.PERSISTENT,
            )

            await exchange.publish(
                routing_key=routing_key,
                message=rabbit_message
            )
            event_msg.completed = True


async def create_unit_of_work():
    async with async_session_maker() as session:
        uow = UnitOfWork(session)
        yield uow


async def main():
    outbox_service = RabbitMqOutboxService(create_unit_of_work, app_settings.mq_url,
                                           app_settings.rabbitmq_publish_exchange)
    await outbox_service.run()


if __name__ == '__main__':
    asyncio.run(main())
