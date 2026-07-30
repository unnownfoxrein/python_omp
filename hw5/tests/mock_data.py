"""Mock-данные для тестов.

Реалистичные ответы Open-Meteo API для космодрома Байконур (45.965, 63.305).
Используются в respx-фикстурах для перехвата HTTP-запросов.
"""

# Ответ API для текущей погоды — хорошие условия (GO)
MOCK_CURRENT_RESPONSE_GO = {
    "latitude": 45.96,
    "longitude": 63.3,
    "elevation": 90.0,
    "generationtime_ms": 0.5,
    "utc_offset_seconds": 0,
    "timezone": "GMT",
    "timezone_abbreviation": "GMT",
    "current_units": {
        "time": "iso8601",
        "interval": "seconds",
        "temperature_2m": "°C",
        "relative_humidity_2m": "%",
        "wind_speed_10m": "km/h",
        "wind_direction_10m": "°",
        "precipitation": "mm",
        "cloud_cover": "%",
        "weather_code": "wmo code",
    },
    "current": {
        "time": "2025-03-15T12:00",
        "interval": 900,
        "temperature_2m": 8.5,
        "relative_humidity_2m": 45,
        "wind_speed_10m": 12.3,
        "wind_direction_10m": 180,
        "precipitation": 0.0,
        "cloud_cover": 25,
        "weather_code": 1,
    },
}

# Ответ API для текущей погоды — плохие условия (NO_GO: сильный ветер и осадки)
MOCK_CURRENT_RESPONSE_NO_GO = {
    "latitude": 45.96,
    "longitude": 63.3,
    "elevation": 90.0,
    "generationtime_ms": 0.5,
    "utc_offset_seconds": 0,
    "timezone": "GMT",
    "timezone_abbreviation": "GMT",
    "current_units": {
        "time": "iso8601",
        "interval": "seconds",
        "temperature_2m": "°C",
        "relative_humidity_2m": "%",
        "wind_speed_10m": "km/h",
        "wind_direction_10m": "°",
        "precipitation": "mm",
        "cloud_cover": "%",
        "weather_code": "wmo code",
    },
    "current": {
        "time": "2025-03-15T12:00",
        "interval": 900,
        "temperature_2m": 2.1,
        "relative_humidity_2m": 85,
        "wind_speed_10m": 45.0,
        "wind_direction_10m": 270,
        "precipitation": 3.2,
        "cloud_cover": 90,
        "weather_code": 61,
    },
}

# Ответ API для почасового прогноза (6 часов для простоты тестов)
# Часы 0-2: хорошие условия, час 3: плохой (ветер), часы 4-5: хорошие
MOCK_FORECAST_RESPONSE = {
    "latitude": 45.96,
    "longitude": 63.3,
    "elevation": 90.0,
    "generationtime_ms": 1.2,
    "utc_offset_seconds": 0,
    "timezone": "GMT",
    "timezone_abbreviation": "GMT",
    "hourly_units": {
        "time": "iso8601",
        "temperature_2m": "°C",
        "wind_speed_10m": "km/h",
        "precipitation_probability": "%",
        "cloud_cover": "%",
    },
    "hourly": {
        "time": [
            "2025-03-15T12:00",
            "2025-03-15T13:00",
            "2025-03-15T14:00",
            "2025-03-15T15:00",
            "2025-03-15T16:00",
            "2025-03-15T17:00",
        ],
        "temperature_2m": [8.5, 9.1, 10.2, 7.0, 8.8, 9.5],
        "wind_speed_10m": [12.3, 15.0, 18.5, 42.0, 20.0, 14.0],
        "precipitation_probability": [0, 5, 10, 60, 15, 5],
        "cloud_cover": [25, 30, 35, 85, 40, 20],
    },
}

# Ответ API для прогноза — все часы хорошие
MOCK_FORECAST_RESPONSE_ALL_GOOD = {
    "latitude": 45.96,
    "longitude": 63.3,
    "elevation": 90.0,
    "generationtime_ms": 1.0,
    "utc_offset_seconds": 0,
    "timezone": "GMT",
    "timezone_abbreviation": "GMT",
    "hourly_units": {
        "time": "iso8601",
        "temperature_2m": "°C",
        "wind_speed_10m": "km/h",
        "precipitation_probability": "%",
        "cloud_cover": "%",
    },
    "hourly": {
        "time": [
            "2025-03-15T12:00",
            "2025-03-15T13:00",
            "2025-03-15T14:00",
            "2025-03-15T15:00",
        ],
        "temperature_2m": [8.5, 9.1, 10.2, 9.0],
        "wind_speed_10m": [12.3, 15.0, 18.5, 14.0],
        "precipitation_probability": [0, 5, 10, 5],
        "cloud_cover": [25, 30, 35, 20],
    },
}
