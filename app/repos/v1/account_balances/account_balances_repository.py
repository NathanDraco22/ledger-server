from .data.account_balances_datasource import AccountBalancesDataSource
from .models.account_balance_model import (
    CreateAccountBalance,
    UpdateAccountBalance,
    AccountBalanceInDb,
)


class AccountBalancesRepository:
    def __init__(self, account_balances_ds: AccountBalancesDataSource):
        self.account_balances_ds = account_balances_ds

    async def create_account_balance(
        self, create_account_balance: CreateAccountBalance
    ) -> AccountBalanceInDb:
        # TODO: implement create
        raise NotImplementedError()

    async def get_all_account_balances(self) -> list[AccountBalanceInDb]:
        results = await self.account_balances_ds.get_all_account_balances()
        models = [AccountBalanceInDb.model_validate(result) for result in results]
        return models

    async def get_account_balance_by_id(
        self, account_balance_id: str
    ) -> AccountBalanceInDb | None:
        result = await self.account_balances_ds.get_account_balance_by_id(
            account_balance_id
        )

        if result is None:
            return None

        return AccountBalanceInDb.model_validate(result)

    async def update_account_balance_by_id(
        self, account_balance_id: str, account_balance: UpdateAccountBalance
    ) -> AccountBalanceInDb | None:
        # TODO: implement update
        raise NotImplementedError()
