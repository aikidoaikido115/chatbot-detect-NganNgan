from fastapi import FastAPI
from app.interface_adapters.controllers import router

app = FastAPI()

app.include_router(router)
