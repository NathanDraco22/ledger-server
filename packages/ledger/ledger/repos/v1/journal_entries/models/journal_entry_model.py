from pydantic import BaseModel


class JournalLine(BaseModel):
    branchId: str | None = None
    accountId: str
    amount: int
    description: str
    pass


class BaseJournalEntry(BaseModel):
    businessId: str
    date: int
    description: str
    docNumber: str
    reference: str
    dateId: str
    lines: list[JournalLine]


class CreateJournalEntry(BaseJournalEntry):
    pass


class UpdateJournalEntry(BaseModel):
    pass


class JournalEntryInDb(BaseJournalEntry):
    id: str
    createdAt: int
    updatedAt: int | None = None
