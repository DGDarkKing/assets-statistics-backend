from models import EventOrm
from orders.sa_order import SaOrderSpecification


class EventsCreatedAtAsc(SaOrderSpecification):
    def __init__(self):
        super().__init__(EventOrm.created_at.asc())
