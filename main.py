from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Smart Data Validator API")

app.include_router(router, prefix="/api")
