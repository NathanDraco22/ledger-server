from typing import Literal
from pydantic import BaseModel

AccountType = Literal["credit", "debit"]


class BaseAccount(BaseModel):
    businessId: str
    name: str
    description: str = ""
    parentAccountId: str | None = None
    accountIndexPath: list[str]
    isTransactionAccount: bool = False
    balance: int = 0
    type: AccountType


class CreateAccount(BaseAccount):
    pass


class UpdateAccount(BaseModel):
    name: str | None = None
    description: str | None = None
    accountIndexPath: list[str] | None = None
    type: AccountType | None = None


class AccountInDb(BaseAccount):
    id: str
    createdAt: int
    updatedAt: int | None = None
