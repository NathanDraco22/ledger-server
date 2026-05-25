from pydantic import BaseModel


class BaseBranch(BaseModel):
    businessId: str
    name: str
    description: str = ""
    idCard: str = ""
    address: str = ""
    email: str = ""
    phone: str = ""
    image: str = ""


class CreateBranch(BaseBranch):
    pass


class UpdateBranch(BaseModel):
    name: str | None = None
    idCard: str | None = None
    address: str | None = None
    email: str | None = None
    phone: str | None = None
    description: str | None = None
    image: str | None = None


class BranchInDb(BaseBranch):
    id: str
    createdAt: int
    updatedAt: int | None = None
