from io import BytesIO

from typing_extensions import IO

from commands.add_transactions import AddTransactionsCommand
from schemas.transaction import TransactionEntity
from services.interfaces.i_file_transaction_parser import IFileTransactionParser
from storages.minio_storage import MinioClient


class AddTransactionsFromS3FileCommand:
    def __init__(
            self,
            add_transactions_command: AddTransactionsCommand,
            client: MinioClient,
            parser: IFileTransactionParser,
    ):
        self.__parser = parser
        self.__client = client
        self.__add_transactions_command = add_transactions_command

    async def __call__(
            self,
            path: str
    ) -> list[TransactionEntity]:
        file = self.__get_file(path)
        transactions = self.__parser.parse(file)
        entities = await self.__add_transactions_command(transactions)
        return entities

    def __get_file(self, path) -> IO:
        path_parts = path.split('/')
        bucket, obj_name = path_parts[0], '/'.join(path_parts[1:])
        data = self.__client.get_object(bucket, obj_name)
        return BytesIO(data)
