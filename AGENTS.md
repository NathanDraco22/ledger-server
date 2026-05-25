# AI Agents Guide
Welcome, Agent. This document contains the architectural rules, conventions, and tool usage for this project. **Read this before performing any modification.**

## 🏗 Project Architecture: Onion Architecture
The project follows a strict **Onion Architecture** (Clean Architecture) pattern. Data must flow from the outside in, never the reverse.

### Data Flow Pattern
`Router` (HTTP) → `Controller` (Orchestration) → `Repository` (Business Logic) → `DataSource` (DB/Persistence) → `Service` (External)

### Layer Responsibilities
- **`packages/ledger/`**: Editable Python package (`ledger`) that encapsulates all business logic. Designed to be reusable across future implementations.
  - `ledger/repos/vX/`: Repositories, datasources, and Pydantic models (business logic layer).
  - `ledger/core/`: Shared complex business processes (e.g., invoice processing, report generation).
  - `ledger/services/`: Database connections, external service abstractions (MongoDB/Motor).
  - `ledger/tools/`: Pure utilities and auxiliary helpers (`TimeTools`, `UuidTool`).
  - `ledger/config/`: Configuration files (e.g., `onion-config.toml`).
- **`app/api/vX/`**: FastAPI presentation layer.
  - `router.py`: Endpoint definitions.
  - `controller.py`: Validates inputs, calls package repositories, and maps responses.
- **`app/responses/`**: Shared response models (e.g., `ListResponse`).
- **`app/main.py`**, **`app/app_lifespan.py`**: Application entry point and lifecycle.

---

## 🛠 Tooling: Onion CLI
This project uses a custom CLI called `onion` to automate boilerplate creation.
Full documentation:
- [ONION CLI Usage Guide](https://github.com/NathanDraco22/onion-cli/blob/main/ONION-CLI-USAGE.md)
- [README](https://github.com/NathanDraco22/onion-cli/blob/main/README.md)

Run `uv run onion --help` for available commands.

### Naming Rules
- Entity names **must** be in **singular** (e.g., `product`, not `products`).
- The CLI automatically pluralizes and converts to PascalCase (`order-item` → `OrderItem`).
- Multiple entities can be passed at once: `onion crud product category supplier --version 1`.

### FastAPI Commands

| Command | Router + Controller | Repo + DataSource + Model | Mongo Collection |
|---|---|---|---|
| `router` | ✅ | ❌ | ❌ |
| `crud` | ✅ | ✅ | ❌ |
| `crud-mongo` | ✅ | ✅ | ✅ |
| `repo` | ❌ | ✅ | ❌ |
| `repo-mongo` | ❌ | ✅ | ✅ |

- `--version` flag is **required** for all CRUD commands.
- `--output-dir <DIR>` option controls where files are created (replaces `app/`).

#### `onion project fastapi-app [OUTPUT_DIR] --force`
Copies the `app/` folder template with placeholder entity names.

#### `onion project fastapi-init OUTPUT_DIR --force`
Copies a **complete** FastAPI project (root files, Dockerfile, tests, configs, etc.).

### Generated File Counts (FastAPI)

| Command | Files Created |
|---|---|
| `project fastapi-app` | ~15 |
| `project fastapi-init` | ~25 |
| `crud` | 6 |
| `crud-mongo` | 10 |
| `repo` | 4 |
| `repo-mongo` | 8 |
| `router` | 2 |

### Auto-Registration
The version router (`app/api/v1/router.py`) is **auto-created/updated** with `include_router()` lines — no manual setup needed.

### Regeneration Behavior
When re-running `crud-mongo` on an **existing** entity: the CLI regenerates entity files (router, controller, repository, datasource, models, collection) but **preserves** existing project-level infrastructure (`mongo_service.py`, `services/__init__.py`, `base_mongo_collection.py`). Collection classes are kept with the old pattern (not upgraded to `BaseMongoCollection`).

**Important:** The CLI generates model properties as `snake_case` + `str` by default. After regeneration, you MUST fix them to match project conventions:
- `created_at: str` → `createdAt: int`
- `updated_at: str` → `updatedAt: int | None = None`

### Known Circular Import Fix
When `base_mongo_collection.py` is generated, it imports `from services import MongoService` which causes a circular import (since `services/__init__.py` imports `BaseMongoCollection` from it). Fix by changing to relative import:
```python
from .mongo_service import MongoService
```

**Note:** If creating a NEW API version (e.g., `v2`), it must be included in `app/main.py`.

---

## 📋 Coding Conventions
1. **Naming**:
    - Files/Folders: `snake_case`.
    - Classes: `PascalCase`.
    - Functions/Variables: `snake_case`.
    - **Pydantic Model Properties**: MUST use **`camelCase`** (to maintain consistency with Flutter/MongoDB standards). Example: `productId`, `branchId`.
2. **Entities**: Always use **singular** for entity names (`product`, not `products`).
3. **Database**: 
    - Use `MongoService` for DB access.
    - Collection names are tracked in `app/config/onion-config.toml`.
    - Do NOT hardcode collection names; use constants or configuration references.
4. **Validation**: Use **Pydantic** models for all Request/Response bodies.
5. **Data Types**:
    - **Dates**: Always use `int` (Unix Timestamps).
    - **Currency/Money**: Always use `int` (to avoid floating-point errors, usually representing cents or the smallest unit).
6. **Dependencies**: Managed by `uv`. Add dependencies using `uv add <package>`.

---

## 🤖 Agent Session Protocol
- **`GEMINI.md`**: After every session or major feature completion, YOU MUST update the `GEMINI.md` file at the root. Record the date, the objective, and a summary of the technical implementation.
- **Aesthetics**: When asked for Web App or UI changes, prioritize premium aesthetics, dynamic designs, and rich UX.

---

## ✅ Verification Commands
After every modification, run these commands to verify code quality:
1. `uv run ty check` — type checking
2. `uv run ruff check --fix .` — linting and auto-format

---

## 📐 Repository Implementation Pattern
When implementing repository methods (after CLI generation leaves `NotImplementedError` stubs), follow this established pattern from `app/repos/v1/branches/branches_repository.py`:

### Available Tools
- `from tools import TimeTools, UuidTool`
  - `UuidTool.generate_uuid()` → generates a UUID v4 string
  - `TimeTools.get_now_in_milliseconds()` → current Unix timestamp in milliseconds (int)

### Create Method
```python
async def create_entity(self, create_data: CreateEntity) -> EntityInDb:
    new_entity_in_db = EntityInDb(
        **create_data.model_dump(),
        id=UuidTool.generate_uuid(),
        createdAt=TimeTools.get_now_in_milliseconds(),
    )
    await self.ds.create_entity(new_entity_in_db.model_dump())
    return new_entity_in_db
```

### Update Method
```python
async def update_entity_by_id(self, entity_id: str, data: UpdateEntity) -> EntityInDb | None:
    data_dict = data.model_dump(exclude_unset=True)
    data_dict["updatedAt"] = TimeTools.get_now_in_milliseconds()
    result = await self.ds.update_entity_by_id(entity_id, data_dict)
    if result is None:
        return None
    return EntityInDb.model_validate(result)
```

### Get By Id / Delete By Id Pattern
Both follow the same pattern:
```python
result = await self.ds.method(entity_id)
if result is None:
    return None
return EntityInDb.model_validate(result)
```

### Get All Pattern
```python
results = await self.ds.get_all()
return [EntityInDb.model_validate(r) for r in results]
```

---

## 🏗 Registry Reference
- **Main Entry Point**: `app/main.py`
- **Dependency/Startup**: `app/app_lifespan.py`
- **Global V1 Router**: `app/api/v1/router.py`
- **CLI Config**: `app/config/onion-config.toml`
