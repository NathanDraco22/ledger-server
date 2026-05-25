from fastapi import APIRouter

from .account_transactions.account_transactions_router import account_transactions_router
from .accounts.accounts_router import accounts_router
from .branches.branches_router import branches_router
from .businesses.businesses_router import businesses_router
from .users.users_router import users_router

router_v1 = APIRouter(tags=["apiV1"])

router_v1.include_router(account_transactions_router, prefix='/account-transactions')
router_v1.include_router(accounts_router, prefix='/accounts')
router_v1.include_router(branches_router, prefix='/branches')
router_v1.include_router(businesses_router, prefix='/businesses')
router_v1.include_router(users_router, prefix='/users')

