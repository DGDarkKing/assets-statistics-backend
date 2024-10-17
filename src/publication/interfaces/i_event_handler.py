from abc import ABC, abstractmethod

from typing_extensions import TypeVar

from events.intefaces.i_event import IEvent

T = TypeVar('EventTemplate', bound=IEvent)

class IPublishHandler[T](ABC):
    @abstractmethod
    async def __call__(self, event: T):
        ...
