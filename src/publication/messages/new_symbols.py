from typing import Iterable

from publication.interfaces.i_publish_message import IPubishMessage


class NewSymbolsMessage(IPubishMessage):
    symbols: Iterable[str]
