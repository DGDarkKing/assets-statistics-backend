from typing import Iterable

from conditions.interfaces.base_specification import SqlAlchemySpecification
from models import CoinOrm


class CoinSymbolsInSpecification(SqlAlchemySpecification):
    def __init__(self, coins_symbols: Iterable[str]):
        super().__init__(CoinOrm.symbols.in_(coins_symbols))
