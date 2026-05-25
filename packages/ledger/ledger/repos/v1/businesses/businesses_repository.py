from .data.businesses_datasource import BusinessesDataSource
from .models.business_model import CreateBusiness, UpdateBusiness, BusinessInDb

from ledger.tools import TimeTools, UuidTool


class BusinessesRepository:
    _instance: "BusinessesRepository|None" = None

    def __init__(self, businesses_ds: BusinessesDataSource):
        self.businesses_ds = businesses_ds

    @classmethod
    def get_instance(cls) -> "BusinessesRepository":
        if cls._instance is None:
            cls._instance = cls(BusinessesDataSource())
        return cls._instance

    async def create_business(self, create_business: CreateBusiness) -> BusinessInDb:
        new_business_in_db = BusinessInDb(
            **create_business.model_dump(),
            id=UuidTool.generate_uuid(),
            createdAt=TimeTools.get_now_in_milliseconds(),
        )

        await self.businesses_ds.create_business(new_business_in_db.model_dump())

        return new_business_in_db

    async def get_all_businesses(self) -> list[BusinessInDb]:
        results = await self.businesses_ds.get_all_businesses()
        models = [BusinessInDb.model_validate(result) for result in results]
        return models

    async def get_business_by_id(self, business_id: str) -> BusinessInDb | None:
        result = await self.businesses_ds.get_business_by_id(business_id)

        if result is None:
            return None

        return BusinessInDb.model_validate(result)

    async def update_business_by_id(
        self, business_id: str, business: UpdateBusiness
    ) -> BusinessInDb | None:

        business_data = business.model_dump(exclude_unset=True)

        business_data["updatedAt"] = TimeTools.get_now_in_milliseconds()

        result = await self.businesses_ds.update_business_by_id(business_id, business_data)

        if result is None:
            return None

        return BusinessInDb.model_validate(result)

    async def delete_business_by_id(self, business_id: str) -> BusinessInDb | None:
        result = await self.businesses_ds.delete_business_by_id(business_id)

        if result is None:
            return None

        return BusinessInDb.model_validate(result)
