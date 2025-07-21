from fastapi import APIRouter

from .entries_controller import entries_controller

from repos.v1.transactions import CreateEntryTransaction
from repos.v1.account_balances import AccountBalanceInDb

entries_router = APIRouter(tags=["entriesV1"])


@entries_router.post("")
async def create_entry(
    create_entry: CreateEntryTransaction,
) -> AccountBalanceInDb:
    return await entries_controller.create_entry(create_entry)
