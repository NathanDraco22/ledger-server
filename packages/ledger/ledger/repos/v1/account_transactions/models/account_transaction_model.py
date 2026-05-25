from pydantic import BaseModel


class BaseAccountTransaction(BaseModel):
    accountId: str
    journalId: str
    amount: int
    resultBalance: int


class CreateAccountTransaction(BaseAccountTransaction):
    pass


class UpdateAccountTransaction(BaseModel):
    pass


class AccountTransactionInDb(BaseAccountTransaction):
    id: str
    createdAt: int
    updatedAt: int | None = None
