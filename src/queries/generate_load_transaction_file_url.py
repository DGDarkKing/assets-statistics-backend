from storages.minio_storage import MinioClient


class GenerateLoadTransactionFileUrlQuery:
    def __init__(
            self,
            client: MinioClient,
    ):
        self.__client = client

    async def __call__(
            self,
            filename: str,
    ) -> str:

        return self.__client.presign_object('transactions', filename)
