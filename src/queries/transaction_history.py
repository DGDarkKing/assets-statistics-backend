from schemas.transaction_filter import TransactionFilter


class TransactionHistoryQuery:
    async def __call__(
            self,
            filter: TransactionFilter
    ):
