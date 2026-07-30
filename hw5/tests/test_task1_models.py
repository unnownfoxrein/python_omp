"""Тесты для Задачи 1: Pydantic-модели.

Проверяют корректность определения моделей, валидации и дефолтных значений.
15 баллов.

НЕ ИЗМЕНЯЙТЕ ЭТОТ ФАЙЛ.
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.models import (
    Coordinates,
    LaunchConditions,
    LaunchStatus,
    LaunchVerdict,
    LaunchWindow,
    SpaceportInfo,
    WeatherCurrent,
    WeatherForecast,
)


# ========================= WeatherCurrent (5 баллов) =========================


class TestWeatherCurrent:
    """Тесты модели WeatherCurrent."""

    def test_valid_data(self):
        """Создание с валидными данными."""
        weather = WeatherCurrent(
            temperature=8.5,
            wind_speed=12.3,
            wind_direction=180,
            humidity=45,
            precipitation=0.0,
            cloud_cover=25,
            weather_code=1,
        )
        assert weather.temperature == 8.5
        assert weather.wind_speed == 12.3
        assert weather.wind_direction == 180
        assert weather.humidity == 45
        assert weather.precipitation == 0.0
        assert weather.cloud_cover == 25
        assert weather.weather_code == 1

    def test_negative_temperature(self):
        """Отрицательная температура допустима."""
        weather = WeatherCurrent(
            temperature=-30.5,
            wind_speed=5.0,
            wind_direction=0,
            humidity=80,
            precipitation=0.0,
            cloud_cover=10,
            weather_code=0,
        )
        assert weather.temperature == -30.5

    def test_invalid_humidity_too_high(self):
        """Влажность > 100 должна вызывать ошибку валидации."""
        with pytest.raises(ValidationError):
            WeatherCurrent(
                temperature=10.0,
                wind_speed=5.0,
                wind_direction=90,
                humidity=150,
                precipitation=0.0,
                cloud_cover=50,
                weather_code=0,
            )

    def test_invalid_humidity_negative(self):
        """Отрицательная влажность должна вызывать ошибку валидации."""
        with pytest.raises(ValidationError):
            WeatherCurrent(
                temperature=10.0,
                wind_speed=5.0,
                wind_direction=90,
                humidity=-10,
                precipitation=0.0,
                cloud_cover=50,
                weather_code=0,
            )

    def test_invalid_wind_speed_negative(self):
        """Отрицательная скорость ветра должна вызывать ошибку валидации."""
        with pytest.raises(ValidationError):
            WeatherCurrent(
                temperature=10.0,
                wind_speed=-5.0,
                wind_direction=90,
                humidity=50,
                precipitation=0.0,
                cloud_cover=50,
                weather_code=0,
            )

    def test_invalid_cloud_cover_too_high(self):
        """Облачность > 100 должна вызывать ошибку валидации."""
        with pytest.raises(ValidationError):
            WeatherCurrent(
                temperature=10.0,
                wind_speed=5.0,
                wind_direction=90,
                humidity=50,
                precipitation=0.0,
                cloud_cover=110,
                weather_code=0,
            )

    def test_json_round_trip(self):
        """Сериализация в JSON и обратно."""
        weather = WeatherCurrent(
            temperature=15.0,
            wind_speed=8.0,
            wind_direction=270,
            humidity=60,
            precipitation=0.5,
            cloud_cover=40,
            weather_code=3,
        )
        json_str = weather.model_dump_json()
        restored = WeatherCurrent.model_validate_json(json_str)
        assert restored == weather


# ========================= WeatherForecast (3 балла) =========================


class TestWeatherForecast:
    """Тесты модели WeatherForecast."""

    def test_valid_data(self):
        """Создание с валидными данными."""
        forecast = WeatherForecast(
            timestamp=datetime(2025, 3, 15, 12, 0),
            temperature=9.1,
            wind_speed=15.0,
            precipitation_probability=5,
            cloud_cover=30,
        )
        assert forecast.timestamp == datetime(2025, 3, 15, 12, 0)
        assert forecast.temperature == 9.1
        assert forecast.wind_speed == 15.0
        assert forecast.precipitation_probability == 5
        assert forecast.cloud_cover == 30

    def test_invalid_precipitation_probability(self):
        """Вероятность осадков > 100 должна вызывать ошибку."""
        with pytest.raises(ValidationError):
            WeatherForecast(
                timestamp=datetime(2025, 3, 15, 12, 0),
                temperature=9.1,
                wind_speed=15.0,
                precipitation_probability=120,
                cloud_cover=30,
            )

    def test_invalid_wind_speed(self):
        """Отрицательная скорость ветра в прогнозе."""
        with pytest.raises(ValidationError):
            WeatherForecast(
                timestamp=datetime(2025, 3, 15, 12, 0),
                temperature=9.1,
                wind_speed=-1.0,
                precipitation_probability=5,
                cloud_cover=30,
            )


# ========================= SpaceportInfo (2 балла) ===========================


class TestSpaceportInfo:
    """Тесты модели SpaceportInfo."""

    def test_valid_data(self):
        """Создание с валидными данными."""
        sp = SpaceportInfo(
            name="Байконур",
            country="Казахстан",
            coordinates=Coordinates(latitude=45.965, longitude=63.305),
            timezone="Asia/Oral",
        )
        assert sp.name == "Байконур"
        assert sp.country == "Казахстан"
        assert sp.coordinates.latitude == 45.965
        assert sp.timezone == "Asia/Oral"

    def test_invalid_coordinates(self):
        """Невалидные координаты должны вызывать ошибку."""
        with pytest.raises(ValidationError):
            SpaceportInfo(
                name="Test",
                country="Test",
                coordinates=Coordinates(latitude=100.0, longitude=0.0),
                timezone="UTC",
            )


# ========================= LaunchConditions (3 балла) ========================


class TestLaunchConditions:
    """Тесты модели LaunchConditions."""

    def test_defaults(self):
        """Создание без аргументов — все дефолтные значения."""
        conditions = LaunchConditions()
        assert conditions.max_wind_speed == 30.0
        assert conditions.max_precipitation == 0.1
        assert conditions.max_cloud_cover == 70
        assert conditions.min_temperature == -10.0
        assert conditions.max_temperature == 40.0

    def test_custom_values(self):
        """Создание с кастомными значениями."""
        conditions = LaunchConditions(
            max_wind_speed=50.0,
            max_precipitation=1.0,
            max_cloud_cover=90,
            min_temperature=-20.0,
            max_temperature=50.0,
        )
        assert conditions.max_wind_speed == 50.0
        assert conditions.max_precipitation == 1.0
        assert conditions.max_cloud_cover == 90

    def test_json_round_trip(self):
        """Сериализация LaunchConditions в JSON и обратно."""
        conditions = LaunchConditions(max_wind_speed=25.0)
        json_str = conditions.model_dump_json()
        restored = LaunchConditions.model_validate_json(json_str)
        assert restored.max_wind_speed == 25.0
        # Остальные поля — дефолтные
        assert restored.max_precipitation == 0.1


# ========================= Provided models (не оцениваются) ==================


class TestProvidedModels:
    """Проверка предоставленных моделей (LaunchStatus, LaunchVerdict, LaunchWindow)."""

    def test_launch_status_values(self):
        """Enum LaunchStatus имеет три значения."""
        assert LaunchStatus.GO == "go"
        assert LaunchStatus.NO_GO == "no_go"
        assert LaunchStatus.CAUTION == "caution"

    def test_launch_verdict(self):
        """LaunchVerdict создаётся корректно."""
        verdict = LaunchVerdict(
            status=LaunchStatus.GO,
            reasons=[],
        )
        assert verdict.status == LaunchStatus.GO
        assert verdict.reasons == []
        assert isinstance(verdict.checked_at, datetime)

    def test_launch_window(self):
        """LaunchWindow создаётся корректно."""
        window = LaunchWindow(
            start=datetime(2025, 3, 15, 12, 0),
            end=datetime(2025, 3, 15, 14, 0),
        )
        assert window.start < window.end
