from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lib.config import settings
from lib.log import setup_logger
from routes.roku import router as roku_router

setup_logger(settings.log_module_name, settings.log_level)

app = FastAPI(
    title="Roku API",
    description="API for controlling local Roku devices.",
    version="1.0.0",
    docs_url="/",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(roku_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host=settings.host, port=settings.port)
