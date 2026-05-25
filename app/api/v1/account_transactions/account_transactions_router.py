from fastapi import APIRouter

from ledger.repos.v1.account_transactions import CreateAccountTransaction, UpdateAccountTransaction, AccountTransactionInDb
from responses.v1.list_response import ListResponse

from .account_transactions_controller import account_transactions_controller


account_transactions_router = APIRouter(tags=["account_transactionsV1"])


@account_transactions_router.post("")
async def create_account_transaction(body: CreateAccountTransaction) -> AccountTransactionInDb:
    return await account_transactions_controller.create_account_transaction(body)


@account_transactions_router.get("")
async def get_all_account_transactions() -> ListResponse[AccountTransactionInDb]:
    return await account_transactions_controller.get_all_account_transactions()


@account_transactions_router.get("/{account_transaction_id}")
async def get_account_transaction_by_id(account_transaction_id: str) -> AccountTransactionInDb:
    return await account_transactions_controller.get_account_transaction_by_id(account_transaction_id)


@account_transactions_router.patch("/{account_transaction_id}")
async def update_account_transaction_by_id(account_transaction_id: str, body: UpdateAccountTransaction) -> AccountTransactionInDb: 
    return await account_transactions_controller.update_account_transaction_by_id(account_transaction_id, body)


@account_transactions_router.delete("/{account_transaction_id}")
async def delete_account_transaction_by_id(account_transaction_id: str) -> AccountTransactionInDb:
    return await account_transactions_controller.delete_account_transaction_by_id(account_transaction_id)
