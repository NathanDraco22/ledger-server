from repos.v1.transactions import CreateEntryTransaction
from repos.v1.account_balances import AccountBalanceInDb
from core.ledge.ledge_manager import LedgerManager


class EntriesController:
    def __init__(self, ledge_manager: LedgerManager) -> None:
        self.ledge_manager = ledge_manager
        pass

    async def create_entry(self, body: CreateEntryTransaction) -> AccountBalanceInDb:
        return await self.ledge_manager.create_entry(body)


entries_controller = EntriesController(ledge_manager=LedgerManager())
