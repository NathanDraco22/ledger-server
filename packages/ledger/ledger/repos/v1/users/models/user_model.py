from pydantic import BaseModel


class BusinessRef(BaseModel):
    businessId: str
    isOwner: bool = False


class BaseUser(BaseModel):
    name: str
    lastName: str
    cardId: str
    phoneNumber: str
    email: str
    password: str
    businesses: list[BusinessRef]


class CreateUser(BaseUser):
    pass


class UpdateUser(BaseModel):
    pass


class UserInDb(BaseUser):
    id: str
    createdAt: int
    updatedAt: int | None = None
