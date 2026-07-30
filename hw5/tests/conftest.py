"""Общие фикстуры для тестов.

Настраивает:
- AsyncClient для тестирования FastAPI
- respx-моки для перехвата запросов к Open-Meteo API
"""

import pytest
import respx
from httpx import ASGITransport, AsyncClient, Response

from app.main import app
from tests.mock_data import MOCK_CURRENT_RESPONSE_GO, MOCK_FORECAST_RESPONSE


@pytest.fixture
def async_client():
    """Асинхронный тестовый клиент для FastAPI."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.fixture
def mock_weather_api():
    """respx-мок для Open-Meteo API.

    Перехватывает ВСЕ запросы к api.open-meteo.com.
    Возвращает предопределённые ответы из mock_data.py.
    """
    with respx.mock(assert_all_mocked=False) as respx_mock:
        # Мок для текущей погоды (запросы с параметром current=...)
        respx_mock.get(
            "https://api.open-meteo.com/v1/forecast",
            params__contains={"current": CURRENT_PARAMS_STR},
        ).mock(return_value=Response(200, json=MOCK_CURRENT_RESPONSE_GO))

        # Мок для прогноза (запросы с параметром hourly=...)
        respx_mock.get(
            "https://api.open-meteo.com/v1/forecast",
            params__contains={"hourly": HOURLY_PARAMS_STR},
        ).mock(return_value=Response(200, json=MOCK_FORECAST_RESPONSE))

        yield respx_mock


# Параметры, которые студенты должны отправлять в запросах
CURRENT_PARAMS_STR = (
    "temperature_2m,"
    "relative_humidity_2m,"
    "wind_speed_10m,"
    "wind_direction_10m,"
    "precipitation,"
    "cloud_cover,"
    "weather_code"
)

HOURLY_PARAMS_STR = (
    "temperature_2m,"
    "wind_speed_10m,"
    "precipitation_probability,"
    "cloud_cover"
)


@pytest.fixture
def mock_weather_api_error():
    """respx-мок, имитирующий ошибку Open-Meteo API."""
    with respx.mock(assert_all_mocked=False) as respx_mock:
        respx_mock.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(500, json={"reason": "Internal Server Error"})
        )
        yield respx_mock
