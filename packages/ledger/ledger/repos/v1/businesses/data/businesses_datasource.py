from typing import Any
from ledger.services.mongo_collections.v1 import BusinessesCollection


class BusinessesDataSource:

    async def create_business(self, business: dict[str, Any]) -> dict[str, Any]:
        collection = BusinessesCollection.get_instance()
        await collection.create_business(business)
        return business

    async def get_all_businesses(self) -> list[dict[str, Any]]:
        collection = BusinessesCollection.get_instance()
        return await collection.fetch_all_businesses()

    async def get_business_by_id(self, business_id: str) -> dict[str, Any] | None:
        collection = BusinessesCollection.get_instance()
        return await collection.fetch_business_by_id(business_id)

    async def update_business_by_id(
        self, business_id: str, business: dict[str, Any]
    ) -> dict[str, Any] | None:
        collection = BusinessesCollection.get_instance()
        return await collection.update_business_by_id(business_id, business)

    async def delete_business_by_id(self, business_id: str) -> dict[str, Any] | None:
        collection = BusinessesCollection.get_instance()
        return await collection.delete_business_by_id(business_id)
