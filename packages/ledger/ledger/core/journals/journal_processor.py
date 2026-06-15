from ledger.repos.v1.journal_entries import CreateJournalEntry, JournalEntryInDb
from .process_journal import process_journal


class JournalProcessor:
    _instance: "JournalProcessor|None" = None

    @classmethod
    def get_instance(cls) -> "JournalProcessor":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def create_journal(
        self, create_journal: CreateJournalEntry
    ) -> JournalEntryInDb:
        return await process_journal(create_journal)
