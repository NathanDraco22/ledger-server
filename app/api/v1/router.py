from fastapi import APIRouter

from .accounts.accounts_router import accounts_router
from .branches.branches_router import branches_router
from .units.units_router import units_router

router_v1 = APIRouter(tags=["apiV1"])

router_v1.include_router(accounts_router, prefix="/accounts")
router_v1.include_router(branches_router, prefix='/branches')
router_v1.include_router(units_router, prefix='/units')

