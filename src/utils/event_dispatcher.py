from typing_extensions import Type

from event_handlers.interfaces.i_event_handler import IEventHandler
from events.intefaces.i_event import IEvent


class EventDispatcher:

    def __init__(
            self,
            listeners: dict[
                Type[IEvent],
                list[IEventHandler]
            ]
    ):
        self.__listeners = listeners

    async def dispatch(
            self,
            event: IEvent
    ):
        handlers = self.__listeners.get(event.__class__, [])
        for handler in handlers:
            await handler(event)
