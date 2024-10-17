from typing_extensions import Self

from joins.interfaces.i_join_specification import IJoinSpecification


class SaJoinSpecification(IJoinSpecification):
    def __init__(self, *joins):
        self.__joins = joins

    def complete(self) -> tuple:
        return self.__joins

    def __and__(self, other: "SaJoinSpecification") -> Self:
        return SaJoinSpecification(*self.__joins, *other.__joins)
