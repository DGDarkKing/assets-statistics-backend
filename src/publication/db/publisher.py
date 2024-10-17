from typing import Type

from publication.interfaces.i_event_handler import IPublishHandler
from publication.interfaces.i_publish_message import IPubishMessage
from publication.interfaces.i_publisher import IPublisher


class DbPublisher(IPublisher):
    def __init__(
            self,
            publish_handlers: dict[Type[IPubishMessage], IPublishHandler]
    ):
        self.__publish_handlers = publish_handlers

    async def publish(self, message: IPubishMessage):
        handler = self.__publish_handlers.get(message.__class__, None)
        if handler is None:
            raise ValueError(f'PublishHandler not exists for {message.__class__}')
        await handler(message)
