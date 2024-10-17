from abc import ABC, abstractmethod

from publication.interfaces.i_publish_message import IPubishMessage


class IPublisher(ABC):
    @abstractmethod
    def publish(self, message: IPubishMessage):
        ...