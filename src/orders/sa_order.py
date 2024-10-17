from typing_extensions import Self

from orders.interfaces.i_order import IOrderSpecification


class SaOrderSpecification(IOrderSpecification):
    def __init__(self, *orders):
        self.__orders = orders

    def complete(self) -> tuple:
        return self.__orders

    def __and__(self, other: "SaOrderSpecification") -> Self:
        return SaOrderSpecification(*self.__orders, *other.__orders)
