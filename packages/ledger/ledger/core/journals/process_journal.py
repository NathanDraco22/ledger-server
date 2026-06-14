from ledger.repos.v1.journal_entries import CreateJournalEntry, JournalEntryInDb
from ledger.repos.v1.account_transactions.models.account_transaction_model import (
    AccountTransactionInDb,
)
from ledger.services import MongoService
from ledger.services.mongo_collections.v1 import (
    AccountsCollection,
    JournalEntriesCollection,
    AccountTransactionsCollection,
)
from ledger.tools import TimeTools, UuidTool

SIGN_FACTOR: dict[str, int] = {
    "asset": 1,
    "expense": 1,
    "liability": -1,
    "equity": -1,
    "revenue": -1,
}


async def process_journal(create_journal: CreateJournalEntry) -> JournalEntryInDb:
    mongo_client = MongoService().client
    journal_col = JournalEntriesCollection.get_instance()
    account_col = AccountsCollection.get_instance()
    tx_col = AccountTransactionsCollection.get_instance()

    time_now = TimeTools.get_now_in_milliseconds()

    async with mongo_client.start_session() as session:
        async with session.bind():
            async with await session.start_transaction():
                accounts_map: dict[str, dict] = {}

                for line in create_journal.lines:
                    account = await account_col.fetch_account_by_id(line.accountId)
                    if account is None:
                        raise ValueError(f"Account {line.accountId} not found")
                    if not account["isDetail"]:
                        raise ValueError(
                            f"Account {line.accountId} is not a detail account"
                        )
                    accounts_map[line.accountId] = account

                total = sum(
                    abs(line.amount)
                    * SIGN_FACTOR[accounts_map[line.accountId]["baseType"]]
                    for line in create_journal.lines
                )
                if total != 0:
                    raise ValueError("Journal entry does not balance")

                journal_entry = JournalEntryInDb(
                    **create_journal.model_dump(),
                    id=UuidTool.generate_uuid(),
                    createdAt=time_now,
                )
                await journal_col.create_journal_entry(journal_entry.model_dump())

                transactions = []

                for line in create_journal.lines:
                    account = accounts_map[line.accountId]

                    amount_to_add = (
                        abs(line.amount)
                        * SIGN_FACTOR[account["baseType"]]
                    )
                    new_balance = account["currentBalance"] + amount_to_add

                    await account_col.update_account_by_id(
                        line.accountId,
                        {
                            "currentBalance": new_balance,
                            "updatedAt": time_now,
                        },
                    )

                    transactions.append(
                        AccountTransactionInDb(
                            accountId=line.accountId,
                            journalId=journal_entry.id,
                            amount=amount_to_add,
                            resultBalance=new_balance,
                            id=UuidTool.generate_uuid(),
                            createdAt=time_now,
                        ).model_dump()
                    )

                if transactions:
                    await tx_col.create_many_transactions(transactions)

                return journal_entry
