"""Mission Control — Spaceport Weather Intelligence System.

Точка входа приложения. Этот файл изменять НЕ нужно.

Запуск:
    uv run fastapi dev app/main.py
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.api import router as api_router
from app.routes.pages import router as pages_router

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="Mission Control",
    description="Spaceport Weather Intelligence System",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(api_router)
app.include_router(pages_router)
