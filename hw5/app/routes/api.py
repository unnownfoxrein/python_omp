"""REST API эндпоинты для Mission Control.

Задача 4: реализовать обработчики HTTP-запросов.
Используйте функции из app.weather и app.analysis.
"""

from fastapi import APIRouter, HTTPException, Query  # noqa: F401

from app.models import Coordinates, SpaceportInfo

router = APIRouter(prefix="/api", tags=["api"])


# ---------------------------------------------------------------------------
# Данные о космодромах — НЕ ИЗМЕНЯТЬ
# ---------------------------------------------------------------------------

SPACEPORTS: dict[str, SpaceportInfo] = {
    "baikonur": SpaceportInfo(
        name="Байконур",
        country="Казахстан",
        coordinates=Coordinates(latitude=45.965, longitude=63.305),
        timezone="Asia/Oral",
    ),
    "canaveral": SpaceportInfo(
        name="Cape Canaveral",
        country="США",
        coordinates=Coordinates(latitude=28.396, longitude=-80.605),
        timezone="America/New_York",
    ),
    "kourou": SpaceportInfo(
        name="Куру",
        country="Французская Гвиана",
        coordinates=Coordinates(latitude=5.236, longitude=-52.769),
        timezone="America/Cayenne",
    ),
    "tanegashima": SpaceportInfo(
        name="Танегасима",
        country="Япония",
        coordinates=Coordinates(latitude=30.400, longitude=130.969),
        timezone="Asia/Tokyo",
    ),
    "vostochny": SpaceportInfo(
        name="Восточный",
        country="Россия",
        coordinates=Coordinates(latitude=51.884, longitude=128.334),
        timezone="Asia/Yakutsk",
    ),
    "plesetsk": SpaceportInfo(
        name="Плесецк",
        country="Россия",
        coordinates=Coordinates(latitude=62.926, longitude=40.577),
        timezone="Europe/Moscow",
    ),
}


def _get_spaceport(name: str) -> SpaceportInfo:
    """Получить космодром по ключу или бросить 404."""
    spaceport = SPACEPORTS.get(name.lower())
    if spaceport is None:
        raise HTTPException(status_code=404, detail=f"Spaceport '{name}' not found")
    return spaceport


# ---------------------------------------------------------------------------
# Задача 4.1: GET /api/spaceports — список всех космодромов
# ---------------------------------------------------------------------------
#
# Верните словарь {ключ: SpaceportInfo} для всех космодромов.
# Пример ответа:
# {
#     "baikonur": {"name": "Байконур", "country": "Казахстан", ...},
#     "canaveral": {"name": "Cape Canaveral", ...},
#     ...
# }


@router.get("/spaceports")
async def list_spaceports() -> dict[str, SpaceportInfo]:
    """Получить список всех космодромов."""
    # TODO: реализуйте эндпоинт
    raise NotImplementedError("Задача 4.1: реализуйте list_spaceports")


# ---------------------------------------------------------------------------
# Задача 4.2: GET /api/spaceports/{name}/weather — текущая погода
# ---------------------------------------------------------------------------
#
# 1. Найдите космодром по name (используйте _get_spaceport)
# 2. Вызовите fetch_current_weather с координатами космодрома
# 3. Верните WeatherCurrent
#
# Если внешний API вернул ошибку (WeatherAPIError), верните HTTP 502.


@router.get("/spaceports/{name}/weather")
async def get_weather(name: str):
    """Получить текущую погоду на космодроме."""
    # TODO: реализуйте эндпоинт
    raise NotImplementedError("Задача 4.2: реализуйте get_weather")


# ---------------------------------------------------------------------------
# Задача 4.3: GET /api/spaceports/{name}/forecast — прогноз погоды
# ---------------------------------------------------------------------------
#
# Query-параметр hours (int, default=24, от 1 до 72).
# Используйте Query(default=24, ge=1, le=72) для валидации.
#
# 1. Найдите космодром
# 2. Вызовите fetch_forecast
# 3. Верните список WeatherForecast
#
# При ошибке внешнего API — HTTP 502.


@router.get("/spaceports/{name}/forecast")
async def get_forecast(name: str, hours: int = Query(default=24, ge=1, le=72)):
    """Получить почасовой прогноз погоды на космодроме."""
    # TODO: реализуйте эндпоинт
    raise NotImplementedError("Задача 4.3: реализуйте get_forecast")


# ---------------------------------------------------------------------------
# Задача 4.4: GET /api/spaceports/{name}/launch-status — вердикт о запуске
# ---------------------------------------------------------------------------
#
# Это самый сложный эндпоинт — он объединяет задачи 2 и 3.
#
# 1. Найдите космодром
# 2. Получите текущую погоду (fetch_current_weather)
# 3. Получите прогноз на 24 часа (fetch_forecast)
# 4. Оцените текущие условия (evaluate_current) с дефолтными LaunchConditions
# 5. Найдите окна запуска (find_launch_windows)
# 6. Найдите лучшее окно (best_launch_window)
# 7. Верните JSON:
#    {
#        "spaceport": SpaceportInfo,
#        "current_weather": WeatherCurrent,
#        "verdict": LaunchVerdict,
#        "launch_windows": [LaunchWindow, ...],
#        "best_window": LaunchWindow | null
#    }
#
# При ошибке внешнего API — HTTP 502.


@router.get("/spaceports/{name}/launch-status")
async def get_launch_status(name: str):
    """Получить полный отчёт о возможности запуска."""
    # TODO: реализуйте эндпоинт
    raise NotImplementedError("Задача 4.4: реализуйте get_launch_status")
