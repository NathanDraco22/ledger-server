from fastapi import APIRouter

from .accounts.accounts_router import accounts_router

router_v1 = APIRouter(tags=["apiV1"])

router_v1.include_router(accounts_router, prefix='/accounts')

