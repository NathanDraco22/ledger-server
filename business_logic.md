# Arquitectura y Lógica de Negocio (Ledger SaaS)

Este documento centraliza las reglas de negocio, decisiones de arquitectura y descubrimientos del diseño del sistema contable (paquete `ledger`). El sistema está diseñado para ser **Multi-Tenant** (SaaS) y también **Instanciable** (Enterprise Dedicado) sin cambiar el código base.

## 1. Arquitectura Multi-Tenant (Usuarios y Negocios)
El sistema separa estrictamente al usuario de los datos comerciales, permitiendo que un contador gestione múltiples clientes.
*   **Usuarios (`User`):** Tienen un arreglo `businesses: list[BusinessRef]`. Cada referencia contiene el `businessId` y un flag `isOwner`.
*   **Negocios (`Business`):** Es la entidad jurídica y fiscal. Toda entidad contable (cuentas, sucursales, asientos) le pertenece estructuralmente a un `Business` mediante el campo `businessId`.
*   **Aislamiento de Datos:** La lógica del paquete filtra todas las operaciones por `businessId`. Esto permite que funcione como SaaS (filtrando el ID del cliente actual) o como servidor dedicado (filtrando por el único ID existente).

## 2. Sucursales vs. Negocio (Lo Fiscal vs. Lo Operativo)
*   **Nivel Legal (`Business`):** La contabilidad oficial (Plan de Cuentas, Estados Financieros para impuestos) se lleva a nivel del Negocio.
*   **Nivel Operativo (`Branch`):** Las sucursales funcionan como **Centros de Costo**.
    *   Las líneas de los asientos contables pueden etiquetarse opcionalmente con un `branchId`.
    *   Esto permite generar Estados de Resultados filtrados por sucursal para análisis de rentabilidad interna, sin romper la contabilidad legal unificada.

## 3. Plan de Cuentas (Chart of Accounts)
El diseño del árbol de cuentas incluye reglas estrictas para evitar errores de captura:
*   **Jerarquía NoSQL:** Se utiliza `accountIndexPath: list[str]` para lecturas y agregaciones rápidas del árbol, y se complementa con `parentId: str | None` para facilitar la construcción del UI.
*   **Prevención de Errores Decimales:** Los balances se manejan como `int` (enteros, ej. centavos) para evitar la pérdida de precisión de punto flotante.
*   **Cuentas Agrupadoras vs. Transaccionales:**
    *   El modelo incluye un flag: `isTransactionAccount: bool` (Cuenta de Movimiento / Detalle).
    *   **Regla de Negocio 1:** Solo se pueden registrar asientos contables en cuentas donde `isTransactionAccount == True`.
    *   **Regla de Negocio 2 (Jerarquía):** No se pueden crear sub-cuentas (hijas) dentro de una cuenta que ya sea transaccional. Las cuentas transaccionales son estrictamente nodos "hoja" (leaf nodes).
    *   **Regla de Negocio 3 (Mutación):** Si una cuenta fue transaccional y tiene historial/balance, el sistema no permite cambiarla a cuenta agrupadora para evitar la corrupción del árbol.

## 4. Transacciones y Asientos Contables (Partida Doble)
El corazón del sistema utiliza una arquitectura basada en **Asientos** (`JournalEntry`) y **Movimientos Individuales** (`AccountTransaction` o `JournalLine`), garantizando la integridad de los datos financieros.

### Flujo de Registro (Posting Workflow)
Para guardar un asiento contable en el sistema, el motor ejecutará una **Transacción de MongoDB (ACID)** para asegurar que o se guarda todo perfectamente, o no se guarda nada.

1.  **Fase de Validación Matemática (Pre-Guardado):**
    *   El motor recibe el `JournalEntry` (Asiento principal) junto con todas sus líneas de detalle.
    *   **Regla de Oro:** Se suman todos los montos de las líneas (ej. Débitos en positivo, Créditos en negativo). La sumatoria final **DEBE dar exactamente 0**.
    *   Si no da 0, la operación se rechaza inmediatamente con un error (Principio de Partida Doble).
    *   *Validación extra:* Asegurar que cada cuenta involucrada tenga `isTransactionAccount == True`.

2.  **Fase de Ejecución (Dentro de la Mongo Transaction):**
    *   **Paso 1:** Se crea y guarda el documento padre `JournalEntry` (contiene la fecha, descripción global, `businessId`, etc.).
    *   **Paso 2:** Por cada línea del asiento, el sistema genera un documento `AccountTransaction` (Movimiento de Cuenta). Este documento indica individualmente cuánto dinero entra o sale de una cuenta específica y se enlaza al `JournalEntry` padre.
    *   **Paso 3:** Se actualiza el campo `balance` del documento `Account` correspondiente (idealmente usando el operador `$inc` de MongoDB) para reflejar el nuevo saldo real de la cuenta de forma atómica.

3.  **Fase de Cierre:**
    *   Si los pasos 1, 2 y 3 tienen éxito, se hace un `commit` de la transacción en MongoDB y el asiento queda oficialmente registrado e inmutable.
    *   Si algo falla (ej. una cuenta fue borrada), se hace un `rollback` automático y no se altera ningún saldo.
