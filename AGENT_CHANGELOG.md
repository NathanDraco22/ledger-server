# AGENT CHANGELOG

## [2026-06-13] Implementación del procesador de journals

### Archivos modificados

- **`packages/ledger/ledger/core/journals/process_journal.py`**
  - Implementada la lógica transaccional completa de `process_journal()`.
  - Dentro de una transacción de MongoDB (con `session.bind()` de PyMongo 4.17):
    1. Inserta el documento `JournalEntryInDb` con UUID y timestamp.
    2. Por cada línea del asiento: actualiza el balance de la cuenta contable (`balance` + `amount` si la cuenta es débito, o `balance` - `amount` si es crédito).
    3. Construye todos los `AccountTransactionInDb` y los inserta en batch con `create_many_transactions()`.

- **`app/api/v1/journal_entries/journal_entries_controller.py`**
  - El método `create_journal_entry` ahora delega en `JournalProcessor.create_journal()` en lugar de llamar directamente al repositorio.

- **`packages/ledger/ledger/services/mongo_collections/v1/account_transactions_collection.py`**
  - Agregado método `create_many_transactions()` que usa `insert_many()` para inserción batch.

- **`app/api/v1/account_transactions/account_transactions_router.py`**
  - Eliminado el endpoint `POST /account-transactions` para que las transacciones solo se creen a través del proceso de journals.

- **`app/api/v1/account_transactions/account_transactions_controller.py`**
  - Eliminado el método `create_account_transaction` por la misma razón.

## [2026-06-13] Migración del modelo Account, validaciones y campo date

### P3 — Migración del modelo Account
- **`packages/ledger/ledger/repos/v1/accounts/models/account_model.py`**
  - Agregado `baseType` (asset, liability, equity, revenue, expense)
  - Agregado `code` (código contable)
  - Renombrado `isTransactionAccount` → `isDetail`
  - Renombrado `balance` → `currentBalance`
  - Renombrado `accountIndexPath` → `path`

- **`ledger_front/lib/src/domain/models/account_model/account_model.dart`**
  - Misma migración que el backend

### P4 — Validaciones en process_journal
- **`packages/ledger/ledger/core/journals/process_journal.py`**
  - **Leaf Node Validation**: antes de procesar, verifica que todas las cuentas
    tengan `isDetail == true`. Rechaza si alguna no es hoja.
  - **Zero Sum Validation**: calcula `sum(abs(amount) * sign_factor)` usando el
    mapa de signos (+ para asset/expense, - para liability/equity/revenue).
    Rechaza si la suma no es cero.
  - Actualizado para usar `account["currentBalance"]` y `account["baseType"]`.

### P5 — Campo date en AccountTransaction
- No se implementó: `createdAt` ya cubre la función de fecha. `date` era redundante.

## [2026-06-13] default_accounts creado (sin conectar)

- **`packages/ledger/ledger/core/default_values/default_accounts.py`**
  - Creada función `default_accounts(business_id)` que inserta las 5 cuentas
    base (Activos, Pasivos, Patrimonio, Ingresos, Egresos) usando el repositorio.
  - No está conectada a ningún flujo aún. Pendiente de decidir dónde dispararla.

## [2026-06-14] Eliminado baseType del modelo Account

- **`packages/ledger/ledger/repos/v1/accounts/models/account_model.py`**
  - Eliminado `BaseAccountType` type alias y campo `baseType` de `BaseAccount` y `UpdateAccount`.
  - Las cuentas ahora solo usan `type` (debit/credit) para su naturaleza.

- **`packages/ledger/ledger/core/default_values/default_accounts.py`**
  - `DEFAULT_ACCOUNTS` convertido de `list[dict]` a función `default_accounts_list()` que retorna `list[CreateAccount]` directamente.
  - Eliminado `baseType` de todos los valores por defecto.

## [2026-06-14] Fix: balance check ignoraba el signo débito/crédito

- **`packages/ledger/ledger/core/journals/process_journal.py`**
  - Eliminado `SIGN_FACTOR` y `abs(line.amount)` del cálculo de balance.
  - Ahora se usa `line.amount` directamente (positivo = débito, negativo = crédito).
  - **Bug**: El `abs()` impedía distinguir créditos de débitos, causando
    `ValueError("Journal entry does not balance")` en asientos balanceados
    que usaban créditos en cuentas de naturaleza deudora (ej. pagar gasto
    en efectivo: crédito a Caja + débito a Gasto).

### Pendiente por definir

- **Dónde disparar `default_accounts(business_id)`**: al crear un negocio, en
  el startup, o ambos. Ver `AGENT_PENDING_CLARIFICATION.md`.
