from typing import Any

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from database import DateTimeServerNow, ModelBaseInt


class EventOrm(ModelBaseInt):
    __tablename__ = 'events'

    message: Mapped[dict[str, Any]] = mapped_column(JSONB(none_as_null=True))
    created_at: Mapped[DateTimeServerNow]
    completed: Mapped[bool] = mapped_column(default=False)
