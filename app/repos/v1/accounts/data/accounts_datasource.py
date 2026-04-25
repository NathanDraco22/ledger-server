from typing import Any
from services.mongo_collections.v1 import AccountsCollection


class AccountsDataSource:
    async def create_account(self, account: dict[str, Any]) -> dict[str, Any]:
        collection = AccountsCollection()
        await collection.create_account(account)
        return account

    async def get_all_accounts(self) -> list[dict[str, Any]]:
        collection = AccountsCollection()
        return await collection.fetch_all_accounts()

    async def get_account_by_id(self, account_id: str) -> dict[str, Any] | None:
        collection = AccountsCollection()
        return await collection.fetch_account_by_id(account_id)

    async def update_account_by_id(
        self, account_id: str, account: dict[str, Any]
    ) -> dict[str, Any] | None:
        collection = AccountsCollection()
        return await collection.update_account_by_id(account_id, account)

    async def delete_account_by_id(self, account_id: str) -> dict[str, Any] | None:
        collection = AccountsCollection()
        return await collection.delete_account_by_id(account_id)
