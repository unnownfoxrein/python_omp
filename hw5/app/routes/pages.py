"""Веб-страницы (Jinja2 шаблоны) для Mission Control.

Задача 5 (бонус): реализовать веб-дашборд с отображением статуса космодромов.
"""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

router = APIRouter(tags=["pages"])


# ---------------------------------------------------------------------------
# Задача 5.1: GET / — главная страница дашборда
# ---------------------------------------------------------------------------
#
# Отрендерите шаблон index.html, передав в контекст:
#   - request (обязательно для Jinja2Templates)
#   - spaceports: словарь SPACEPORTS из app.routes.api
#   - statuses: словарь {name: LaunchVerdict} для каждого космодрома
#
# Для получения статусов вызовите evaluate_current для каждого космодрома.
# Если для какого-то космодрома API вернул ошибку — поставьте статус None.
#
# Подсказка: используйте asyncio.gather() для параллельных запросов.


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Главная страница — дашборд с обзором всех космодромов."""
    # TODO: реализуйте страницу (бонус)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "spaceports": {}, "statuses": {}},
    )


# ---------------------------------------------------------------------------
# Задача 5.2: GET /spaceports/{name} — детальная страница космодрома
# ---------------------------------------------------------------------------
#
# Отрендерите шаблон spaceport.html, передав:
#   - request
#   - spaceport: SpaceportInfo
#   - weather: WeatherCurrent
#   - verdict: LaunchVerdict
#   - windows: list[LaunchWindow]
#   - best_window: LaunchWindow | None
#
# Если космодром не найден — HTTP 404.
# Если API погоды недоступен — покажите страницу с сообщением об ошибке.


@router.get("/spaceports/{name}", response_class=HTMLResponse)
async def spaceport_detail(request: Request, name: str):
    """Детальная страница космодрома с погодой и вердиктом."""
    # TODO: реализуйте страницу (бонус)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "spaceports": {}, "statuses": {}},
    )
