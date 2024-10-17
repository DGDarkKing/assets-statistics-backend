from abc import ABC, abstractmethod

from typing_extensions import Self


class IJoinSpecification(ABC):
    @abstractmethod
    def complete(self) -> tuple:
        ...

    @abstractmethod
    def __and__(self, other) -> Self:
        ...

