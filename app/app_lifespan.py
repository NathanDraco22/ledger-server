from contextlib import asynccontextmanager

from fastapi import FastAPI

from ledger.core.services_initializer import ledger_init_services


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ledger_init_services()
    yield
