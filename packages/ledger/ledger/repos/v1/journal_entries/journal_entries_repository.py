from .data.journal_entries_datasource import JournalEntriesDataSource
from .models.journal_entry_model import CreateJournalEntry, UpdateJournalEntry, JournalEntryInDb

from ledger.tools import TimeTools, UuidTool


class JournalEntriesRepository:
    
    _instance: "JournalEntriesRepository|None" = None
    
    def __init__(self, journal_entries_ds: JournalEntriesDataSource):
        self.journal_entries_ds = journal_entries_ds

    @classmethod
    def get_instance(cls) -> "JournalEntriesRepository":
        if cls._instance is None:
            cls._instance = cls(JournalEntriesDataSource())
        return cls._instance

    async def create_journal_entry(self, create_journal_entry: CreateJournalEntry) -> JournalEntryInDb:
        new_journal_entry_in_db = JournalEntryInDb(
            **create_journal_entry.model_dump(),
            id=UuidTool.generate_uuid(),
            createdAt=TimeTools.get_now_in_milliseconds(),
        )

        await self.journal_entries_ds.create_journal_entry(new_journal_entry_in_db.model_dump())

        return new_journal_entry_in_db

    async def get_all_journal_entries(self) -> list[JournalEntryInDb]:
        results = await self.journal_entries_ds.get_all_journal_entries()
        models = [JournalEntryInDb.model_validate(result) for result in results]
        return models

    async def get_journal_entry_by_id(self, journal_entry_id: str) -> JournalEntryInDb | None :
        result = await self.journal_entries_ds.get_journal_entry_by_id(journal_entry_id)
        
        if result is None:
            return None
        
        return JournalEntryInDb.model_validate(result)

    async def update_journal_entry_by_id(self, journal_entry_id: str, journal_entry: UpdateJournalEntry) -> JournalEntryInDb | None:
        # TODO: implement update
        raise NotImplementedError()

    async def delete_journal_entry_by_id(self, journal_entry_id: str) -> JournalEntryInDb | None:
        # TODO: implement delete
        raise NotImplementedError()
