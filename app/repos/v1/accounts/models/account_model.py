from pydantic import BaseModel


class BaseAccount(BaseModel):
    pass


class CreateAccount(BaseAccount):
    pass


class UpdateAccount(BaseModel):
    pass


class AccountInDb(BaseAccount):
    id: str
    createdAt: int
    updatedAt: int | None = None
