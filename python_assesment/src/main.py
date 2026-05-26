from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.logs.logging import setup_logging

from src.config.mongodb import documents_collection, create_indexes


from src.routes.documents import router as documents_router
from src.routes.users import router as users_router
from src.routes.health import router as health_router

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):

    await create_indexes()
    yield

app = FastAPI(title="Document_Insights_API", lifespan=lifespan)

app.include_router(documents_router)
app.include_router(users_router)
app.include_router(health_router)