from .data.accounts_datasource import AccountsDataSource
from .models.account_model import CreateAccount, UpdateAccount, AccountInDb

from tools import TimeTools, UuidTool


class AccountsRepository:
    
    _instance: "AccountsRepository|None" = None
    
    def __init__(self, accounts_ds: AccountsDataSource):
        self.accounts_ds = accounts_ds

    @classmethod
    def get_instance(cls) -> "AccountsRepository":
        if cls._instance is None:
            cls._instance = cls(AccountsDataSource())
        return cls._instance

    async def create_account(self, create_account: CreateAccount) -> AccountInDb:
        new_account_in_db = AccountInDb(
            **create_account.model_dump(),
            id=UuidTool.generate_uuid(),
            createdAt=TimeTools.get_now_in_milliseconds(),
        )

        await self.accounts_ds.create_account(new_account_in_db.model_dump())

        return new_account_in_db

    async def get_all_accounts(self) -> list[AccountInDb]:
        results = await self.accounts_ds.get_all_accounts()
        models = [AccountInDb.model_validate(result) for result in results]
        return models

    async def get_account_by_id(self, account_id: str) -> AccountInDb | None :
        result = await self.accounts_ds.get_account_by_id(account_id)
        
        if result is None:
            return None
        
        return AccountInDb.model_validate(result)

    async def update_account_by_id(self, account_id: str, account: UpdateAccount) -> AccountInDb | None:
        account_data = account.model_dump(exclude_unset=True)

        account_data["updatedAt"] = TimeTools.get_now_in_milliseconds()

        result = await self.accounts_ds.update_account_by_id(account_id, account_data)

        if result is None:
            return None

        return AccountInDb.model_validate(result)

    async def delete_account_by_id(self, account_id: str) -> AccountInDb | None:
        result = await self.accounts_ds.delete_account_by_id(account_id)
        
        if result is None:
            return None
        
        return AccountInDb.model_validate(result)
