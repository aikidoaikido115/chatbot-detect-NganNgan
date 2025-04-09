from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.interface_adapters.controllers import router

from app.infrastructure.database.postgres import engine
from app.domain.database.models import Base

# app = FastAPI()

# @app.on_event("startup")
# def startup():
#     Base.metadata.create_all(bind=engine)

# app.include_router(router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)
