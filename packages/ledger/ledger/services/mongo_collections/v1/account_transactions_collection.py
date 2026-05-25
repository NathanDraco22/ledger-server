from typing import Any

from pymongo import ReturnDocument
from ledger.services import BaseMongoCollection


class AccountTransactionsCollection(BaseMongoCollection):
    collection_name = "AccountTransactions"

    async def create_account_transaction(self, account_transaction: dict) -> None:
        collection = self._collection
        await collection.insert_one(account_transaction)

    async def fetch_all_account_transactions(self) -> list[dict[str, Any]]:
        collection = self._collection
        cursor = collection.find()

        result = await cursor.to_list(length=None)
        await cursor.close()

        return result

    async def fetch_account_transaction_by_id(self, account_transaction_id: str) -> dict[str, Any] | None:
        collection = self._collection
        result = await collection.find_one({"id": account_transaction_id})
        return result

    async def update_account_transaction_by_id(
        self,
        account_transaction_id: str,
        account_transaction: dict,
    ) -> dict[str, Any] | None:
        collection = self._collection

        result = await collection.find_one_and_update(
            {"id": account_transaction_id},
            {"$set": account_transaction},
            return_document=ReturnDocument.AFTER,
        )

        return result

    async def delete_account_transaction_by_id(self, account_transaction_id: str) -> dict[str, Any] | None:
        collection = self._collection
        result = await collection.find_one_and_delete({"id": account_transaction_id})
        return result
