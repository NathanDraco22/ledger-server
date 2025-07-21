from repos.v1.transactions import CreateEntryTransaction, CreateExitTransaction

from repos.v1.account_balances import AccountBalanceInDb

from services.mongo_collections.v1 import TransactionsCollection
from services.mongo_collections.v1 import AccountBalancesCollection
from services import MongoService

from tools import TimeTools


async def process_account_entry_transaction(
    entry: CreateEntryTransaction,
) -> AccountBalanceInDb:
    client = MongoService().client

    transaction_col = TransactionsCollection()
    account_balance_col = AccountBalancesCollection()

    async with await client.start_session() as session:
        async with session.start_transaction():
            result = await account_balance_col.update_account_balance_with_session(
                entry.accountId,
                entry.branchId,
                entry.quantity,
                updated_at=TimeTools.get_now_in_milliseconds(),
                session=session,
            )

            transaction_data = entry.model_dump()
            await transaction_col.create_transaction_with_session(
                transaction_data,
                session,
            )

            return AccountBalanceInDb.model_validate(result)


class InsufficientBalanceError(Exception):
    pass


async def process_account_exit_transaction(
    exit: CreateExitTransaction,
) -> AccountBalanceInDb:
    client = MongoService().client

    transaction_col = TransactionsCollection()
    account_balance_col = AccountBalancesCollection()

    async with await client.start_session() as session:
        async with session.start_transaction():
            result = await account_balance_col.subtract_account_balance_with_session(
                exit.accountId,
                exit.branchId,
                exit.quantity,
                updated_at=TimeTools.get_now_in_milliseconds(),
                session=session,
            )

            if result is None:
                raise InsufficientBalanceError()

            transaction_data = exit.model_dump()
            await transaction_col.create_transaction_with_session(
                transaction_data,
                session,
            )

            return AccountBalanceInDb.model_validate(result)
