from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.interface_adapters.controllers import router

from app.infrastructure.database.postgres import engine
from app.domain.database.models import Base

# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Code to run on shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(router)
