from pydantic import BaseModel


class BaseAccountTransaction(BaseModel):
    pass


class CreateAccountTransaction(BaseAccountTransaction):
    pass


class UpdateAccountTransaction(BaseModel):
    pass


class AccountTransactionInDb(BaseAccountTransaction):
    id: str
    created_at: str
    updated_at: str
