from typing import Any

from pymongo import ReturnDocument
from ledger.services import BaseMongoCollection


class BusinessesCollection(BaseMongoCollection):
    collection_name = "Businesses"

    async def create_business(self, business: dict) -> None:
        collection = self._collection
        await collection.insert_one(business)

    async def fetch_all_businesses(self) -> list[dict[str, Any]]:
        collection = self._collection
        cursor = collection.find()

        result = await cursor.to_list(length=None)
        await cursor.close()

        return result

    async def fetch_business_by_id(self, business_id: str) -> dict[str, Any] | None:
        collection = self._collection
        result = await collection.find_one({"id": business_id})
        return result

    async def update_business_by_id(
        self,
        business_id: str,
        business: dict,
    ) -> dict[str, Any] | None:
        collection = self._collection

        result = await collection.find_one_and_update(
            {"id": business_id},
            {"$set": business},
            return_document=ReturnDocument.AFTER,
        )

        return result

    async def delete_business_by_id(self, business_id: str) -> dict[str, Any] | None:
        collection = self._collection
        result = await collection.find_one_and_delete({"id": business_id})
        return result
