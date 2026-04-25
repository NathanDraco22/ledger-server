from fastapi import APIRouter

from .account_transactions.account_transactions_router import account_transactions_router
from .accounts.accounts_router import accounts_router

router_v1 = APIRouter(tags=["apiV1"])

router_v1.include_router(account_transactions_router, prefix='/account-transactions')
router_v1.include_router(accounts_router, prefix='/accounts')

