from ledger.repos.v1.accounts import AccountsRepository, CreateAccount


DEFAULT_ACCOUNTS: list[dict] = [
    {
        "name": "Activos",
        "baseType": "asset",
        "type": "debit",
        "path": ["1"],
        "code": "1",
        "isDetail": False,
        "description": "Bienes y derechos propiedad de la entidad",
    },
    {
        "name": "Pasivos",
        "baseType": "liability",
        "type": "credit",
        "path": ["2"],
        "code": "2",
        "isDetail": False,
        "description": "Deudas y obligaciones financieras con terceros",
    },
    {
        "name": "Patrimonio",
        "baseType": "equity",
        "type": "credit",
        "path": ["3"],
        "code": "3",
        "isDetail": False,
        "description": "Valor residual tras deducir pasivos",
    },
    {
        "name": "Ingresos",
        "baseType": "revenue",
        "type": "credit",
        "path": ["4"],
        "code": "4",
        "isDetail": False,
        "description": "Entradas de recursos por ventas o servicios",
    },
    {
        "name": "Egresos",
        "baseType": "expense",
        "type": "debit",
        "path": ["5"],
        "code": "5",
        "isDetail": False,
        "description": "Consumo de recursos necesarios para la operación",
    },
]


async def default_accounts(business_id: str) -> None:
    repo = AccountsRepository.get_instance()

    for account_data in DEFAULT_ACCOUNTS:
        create = CreateAccount(businessId=business_id, **account_data)
        await repo.create_account(create)
