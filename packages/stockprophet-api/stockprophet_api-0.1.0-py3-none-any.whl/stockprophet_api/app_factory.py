import motor
from beanie import init_beanie
from fastapi import FastAPI
from pydantic_settings import BaseSettings

from models import Security, EquityOption
from routes import aggregated_router

app = FastAPI(
    title="StockProphet.ai API",
    version="1.0.0",
    description="StockProphet.ai API HTTP and Websocket API based on OpenApi 2.1 and FastApi",
    root_path="/v1",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},    
)

class Settings(BaseSettings):
    mongo_host: str = "localhost"
    mongo_user: str = ""
    mongo_pass: str = ""
    mongo_db: str = "beanie_db"
    mongo_port: int = 27017

    @property
    def mongo_dsn(self):
        if self.mongo_user and self.mongo_pass:
            return f"mongodb://{self.mongo_user}:{self.mongo_pass}@{self.mongo_host}:{self.mongo_port}/{self.mongo_db}"
        else:
            return f"mongodb://{self.mongo_host}:{self.mongo_port}/{self.mongo_db}"

@app.on_event("startup")
async def app_init():
    # CREATE MOTOR CLIENT
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(
            Settings().mongo_dsn
        )
    except Exception as e:
        raise RuntimeError(
            "Failed to connect to MongoDB: {0}".format(e)
        ) from e

    # INIT BEANIE
    try:
        await init_beanie(client.beanie_db, document_models=[Security])
    except Exception as e:
        raise RuntimeError(
            "Failed to init Beanie: {0}".format(e)
        ) from e

    # ADD ROUTES
    try:
        app.include_router(aggregated_router, prefix="/v1")
    except Exception as e:
        raise RuntimeError(
            "Failed to add routes: {0}".format(e)
        ) from e
