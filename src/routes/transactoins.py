from fastapi import APIRouter
from starlette.requests import Request

from depends import GenerateLoadTransactionFileUrlQueryDeps, AddTransactionsFromS3FileCommandDepends, \
    AddTransactionsCommandDeps
from schemas.transaction import Transaction, TransactionEntity

router = APIRouter(
    prefix='/transactions',
    tags=['transactions'],
)


@router.post('/manual')
async def add_transactions_manually(
        transactions: list[Transaction],
        command: AddTransactionsCommandDeps
) -> list[TransactionEntity]:
    return command(transactions)


@router.get('/file')
async def get_upload_file(
        filename: str,
        query: GenerateLoadTransactionFileUrlQueryDeps,
) -> str:
    return await query(filename)


@router.post('/file')
async def add_transactions_from_file(
        request: Request,
        command: AddTransactionsFromS3FileCommandDepends,
) -> None:
    body = await request.json()
    await command(body['Key'])
