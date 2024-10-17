from abc import ABC, abstractmethod
from typing import Any

from conditions.interfaces.i_specification import IConditionSpecification
from joins.interfaces.i_join_specification import IJoinSpecification
from orders.interfaces.i_order import IOrderSpecification


class IRepository(ABC):
    @abstractmethod
    def add(self, objs: list):
        ...

    @abstractmethod
    async def delete(self, objs: list):
        ...

    @abstractmethod
    async def delete_by_condition(self, condition: IConditionSpecification = None):
        ...

    @abstractmethod
    async def get_all(
            self,
            condition: IConditionSpecification = None,
            join: IJoinSpecification = None,
            order: IOrderSpecification = None,
            limit: int = 0
    ) -> list[Any]:
        ...
