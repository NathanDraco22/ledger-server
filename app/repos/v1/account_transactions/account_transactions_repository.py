from .data.account_transactions_datasource import AccountTransactionsDataSource
from .models.account_transaction_model import CreateAccountTransaction, UpdateAccountTransaction, AccountTransactionInDb

from tools import TimeTools, UuidTool


class AccountTransactionsRepository:
    
    _instance: "AccountTransactionsRepository|None" = None
    
    def __init__(self, account_transactions_ds: AccountTransactionsDataSource):
        self.account_transactions_ds = account_transactions_ds

    @classmethod
    def get_instance(cls) -> "AccountTransactionsRepository":
        if cls._instance is None:
            cls._instance = cls(AccountTransactionsDataSource())
        return cls._instance

    async def create_account_transaction(self, create_account_transaction: CreateAccountTransaction) -> AccountTransactionInDb:
        new_account_transaction_in_db = AccountTransactionInDb(
            **create_account_transaction.model_dump(),
            id=UuidTool.generate_uuid(),
            createdAt=TimeTools.get_now_in_milliseconds(),
        )

        await self.account_transactions_ds.create_account_transaction(new_account_transaction_in_db.model_dump())

        return new_account_transaction_in_db

    async def get_all_account_transactions(self) -> list[AccountTransactionInDb]:
        results = await self.account_transactions_ds.get_all_account_transactions()
        models = [AccountTransactionInDb.model_validate(result) for result in results]
        return models

    async def get_account_transaction_by_id(self, account_transaction_id: str) -> AccountTransactionInDb | None :
        result = await self.account_transactions_ds.get_account_transaction_by_id(account_transaction_id)
        
        if result is None:
            return None
        
        return AccountTransactionInDb.model_validate(result)

    async def update_account_transaction_by_id(self, account_transaction_id: str, account_transaction: UpdateAccountTransaction) -> AccountTransactionInDb | None:
        account_transaction_data = account_transaction.model_dump(exclude_unset=True)

        account_transaction_data["updatedAt"] = TimeTools.get_now_in_milliseconds()

        result = await self.account_transactions_ds.update_account_transaction_by_id(account_transaction_id, account_transaction_data)

        if result is None:
            return None

        return AccountTransactionInDb.model_validate(result)

    async def delete_account_transaction_by_id(self, account_transaction_id: str) -> AccountTransactionInDb | None:
        result = await self.account_transactions_ds.delete_account_transaction_by_id(account_transaction_id)
        
        if result is None:
            return None
        
        return AccountTransactionInDb.model_validate(result)
