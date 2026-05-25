from pydantic import BaseModel


class BaseBusiness(BaseModel):
    name: str
    description: str = ""
    ownerId: str
    pass


class CreateBusiness(BaseBusiness):
    pass


class UpdateBusiness(BaseModel):
    name: str | None = None
    description: str | None = None
    ownerId: str | None = None


class BusinessInDb(BaseBusiness):
    id: str
    createdAt: int
    updatedAt: int | None = None
