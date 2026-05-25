from fastapi import APIRouter

from ledger.repos.v1.journal_entries import CreateJournalEntry, JournalEntryInDb
from responses.v1.list_response import ListResponse

from .journal_entries_controller import journal_entries_controller


journal_entries_router = APIRouter(tags=["journal_entriesV1"])


@journal_entries_router.post("")
async def create_journal_entry(body: CreateJournalEntry) -> JournalEntryInDb:
    return await journal_entries_controller.create_journal_entry(body)


@journal_entries_router.get("")
async def get_all_journal_entries() -> ListResponse[JournalEntryInDb]:
    return await journal_entries_controller.get_all_journal_entries()


@journal_entries_router.get("/{journal_entry_id}")
async def get_journal_entry_by_id(journal_entry_id: str) -> JournalEntryInDb:
    return await journal_entries_controller.get_journal_entry_by_id(journal_entry_id)
