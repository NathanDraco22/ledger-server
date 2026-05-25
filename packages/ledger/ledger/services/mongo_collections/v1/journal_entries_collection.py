from typing import Any

from pymongo import ReturnDocument
from ledger.services import BaseMongoCollection


class JournalEntriesCollection(BaseMongoCollection):
    collection_name = "JournalEntries"

    async def create_journal_entry(self, journal_entry: dict) -> None:
        collection = self._collection
        await collection.insert_one(journal_entry)

    async def fetch_all_journal_entries(self) -> list[dict[str, Any]]:
        collection = self._collection
        cursor = collection.find()

        result = await cursor.to_list(length=None)
        await cursor.close()

        return result

    async def fetch_journal_entry_by_id(self, journal_entry_id: str) -> dict[str, Any] | None:
        collection = self._collection
        result = await collection.find_one({"id": journal_entry_id})
        return result

    async def update_journal_entry_by_id(
        self,
        journal_entry_id: str,
        journal_entry: dict,
    ) -> dict[str, Any] | None:
        collection = self._collection

        result = await collection.find_one_and_update(
            {"id": journal_entry_id},
            {"$set": journal_entry},
            return_document=ReturnDocument.AFTER,
        )

        return result

    async def delete_journal_entry_by_id(self, journal_entry_id: str) -> dict[str, Any] | None:
        collection = self._collection
        result = await collection.find_one_and_delete({"id": journal_entry_id})
        return result
