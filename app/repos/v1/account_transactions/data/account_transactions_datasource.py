from typing import Any
from services.mongo_collections.v1 import AccountTransactionsCollection


class AccountTransactionsDataSource:

    async def create_account_transaction(self, account_transaction: dict[str, Any]) -> dict[str, Any]:
        collection = AccountTransactionsCollection()
        await collection.create_account_transaction(account_transaction)
        return account_transaction

    async def get_all_account_transactions(self) -> list[dict[str, Any]]:
        collection = AccountTransactionsCollection()
        return await collection.fetch_all_account_transactions()

    async def get_account_transaction_by_id(self, account_transaction_id: str) -> dict[str, Any] | None:
        collection = AccountTransactionsCollection()
        return await collection.fetch_account_transaction_by_id(account_transaction_id)

    async def update_account_transaction_by_id(
        self, account_transaction_id: str, account_transaction: dict[str, Any]
    ) -> dict[str, Any] | None:
        collection = AccountTransactionsCollection()
        return await collection.update_account_transaction_by_id(account_transaction_id, account_transaction)

    async def delete_account_transaction_by_id(self, account_transaction_id: str) -> dict[str, Any] | None:
        collection = AccountTransactionsCollection()
        return await collection.delete_account_transaction_by_id(account_transaction_id)
