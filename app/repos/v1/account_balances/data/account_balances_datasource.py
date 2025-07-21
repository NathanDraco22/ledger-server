from typing import Any
from typing_extensions import Self
from services.mongo_collections.v1 import AccountBalancesCollection


class AccountBalancesDataSource:
    def __new__(cls) -> Self:
        if not hasattr(cls, "instance"):
            cls.instance = super(cls, cls).__new__(cls)
        return cls.instance

    async def create_account_balance(self, account_balance: dict[str, Any]) -> dict[str, Any]:
        collection = AccountBalancesCollection()
        await collection.create_account_balance(account_balance)
        return account_balance

    async def get_all_account_balances(self) -> list[dict[str, Any]]:
        collection = AccountBalancesCollection()
        return await collection.fetch_all_account_balances()

    async def get_account_balance_by_id(self, account_balance_id: str) -> dict[str, Any] | None:
        collection = AccountBalancesCollection()
        return await collection.fetch_account_balance_by_id(account_balance_id)

    async def update_account_balance_by_id(
        self, account_balance_id: str, account_balance: dict[str, Any]
    ) -> dict[str, Any] | None:
        collection = AccountBalancesCollection()
        return await collection.update_account_balance_by_id(account_balance_id, account_balance)

    async def delete_account_balance_by_id(self, account_balance_id: str) -> dict[str, Any] | None:
        collection = AccountBalancesCollection()
        return await collection.delete_account_balance_by_id(account_balance_id)
