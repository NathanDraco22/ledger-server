from fastapi import APIRouter

from ledger.repos.v1.businesses import CreateBusiness, UpdateBusiness, BusinessInDb
from responses.v1.list_response import ListResponse

from .businesses_controller import businesses_controller


businesses_router = APIRouter(tags=["businessesV1"])


@businesses_router.post("")
async def create_business(body: CreateBusiness) -> BusinessInDb:
    return await businesses_controller.create_business(body)


@businesses_router.get("")
async def get_all_businesses() -> ListResponse[BusinessInDb]:
    return await businesses_controller.get_all_businesses()


@businesses_router.get("/{business_id}")
async def get_business_by_id(business_id: str) -> BusinessInDb:
    return await businesses_controller.get_business_by_id(business_id)


@businesses_router.patch("/{business_id}")
async def update_business_by_id(business_id: str, body: UpdateBusiness) -> BusinessInDb:
    return await businesses_controller.update_business_by_id(business_id, body)


@businesses_router.delete("/{business_id}")
async def delete_business_by_id(business_id: str) -> BusinessInDb:
    return await businesses_controller.delete_business_by_id(business_id)
