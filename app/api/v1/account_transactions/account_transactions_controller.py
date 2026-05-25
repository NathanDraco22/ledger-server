from fastapi import HTTPException, status

from responses.v1.list_response import ListResponse
from ledger.repos.v1.account_transactions import (
    CreateAccountTransaction, 
    AccountTransactionInDb, 
    AccountTransactionsRepository,
)


class AccountTransactionsController:
    def __init__(self, account_transactions_repo: AccountTransactionsRepository) -> None:
        self.account_transactions_repo = account_transactions_repo

    async def create_account_transaction(self, body: CreateAccountTransaction) -> AccountTransactionInDb:
        return await self.account_transactions_repo.create_account_transaction(body)

    async def get_all_account_transactions(self) -> ListResponse[AccountTransactionInDb]:
        account_transactions = await self.account_transactions_repo.get_all_account_transactions()
        return ListResponse(data=account_transactions, count=len(account_transactions))

    async def get_account_transaction_by_id(self, account_transaction_id: str) -> AccountTransactionInDb:
        account_transaction = await self.account_transactions_repo.get_account_transaction_by_id(account_transaction_id)
        if account_transaction is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AccountTransaction not found",
            )
        return account_transaction


account_transactions_controller = AccountTransactionsController(
    account_transactions_repo=AccountTransactionsRepository.get_instance(),
)
