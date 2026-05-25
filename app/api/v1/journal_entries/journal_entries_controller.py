from fastapi import HTTPException, status

from responses.v1.list_response import ListResponse
from ledger.repos.v1.journal_entries import (
    CreateJournalEntry,
    JournalEntryInDb,
    JournalEntriesRepository,
)


class JournalEntriesController:
    def __init__(self, journal_entries_repo: JournalEntriesRepository) -> None:
        self.journal_entries_repo = journal_entries_repo

    async def create_journal_entry(self, body: CreateJournalEntry) -> JournalEntryInDb:
        return await self.journal_entries_repo.create_journal_entry(body)

    async def get_all_journal_entries(self) -> ListResponse[JournalEntryInDb]:
        journal_entries = await self.journal_entries_repo.get_all_journal_entries()
        return ListResponse(data=journal_entries, count=len(journal_entries))

    async def get_journal_entry_by_id(self, journal_entry_id: str) -> JournalEntryInDb:
        journal_entry = await self.journal_entries_repo.get_journal_entry_by_id(journal_entry_id)
        if journal_entry is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="JournalEntry not found",
            )
        return journal_entry


journal_entries_controller = JournalEntriesController(
    journal_entries_repo=JournalEntriesRepository.get_instance(),
)
