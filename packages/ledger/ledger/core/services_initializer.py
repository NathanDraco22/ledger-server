from ledger.services import MongoService


async def ledger_init_services() -> None:
    await MongoService().init_service()
    pass
