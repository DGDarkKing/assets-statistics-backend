from typing import Iterable

from conditions.interfaces.base_specification import SqlAlchemySpecification
from models import EventOrm


class UncompletedEventSpecification(SqlAlchemySpecification):
    def __init__(self):
        super().__init__(EventOrm.completed == False)
