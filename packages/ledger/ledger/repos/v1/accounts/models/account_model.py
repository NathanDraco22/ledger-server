from typing import Literal
from pydantic import BaseModel

AccountType = Literal["credit", "debit"]
BaseAccountType = Literal["asset", "liability", "equity", "revenue", "expense"]


class BaseAccount(BaseModel):
    businessId: str
    name: str
    description: str = ""
    parentAccountId: str | None = None
    path: list[str]
    isDetail: bool = False
    currentBalance: int = 0
    type: AccountType
    baseType: BaseAccountType
    code: str = ""


class CreateAccount(BaseAccount):
    pass


class UpdateAccount(BaseModel):
    name: str | None = None
    description: str | None = None
    path: list[str] | None = None
    type: AccountType | None = None
    baseType: BaseAccountType | None = None
    code: str | None = None


class AccountInDb(BaseAccount):
    id: str
    createdAt: int
    updatedAt: int | None = None
