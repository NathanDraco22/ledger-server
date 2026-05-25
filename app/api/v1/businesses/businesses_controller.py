from fastapi import HTTPException, status

from responses.v1.list_response import ListResponse
from ledger.repos.v1.businesses import (
    CreateBusiness,
    UpdateBusiness,
    BusinessInDb,
    BusinessesRepository,
)


class BusinessesController:
    def __init__(self, businesses_repo: BusinessesRepository) -> None:
        self.businesses_repo = businesses_repo

    async def create_business(self, body: CreateBusiness) -> BusinessInDb:
        return await self.businesses_repo.create_business(body)

    async def get_all_businesses(self) -> ListResponse[BusinessInDb]:
        businesses = await self.businesses_repo.get_all_businesses()
        return ListResponse(data=businesses, count=len(businesses))

    async def get_business_by_id(self, business_id: str) -> BusinessInDb:
        business = await self.businesses_repo.get_business_by_id(business_id)
        if business is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found",
            )
        return business

    async def update_business_by_id(self, business_id: str, body: UpdateBusiness) -> BusinessInDb:
        updated_business = await self.businesses_repo.update_business_by_id(business_id, body)
        if updated_business is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found",
            )
        return updated_business

    async def delete_business_by_id(self, business_id: str) -> BusinessInDb:
        deleted_business = await self.businesses_repo.delete_business_by_id(business_id)
        if deleted_business is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found",
            )
        return deleted_business


businesses_controller = BusinessesController(
    businesses_repo=BusinessesRepository.get_instance(),
)
