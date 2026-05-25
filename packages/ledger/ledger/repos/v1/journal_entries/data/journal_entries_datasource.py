from typing import Any
from ledger.services.mongo_collections.v1 import JournalEntriesCollection


class JournalEntriesDataSource:

    async def create_journal_entry(self, journal_entry: dict[str, Any]) -> dict[str, Any]:
        collection = JournalEntriesCollection.get_instance()
        await collection.create_journal_entry(journal_entry)
        return journal_entry

    async def get_all_journal_entries(self) -> list[dict[str, Any]]:
        collection = JournalEntriesCollection.get_instance()
        return await collection.fetch_all_journal_entries()

    async def get_journal_entry_by_id(self, journal_entry_id: str) -> dict[str, Any] | None:
        collection = JournalEntriesCollection.get_instance()
        return await collection.fetch_journal_entry_by_id(journal_entry_id)

    async def update_journal_entry_by_id(
        self, journal_entry_id: str, journal_entry: dict[str, Any]
    ) -> dict[str, Any] | None:
        collection = JournalEntriesCollection.get_instance()
        return await collection.update_journal_entry_by_id(journal_entry_id, journal_entry)

    async def delete_journal_entry_by_id(self, journal_entry_id: str) -> dict[str, Any] | None:
        collection = JournalEntriesCollection.get_instance()
        return await collection.delete_journal_entry_by_id(journal_entry_id)
