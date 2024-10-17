from sqlalchemy.orm import selectinload

from joins.sa_join import SaJoinSpecification
from models import ReceiverOrm


class JoinAddresses(SaJoinSpecification):
    def __init__(self):
        super().__init__(selectinload(ReceiverOrm.responsibility_addresses))