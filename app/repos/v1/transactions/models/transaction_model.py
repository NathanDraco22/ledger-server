from typing import Literal, Union, Annotated
from pydantic import BaseModel, Field


TransactionType = Literal["ENTRY", "EXIT"]


class BaseTransaction(BaseModel):
    accountId: str
    branchId: str
    quantity: int


class CreateExitTransaction(BaseTransaction):
    type: Literal["EXIT"] = "EXIT"
    quantity: int = Field(..., lt=0)


class CreateEntryTransaction(BaseTransaction):
    type: Literal["ENTRY"] = "ENTRY"
    quantity: int = Field(..., gt=0)


class TransactionInDb(BaseTransaction):
    id: str
    type: TransactionType
    createdAt: int


CreateTransaction = Annotated[
    Union[CreateExitTransaction, CreateEntryTransaction],
    Field(discriminator="type"),
]
