from fastapi import APIRouter

from ledger.repos.v1.account_transactions import AccountTransactionInDb
from responses.v1.list_response import ListResponse

from .account_transactions_controller import account_transactions_controller


account_transactions_router = APIRouter(tags=["account_transactionsV1"])


@account_transactions_router.get("")
async def get_all_account_transactions() -> ListResponse[AccountTransactionInDb]:
    return await account_transactions_controller.get_all_account_transactions()


@account_transactions_router.get("/{account_transaction_id}")
async def get_account_transaction_by_id(account_transaction_id: str) -> AccountTransactionInDb:
    return await account_transactions_controller.get_account_transaction_by_id(account_transaction_id)
