from abc import ABC, abstractmethod

from typing_extensions import IO

from schemas.transaction import Transaction


class IFileTransactionParser(ABC):
    REQUIRED_FIELDS = []
    AT_LEAST_ONE_REQUIRED_FIELDS_BY_RULES = {}

    @abstractmethod
    def parse(self, file: str | IO) -> list[Transaction]:
        ...
