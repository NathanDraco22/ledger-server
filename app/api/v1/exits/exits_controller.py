from repos.v1.transactions import CreateExitTransaction
from repos.v1.account_balances import AccountBalanceInDb
from core.ledge.ledge_manager import LedgerManager


class ExitsController:
    def __init__(self, ledge_manager: LedgerManager):
        self.ledge_manager = ledge_manager

    async def create_exit(self, body: CreateExitTransaction) -> AccountBalanceInDb:
        return await self.ledge_manager.create_exit(body)


exits_controller = ExitsController(
    ledge_manager=LedgerManager(),
)
