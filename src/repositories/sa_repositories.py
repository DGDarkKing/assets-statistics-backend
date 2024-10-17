from models import CoinOrm, TransactionOrm, AssetStatisticOrm, TransactionOfStatisticOrm
from models.events import EventOrm
from repositories.sa_repository import SaAsyncRepository


class TransactionRepository(SaAsyncRepository):
    _MODEL = TransactionOrm


class AssetStatisticsRepository(SaAsyncRepository):
    _MODEL = AssetStatisticOrm


class TransactionOfStatisticRepository(SaAsyncRepository):
    _MODEL = TransactionOfStatisticOrm


class CoinRepository(SaAsyncRepository):
    _MODEL = CoinOrm


class EventRepository(SaAsyncRepository):
    _MODEL = EventOrm
