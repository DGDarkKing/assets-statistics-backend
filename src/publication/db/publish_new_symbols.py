from models import EventOrm
from publication.interfaces.i_event_handler import IPublishHandler
from publication.messages.new_symbols import NewSymbolsMessage
from utils.unit_of_work import UnitOfWork


class PublishNewSymbols(IPublishHandler[NewSymbolsMessage]):
    def __init__(
            self,
            uow: UnitOfWork,
    ):
        self.__uow = uow

    async def __call__(self, new_symbols: NewSymbolsMessage):
        async with self.__uow:
            events = {
                EventOrm(
                    message={
                        'key': 'coin-statistics',
                        'body': {
                            'symbols': symbols
                        }
                    }
                )
                for symbols in new_symbols.symbols
            }
            self.__uow.event_repo.add(events)
            await self.__uow.commit()
