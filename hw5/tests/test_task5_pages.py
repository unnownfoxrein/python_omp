"""Тесты для Задачи 5 (бонус): веб-дашборд.

Проверяют серверный рендеринг HTML-страниц.
15 бонусных баллов.

НЕ ИЗМЕНЯЙТЕ ЭТОТ ФАЙЛ.
"""

import respx
from httpx import ASGITransport, AsyncClient, Response

from app.main import app
from tests.mock_data import MOCK_CURRENT_RESPONSE_GO, MOCK_FORECAST_RESPONSE


async def _client():
    """Создать async test client."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


# =================== GET / — Index page (5 баллов) ============================


class TestIndexPage:
    """Тесты для главной страницы."""

    async def test_returns_html(self):
        """Главная страница возвращает HTML."""
        client = await _client()
        async with client:
            resp = await client.get("/")

        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    async def test_contains_title(self):
        """HTML содержит заголовок Mission Control."""
        client = await _client()
        async with client:
            resp = await client.get("/")

        assert "Mission Control" in resp.text

    @respx.mock
    async def test_contains_spaceport_names(self):
        """Страница содержит названия космодромов."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_CURRENT_RESPONSE_GO)
        )

        client = await _client()
        async with client:
            resp = await client.get("/")

        html = resp.text
        # Проверяем наличие хотя бы некоторых космодромов
        assert "Байконур" in html or "baikonur" in html.lower()

    @respx.mock
    async def test_contains_status_indicators(self):
        """Страница содержит цветные индикаторы статуса."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_CURRENT_RESPONSE_GO)
        )

        client = await _client()
        async with client:
            resp = await client.get("/")

        html = resp.text
        # Индикаторы должны иметь CSS-класс статуса (go, no-go, caution)
        has_status = (
            "status-indicator go" in html
            or "status-indicator no-go" in html
            or "status-indicator caution" in html
        )
        assert has_status, "Страница должна содержать цветные индикаторы статуса"


# =================== GET /spaceports/{name} — Detail page (7 баллов) ==========


class TestSpaceportDetailPage:
    """Тесты для детальной страницы космодрома."""

    @respx.mock
    async def test_returns_html(self):
        """Страница возвращает HTML."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json={
                **MOCK_CURRENT_RESPONSE_GO,
                **{"hourly": MOCK_FORECAST_RESPONSE["hourly"]},
                **{"hourly_units": MOCK_FORECAST_RESPONSE["hourly_units"]},
            })
        )

        client = await _client()
        async with client:
            resp = await client.get("/spaceports/baikonur")

        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    @respx.mock
    async def test_contains_spaceport_name(self):
        """Страница содержит название космодрома."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json={
                **MOCK_CURRENT_RESPONSE_GO,
                **{"hourly": MOCK_FORECAST_RESPONSE["hourly"]},
                **{"hourly_units": MOCK_FORECAST_RESPONSE["hourly_units"]},
            })
        )

        client = await _client()
        async with client:
            resp = await client.get("/spaceports/baikonur")

        assert "Байконур" in resp.text or "Baikonur" in resp.text

    @respx.mock
    async def test_contains_weather_data(self):
        """Страница содержит погодные данные."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json={
                **MOCK_CURRENT_RESPONSE_GO,
                **{"hourly": MOCK_FORECAST_RESPONSE["hourly"]},
                **{"hourly_units": MOCK_FORECAST_RESPONSE["hourly_units"]},
            })
        )

        client = await _client()
        async with client:
            resp = await client.get("/spaceports/baikonur")

        html = resp.text
        assert "8.5" in html  # temperature

    @respx.mock
    async def test_contains_verdict(self):
        """Страница содержит вердикт (go/no_go/caution)."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json={
                **MOCK_CURRENT_RESPONSE_GO,
                **{"hourly": MOCK_FORECAST_RESPONSE["hourly"]},
                **{"hourly_units": MOCK_FORECAST_RESPONSE["hourly_units"]},
            })
        )

        client = await _client()
        async with client:
            resp = await client.get("/spaceports/baikonur")

        html = resp.text.lower()
        assert "go" in html

    async def test_not_found(self):
        """Несуществующий космодром — 404."""
        client = await _client()
        async with client:
            resp = await client.get("/spaceports/atlantis")

        assert resp.status_code == 404


# =================== Error handling (3 балла) =================================


class TestPagesErrorHandling:
    """Тесты обработки ошибок на веб-страницах."""

    @respx.mock
    async def test_detail_page_api_error(self):
        """При ошибке API — страница показывает сообщение, не падает."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(500, json={"reason": "Error"})
        )

        client = await _client()
        async with client:
            resp = await client.get("/spaceports/baikonur")

        # Страница не должна возвращать 500 — должна показать ошибку
        assert resp.status_code in (200, 502)
        if resp.status_code == 200:
            assert "text/html" in resp.headers["content-type"]
