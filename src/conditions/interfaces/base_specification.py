from sqlalchemy.sql.operators import and_, or_

from conditions.interfaces.i_specification import IConditionSpecification


class SqlAlchemySpecification(IConditionSpecification):
    def __and__(self, other: IConditionSpecification):
        return SqlAlchemySpecification(
            (
                and_(
                    self._condition,
                    other._condition
                )
            )
        )

    def __or__(self, other: IConditionSpecification):
        return SqlAlchemySpecification(
            (
                or_(
                    self._condition,
                    other._condition
                )
            )
        )

    def __invert__(self):
        return SqlAlchemySpecification(~self._condition)
