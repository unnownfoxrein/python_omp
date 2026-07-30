"""Тесты для Задачи 3: логика анализа запуска.

Проверяют чистые функции оценки погодных условий.
20 баллов.

НЕ ИЗМЕНЯЙТЕ ЭТОТ ФАЙЛ.
"""

from datetime import datetime, timedelta

import pytest

from app.analysis import best_launch_window, evaluate_current, find_launch_windows
from app.models import (
    LaunchConditions,
    LaunchStatus,
    LaunchWindow,
    WeatherCurrent,
    WeatherForecast,
)


def _make_weather(**kwargs) -> WeatherCurrent:
    """Хелпер: создать WeatherCurrent с дефолтами для хорошей погоды."""
    defaults = {
        "temperature": 15.0,
        "wind_speed": 10.0,
        "wind_direction": 180,
        "humidity": 50,
        "precipitation": 0.0,
        "cloud_cover": 20,
        "weather_code": 0,
    }
    defaults.update(kwargs)
    return WeatherCurrent(**defaults)


def _make_forecast(
    start: datetime, hours: int, **overrides
) -> list[WeatherForecast]:
    """Хелпер: создать список прогнозов."""
    result = []
    for i in range(hours):
        data = {
            "timestamp": start + timedelta(hours=i),
            "temperature": 15.0,
            "wind_speed": 10.0,
            "precipitation_probability": 5,
            "cloud_cover": 20,
        }
        data.update(overrides)
        result.append(WeatherForecast(**data))
    return result


# =================== evaluate_current (7 баллов) ==============================


class TestEvaluateCurrent:
    """Тесты для evaluate_current."""

    def test_go_all_conditions_met(self):
        """Все условия в норме — GO."""
        weather = _make_weather()
        conditions = LaunchConditions()

        verdict = evaluate_current(weather, conditions)

        assert verdict.status == LaunchStatus.GO
        assert verdict.reasons == []

    def test_no_go_high_wind(self):
        """Сильный ветер — NO_GO."""
        weather = _make_weather(wind_speed=45.0)
        conditions = LaunchConditions()

        verdict = evaluate_current(weather, conditions)

        assert verdict.status == LaunchStatus.NO_GO
        assert len(verdict.reasons) >= 1
        # Проверяем, что причина упоминает ветер
        assert any("ветер" in r.lower() or "wind" in r.lower() for r in verdict.reasons)

    def test_no_go_precipitation(self):
        """Осадки выше нормы — NO_GO."""
        weather = _make_weather(precipitation=5.0)
        conditions = LaunchConditions()

        verdict = evaluate_current(weather, conditions)

        assert verdict.status == LaunchStatus.NO_GO
        assert len(verdict.reasons) >= 1

    def test_no_go_both_wind_and_precipitation(self):
        """И ветер, и осадки — NO_GO с двумя причинами."""
        weather = _make_weather(wind_speed=50.0, precipitation=3.0)
        conditions = LaunchConditions()

        verdict = evaluate_current(weather, conditions)

        assert verdict.status == LaunchStatus.NO_GO
        assert len(verdict.reasons) >= 2

    def test_caution_high_cloud_cover(self):
        """Высокая облачность — CAUTION."""
        weather = _make_weather(cloud_cover=85)
        conditions = LaunchConditions()

        verdict = evaluate_current(weather, conditions)

        assert verdict.status == LaunchStatus.CAUTION
        assert len(verdict.reasons) >= 1

    def test_caution_low_temperature(self):
        """Низкая температура — CAUTION."""
        weather = _make_weather(temperature=-15.0)
        conditions = LaunchConditions()

        verdict = evaluate_current(weather, conditions)

        assert verdict.status == LaunchStatus.CAUTION
        assert len(verdict.reasons) >= 1

    def test_caution_high_temperature(self):
        """Высокая температура — CAUTION."""
        weather = _make_weather(temperature=45.0)
        conditions = LaunchConditions()

        verdict = evaluate_current(weather, conditions)

        assert verdict.status == LaunchStatus.CAUTION
        assert len(verdict.reasons) >= 1

    def test_no_go_overrides_caution(self):
        """NO_GO-условие перевешивает CAUTION."""
        weather = _make_weather(wind_speed=50.0, cloud_cover=85)
        conditions = LaunchConditions()

        verdict = evaluate_current(weather, conditions)

        assert verdict.status == LaunchStatus.NO_GO

    def test_custom_conditions(self):
        """Кастомные условия — ветер 20 допустим при увеличенном лимите."""
        weather = _make_weather(wind_speed=35.0)
        conditions = LaunchConditions(max_wind_speed=40.0)

        verdict = evaluate_current(weather, conditions)

        assert verdict.status == LaunchStatus.GO

    def test_verdict_has_checked_at(self):
        """Вердикт содержит timestamp."""
        weather = _make_weather()
        conditions = LaunchConditions()

        verdict = evaluate_current(weather, conditions)

        assert verdict.checked_at is not None


# =================== find_launch_windows (7 баллов) ===========================


class TestFindLaunchWindows:
    """Тесты для find_launch_windows."""

    def test_all_good(self):
        """Все часы хорошие — одно большое окно."""
        start = datetime(2025, 3, 15, 12, 0)
        forecast = _make_forecast(start, 4)
        conditions = LaunchConditions()

        windows = find_launch_windows(forecast, conditions)

        assert len(windows) == 1
        assert windows[0].start == start
        assert windows[0].end == start + timedelta(hours=3)

    def test_all_bad(self):
        """Все часы плохие — нет окон."""
        start = datetime(2025, 3, 15, 12, 0)
        forecast = _make_forecast(start, 4, wind_speed=50.0)
        conditions = LaunchConditions()

        windows = find_launch_windows(forecast, conditions)

        assert windows == []

    def test_empty_forecast(self):
        """Пустой прогноз — нет окон."""
        conditions = LaunchConditions()

        windows = find_launch_windows([], conditions)

        assert windows == []

    def test_single_good_hour(self):
        """Один хороший час — одно окно длиной 0."""
        start = datetime(2025, 3, 15, 12, 0)
        forecast = _make_forecast(start, 1)
        conditions = LaunchConditions()

        windows = find_launch_windows(forecast, conditions)

        assert len(windows) == 1
        assert windows[0].start == start
        assert windows[0].end == start

    def test_multiple_windows(self):
        """Чередование хорошей и плохой погоды — несколько окон."""
        start = datetime(2025, 3, 15, 12, 0)
        # 3 хороших, 1 плохой, 2 хороших
        forecast = _make_forecast(start, 6)
        # Час 3 — сильный ветер
        forecast[3] = WeatherForecast(
            timestamp=start + timedelta(hours=3),
            temperature=15.0,
            wind_speed=50.0,
            precipitation_probability=5,
            cloud_cover=20,
        )
        conditions = LaunchConditions()

        windows = find_launch_windows(forecast, conditions)

        assert len(windows) == 2
        assert windows[0].start == start
        assert windows[0].end == start + timedelta(hours=2)
        assert windows[1].start == start + timedelta(hours=4)
        assert windows[1].end == start + timedelta(hours=5)

    def test_high_precipitation_probability_breaks_window(self):
        """Высокая вероятность осадков прерывает окно."""
        start = datetime(2025, 3, 15, 12, 0)
        forecast = _make_forecast(start, 3)
        # Час 1 — высокая вероятность осадков
        forecast[1] = WeatherForecast(
            timestamp=start + timedelta(hours=1),
            temperature=15.0,
            wind_speed=10.0,
            precipitation_probability=50,
            cloud_cover=20,
        )
        conditions = LaunchConditions()

        windows = find_launch_windows(forecast, conditions)

        assert len(windows) == 2

    def test_cloud_cover_breaks_window(self):
        """Высокая облачность прерывает окно."""
        start = datetime(2025, 3, 15, 12, 0)
        forecast = _make_forecast(start, 3)
        forecast[1] = WeatherForecast(
            timestamp=start + timedelta(hours=1),
            temperature=15.0,
            wind_speed=10.0,
            precipitation_probability=5,
            cloud_cover=90,
        )
        conditions = LaunchConditions()

        windows = find_launch_windows(forecast, conditions)

        assert len(windows) == 2


# =================== best_launch_window (3 балла) =============================


class TestBestLaunchWindow:
    """Тесты для best_launch_window."""

    def test_empty_list(self):
        """Пустой список — None."""
        result = best_launch_window([])
        assert result is None

    def test_single_window(self):
        """Одно окно — вернуть его."""
        window = LaunchWindow(
            start=datetime(2025, 3, 15, 12, 0),
            end=datetime(2025, 3, 15, 15, 0),
        )
        result = best_launch_window([window])
        assert result == window

    def test_multiple_windows_returns_longest(self):
        """Несколько окон — вернуть самое длинное."""
        short = LaunchWindow(
            start=datetime(2025, 3, 15, 12, 0),
            end=datetime(2025, 3, 15, 13, 0),
        )
        long = LaunchWindow(
            start=datetime(2025, 3, 15, 16, 0),
            end=datetime(2025, 3, 15, 20, 0),
        )
        medium = LaunchWindow(
            start=datetime(2025, 3, 15, 22, 0),
            end=datetime(2025, 3, 15, 23, 0),
        )

        result = best_launch_window([short, long, medium])

        assert result == long

    def test_equal_windows_returns_first(self):
        """Окна одной длины — вернуть любое (не упасть)."""
        w1 = LaunchWindow(
            start=datetime(2025, 3, 15, 12, 0),
            end=datetime(2025, 3, 15, 14, 0),
        )
        w2 = LaunchWindow(
            start=datetime(2025, 3, 15, 18, 0),
            end=datetime(2025, 3, 15, 20, 0),
        )

        result = best_launch_window([w1, w2])

        assert result is not None
        assert (result.end - result.start) == timedelta(hours=2)
