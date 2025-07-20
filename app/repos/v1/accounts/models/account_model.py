from pydantic import BaseModel


class BaseAccount(BaseModel):
    name: str
    unitId: str
    isActive: bool = True


class CreateAccount(BaseAccount):
    pass


class UpdateAccount(BaseModel):
    name: str | None = None
    isActive: bool | None = None


class AccountInDb(BaseAccount):
    id: str
    created_at: int
    updated_at: int | None = None
