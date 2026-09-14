from fastapi import FastAPI

from app.core import model_registry  # noqa: F401 (registers all SQLAlchemy models)
from app.api.v1.router import api_router

app = FastAPI(title="PlumiHope API", version="0.1.0")

app.include_router(api_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
