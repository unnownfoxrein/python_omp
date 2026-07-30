"""Тесты для Задачи 4: REST API эндпоинты.

Проверяют HTTP-эндпоинты через FastAPI TestClient.
25 баллов.

НЕ ИЗМЕНЯЙТЕ ЭТОТ ФАЙЛ.
"""

import respx
from httpx import ASGITransport, AsyncClient, Response

from app.main import app
from tests.mock_data import (
    MOCK_CURRENT_RESPONSE_GO,
    MOCK_CURRENT_RESPONSE_NO_GO,
    MOCK_FORECAST_RESPONSE,
)


async def _client():
    """Создать async test client."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


# =================== GET /api/spaceports (3 балла) ============================


class TestListSpaceports:
    """Тесты для GET /api/spaceports."""

    async def test_returns_all_spaceports(self):
        """Возвращает все 6 космодромов."""
        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports")

        assert resp.status_code == 200
        data = resp.json()
        assert "baikonur" in data
        assert "canaveral" in data
        assert "vostochny" in data
        assert len(data) == 6

    async def test_spaceport_has_required_fields(self):
        """Каждый космодром содержит обязательные поля."""
        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports")

        data = resp.json()
        baikonur = data["baikonur"]
        assert "name" in baikonur
        assert "country" in baikonur
        assert "coordinates" in baikonur
        assert "timezone" in baikonur


# =================== GET /api/spaceports/{name}/weather (6 баллов) ============


class TestGetWeather:
    """Тесты для GET /api/spaceports/{name}/weather."""

    @respx.mock
    async def test_success(self):
        """Успешный запрос — возвращает погоду."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_CURRENT_RESPONSE_GO)
        )

        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/baikonur/weather")

        assert resp.status_code == 200
        data = resp.json()
        assert "temperature" in data
        assert "wind_speed" in data
        assert data["temperature"] == 8.5

    @respx.mock
    async def test_case_insensitive(self):
        """Имя космодрома нечувствительно к регистру."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_CURRENT_RESPONSE_GO)
        )

        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/Baikonur/weather")

        assert resp.status_code == 200

    async def test_not_found(self):
        """Несуществующий космодром — 404."""
        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/atlantis/weather")

        assert resp.status_code == 404

    @respx.mock
    async def test_upstream_error(self):
        """Ошибка внешнего API — 502."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(500, json={"reason": "Error"})
        )

        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/baikonur/weather")

        assert resp.status_code == 502


# =================== GET /api/spaceports/{name}/forecast (6 баллов) ===========


class TestGetForecast:
    """Тесты для GET /api/spaceports/{name}/forecast."""

    @respx.mock
    async def test_success_default_hours(self):
        """Успешный запрос с дефолтным hours=24."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_FORECAST_RESPONSE)
        )

        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/baikonur/forecast")

        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    @respx.mock
    async def test_custom_hours(self):
        """Запрос с кастомным hours=3."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_FORECAST_RESPONSE)
        )

        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/baikonur/forecast?hours=3")

        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) <= 3

    async def test_hours_validation_too_low(self):
        """hours=0 — ошибка валидации 422."""
        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/baikonur/forecast?hours=0")

        assert resp.status_code == 422

    async def test_hours_validation_too_high(self):
        """hours=100 — ошибка валидации 422."""
        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/baikonur/forecast?hours=100")

        assert resp.status_code == 422

    async def test_not_found(self):
        """Несуществующий космодром — 404."""
        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/atlantis/forecast")

        assert resp.status_code == 404


# =================== GET /api/spaceports/{name}/launch-status (7 баллов) ======


class TestGetLaunchStatus:
    """Тесты для GET /api/spaceports/{name}/launch-status."""

    @respx.mock
    async def test_success_structure(self):
        """Успешный запрос — правильная структура ответа."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json={
                **MOCK_CURRENT_RESPONSE_GO,
                **{"hourly": MOCK_FORECAST_RESPONSE["hourly"]},
                **{"hourly_units": MOCK_FORECAST_RESPONSE["hourly_units"]},
            })
        )

        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/baikonur/launch-status")

        assert resp.status_code == 200
        data = resp.json()
        assert "spaceport" in data
        assert "current_weather" in data
        assert "verdict" in data
        assert "launch_windows" in data
        assert "best_window" in data

    @respx.mock
    async def test_go_verdict(self):
        """Хорошая погода — вердикт GO."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json={
                **MOCK_CURRENT_RESPONSE_GO,
                **{"hourly": MOCK_FORECAST_RESPONSE["hourly"]},
                **{"hourly_units": MOCK_FORECAST_RESPONSE["hourly_units"]},
            })
        )

        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/baikonur/launch-status")

        data = resp.json()
        assert data["verdict"]["status"] == "go"

    @respx.mock
    async def test_no_go_verdict(self):
        """Плохая погода — вердикт NO_GO."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json={
                **MOCK_CURRENT_RESPONSE_NO_GO,
                **{"hourly": MOCK_FORECAST_RESPONSE["hourly"]},
                **{"hourly_units": MOCK_FORECAST_RESPONSE["hourly_units"]},
            })
        )

        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/baikonur/launch-status")

        data = resp.json()
        assert data["verdict"]["status"] == "no_go"
        assert len(data["verdict"]["reasons"]) >= 1

    async def test_not_found(self):
        """Несуществующий космодром — 404."""
        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/atlantis/launch-status")

        assert resp.status_code == 404

    @respx.mock
    async def test_upstream_error(self):
        """Ошибка внешнего API — 502."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(500, json={"reason": "Error"})
        )

        client = await _client()
        async with client:
            resp = await client.get("/api/spaceports/baikonur/launch-status")

        assert resp.status_code == 502
