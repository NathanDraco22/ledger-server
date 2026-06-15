from ledger.repos.v1.accounts import AccountsRepository, CreateAccount


def default_accounts_list(business_id: str) -> list[CreateAccount]:
    return [
        CreateAccount(
            businessId=business_id,
            name="Activos",
            type="debit",
            path=["1"],
            code="1",
            isDetail=False,
            description="Bienes y derechos propiedad de la entidad",
        ),
        CreateAccount(
            businessId=business_id,
            name="Pasivos",
            type="credit",
            path=["2"],
            code="2",
            isDetail=False,
            description="Deudas y obligaciones financieras con terceros",
        ),
        CreateAccount(
            businessId=business_id,
            name="Patrimonio",
            type="credit",
            path=["3"],
            code="3",
            isDetail=False,
            description="Valor residual tras deducir pasivos",
        ),
        CreateAccount(
            businessId=business_id,
            name="Ingresos",
            type="credit",
            path=["4"],
            code="4",
            isDetail=False,
            description="Entradas de recursos por ventas o servicios",
        ),
        CreateAccount(
            businessId=business_id,
            name="Egresos",
            type="debit",
            path=["5"],
            code="5",
            isDetail=False,
            description="Consumo de recursos necesarios para la operación",
        ),
    ]


async def default_accounts(business_id: str) -> None:
    repo = AccountsRepository.get_instance()

    for create in default_accounts_list(business_id):
        await repo.create_account(create)
