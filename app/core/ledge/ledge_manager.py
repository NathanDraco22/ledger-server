import asyncio
from fastapi import HTTPException, status

from pymongo.errors import OperationFailure

from repos.v1.accounts import AccountsRepository, AccountsDataSource
from repos.v1.branches import BranchesRepository, BranchesDataSource
from repos.v1.account_balances import AccountBalanceInDb
from repos.v1.transactions import (
    CreateEntryTransaction,
)

from .db_transactions import process_account_entry_transaction


class LedgeManager:
    def __init__(self):
        self.accounts_repository = AccountsRepository(AccountsDataSource())
        self.branches_repository = BranchesRepository(BranchesDataSource())

    async def create_entry(
        self,
        create_entry_transaction: CreateEntryTransaction,
    ) -> AccountBalanceInDb:
        account = await self.accounts_repository.get_account_by_id(
            create_entry_transaction.accountId
        )

        if account is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found",
            )

        branch = await self.branches_repository.get_branch_by_id(
            create_entry_transaction.branchId
        )

        if branch is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Branch not found",
            )

        max_retries = 3

        for _ in range(max_retries):
            try:
                result = await process_account_entry_transaction(
                    create_entry_transaction
                )
                return result

            except OperationFailure as e:
                if e.code == 112:
                    await asyncio.sleep(0.3)
                    continue

                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Error processing account entry transaction \n" + str(e),
                    )

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error processing account entry transaction \n" + str(e),
                )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server is too busy, try again later",
        )

    async def create_exit(self, exit):
        pass
