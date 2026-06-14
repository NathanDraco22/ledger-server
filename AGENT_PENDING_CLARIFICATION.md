# Clarificaciones Pendientes

## 1. Disparo de `default_accounts(business_id)`
Definir cuándo se crean las 5 cuentas base para un negocio:
- ¿Al crear el negocio (en el controller de businesses)?
- ¿En el startup de la app (services_initializer) para negocios existentes?
- ¿Ambos?

## 2. Identificar si un negocio ya tiene cuentas base
- ¿Buscar cuentas con `parentAccountId == null`?
- ¿Agregar flag `isSystemAccount`?
