from fastapi import Depends
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from commands.add_transactions import AddTransactionsCommand
from commands.add_transactions_from_s3_file import AddTransactionsFromS3FileCommand
from database import get_async_session
from event_handlers.add_coin_tracking import AddCoinTracking
from event_handlers.calculate_statistics import CalculateStatistics
from events.created_transactions import CreatedTransactions
from publication.db.publish_new_symbols import PublishNewSymbols

from publication.db.publisher import DbPublisher
from publication.interfaces.i_publisher import IPublisher
from publication.messages.new_symbols import NewSymbolsMessage
from queries.generate_load_transaction_file_url import GenerateLoadTransactionFileUrlQuery
from services.excel_transaction_parser import ExcelTransactionParser
from services.interfaces.i_file_transaction_parser import IFileTransactionParser
from services.statistic_calculator import StatisticFifoCalculator
from settings import app_settings
from storages.minio_storage import MinioClient
from utils.event_dispatcher import EventDispatcher
from utils.unit_of_work import UnitOfWork


def create_s3_client() -> MinioClient:
    client = Minio(
        endpoint=app_settings.s3_url,
        access_key=app_settings.s3_access_key,
        secret_key=app_settings.s3_secret_key,
        secure=app_settings.s3_secure,
    )
    return MinioClient(client)


S3ClientDeps = Annotated[MinioClient, Depends(create_s3_client)]

FileTransactionParserDepends = Annotated[IFileTransactionParser, Depends(ExcelTransactionParser)]


def create_generate_load_transaction_file_url_query(
        s3_client: S3ClientDeps,
) -> GenerateLoadTransactionFileUrlQuery:
    return GenerateLoadTransactionFileUrlQuery(s3_client)


GenerateLoadTransactionFileUrlQueryDeps = Annotated[
    GenerateLoadTransactionFileUrlQuery,
    Depends(create_generate_load_transaction_file_url_query)
]

AsyncSessionDeps = Annotated[AsyncSession, Depends(get_async_session)]


def create_unit_of_work(
        session: AsyncSessionDeps
) -> UnitOfWork:
    return UnitOfWork(session)


UnitOfWorkDeps = Annotated[UnitOfWork, Depends()]

StatisticCalculatorDeps = Annotated[StatisticFifoCalculator, Depends(StatisticFifoCalculator)]


def create_calculate_statistics(
        uow: UnitOfWorkDeps,
        calculator: StatisticCalculatorDeps,
) -> CalculateStatistics:
    return CalculateStatistics(uow, calculator)


CalculateStatisticsDeps = Annotated[CalculateStatistics, Depends(create_calculate_statistics)]


def create_publish_new_symbols(
        uow: UnitOfWorkDeps,
) -> PublishNewSymbols:
    return PublishNewSymbols(uow)


PublishNewSymbolsDeps = Annotated[PublishNewSymbols, Depends(create_publish_new_symbols)]

def create_db_publisher(
        publish_new_symbols: PublishNewSymbolsDeps,
) -> IPublisher:
    return DbPublisher({
        NewSymbolsMessage: publish_new_symbols
    })

DbPublisherDeps = Annotated[IPublisher, Depends(create_db_publisher)]

def create_add_coin_tracking(
        uow: UnitOfWorkDeps,
        publisher: DbPublisherDeps,
) -> AddCoinTracking:
    return AddCoinTracking(uow, publisher)


AddCoinTrackingDeps = Annotated[AddCoinTracking, Depends(create_add_coin_tracking)]


def create_event_dispatcher(
        calculate_statistics: CalculateStatisticsDeps,
        add_coin_tracking: AddCoinTrackingDeps,

) -> EventDispatcher:
    return EventDispatcher({
        CreatedTransactions: [calculate_statistics, add_coin_tracking],
    })


EventDispatcherDeps = Annotated[EventDispatcher, Depends(create_event_dispatcher)]


def create_add_transactions_command(
        uow: UnitOfWorkDeps,
        event_dispatcher: EventDispatcherDeps,
) -> AddTransactionsCommand:
    return AddTransactionsCommand(uow, event_dispatcher)


AddTransactionsCommandDeps = Annotated[AddTransactionsCommand, Depends(create_add_transactions_command)]


def create_add_transactions_from_file_command(
        add_transactions_command: AddTransactionsCommandDeps,
        s3_client: S3ClientDeps,
        file_transaction_parser: FileTransactionParserDepends,
) -> AddTransactionsFromS3FileCommand:
    return AddTransactionsFromS3FileCommand(
        add_transactions_command,
        s3_client,
        file_transaction_parser,
    )


AddTransactionsFromS3FileCommandDepends = Annotated[
    AddTransactionsFromS3FileCommand,
    Depends(create_add_transactions_from_file_command)
]
