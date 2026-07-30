# Mission Control: Spaceport Weather Intelligence System

> Вы — бэкенд-инженер в частной космической компании. Ваша задача: построить систему
> мониторинга погоды на космодромах мира для принятия решения о запуске ракеты (go/no-go).

Система получает реальные метеоданные через [Open-Meteo API](https://open-meteo.com/)
(бесплатный, без ключа), анализирует их по критериям запуска и выдаёт вердикт через
REST API и веб-дашборд.

---

## Quick Start

```bash
# Установить зависимости
uv sync --all-groups

# Запустить сервер (с hot-reload)
uv run fastapi dev app/main.py

# Открыть в браузере:
#   http://localhost:8000       — дашборд
#   http://localhost:8000/docs  — Swagger UI (документация API)

# Запустить тесты
uv run pytest -v

# Запустить тесты для конкретной задачи
uv run pytest tests/test_task1_models.py -v

# Проверить код линтером
uv run ruff check app/

# Проверить форматирование
uv run ruff format --check app/

# Автоисправление линтера и форматирования
uv run ruff check --fix app/
uv run ruff format app/
```

---

## Задания

### Задача 1: Pydantic-модели (15 баллов)

**Файл:** `app/models.py`

Реализуйте модели данных:

| Модель | Описание |
|--------|----------|
| `WeatherCurrent` | Текущая погода: температура, ветер, влажность, осадки, облачность |
| `WeatherForecast` | Одна запись почасового прогноза |
| `SpaceportInfo` | Информация о космодроме (название, страна, координаты, timezone) |
| `LaunchConditions` | Критерии допустимых условий для запуска (с дефолтами) |

Используйте `Field(ge=..., le=...)` для валидации диапазонов. Модель `Coordinates`
дана как пример — посмотрите на неё.

**Тесты:** `uv run pytest tests/test_task1_models.py -v`

---

### Задача 2: Клиент погодного API (25 баллов)

**Файл:** `app/weather.py`

Реализуйте асинхронные функции для работы с [Open-Meteo API](https://open-meteo.com/en/docs):

| Функция | Описание |
|---------|----------|
| `fetch_current_weather(lat, lon)` | Получить текущую погоду по координатам |
| `fetch_forecast(lat, lon, hours)` | Получить почасовой прогноз |

Ключевой момент — **трансформация параллельных массивов**. Open-Meteo возвращает:
```json
{
  "hourly": {
    "time": ["2025-03-15T12:00", "2025-03-15T13:00"],
    "temperature_2m": [8.5, 9.1],
    "wind_speed_10m": [12.3, 15.0]
  }
}
```

Вам нужно преобразовать это в `list[WeatherForecast]`.

При ошибке API (статус != 200) бросайте `WeatherAPIError`.

**Тесты:** `uv run pytest tests/test_task2_weather.py -v`

> Подсказка: используйте `httpx.AsyncClient` и `zip()` для трансформации массивов.

---

### Задача 3: Логика анализа запуска (20 баллов)

**Файл:** `app/analysis.py`

Реализуйте чистые функции (без обращений к API):

| Функция | Описание |
|---------|----------|
| `evaluate_current(weather, conditions)` | Оценить текущие условия: GO / NO_GO / CAUTION |
| `find_launch_windows(forecast, conditions)` | Найти непрерывные окна в прогнозе |
| `best_launch_window(windows)` | Выбрать самое длинное окно |

**Критерии решения:**
- **NO_GO:** ветер > max или осадки > max
- **CAUTION:** облачность > max, или температура вне диапазона
- **GO:** все условия в норме

`find_launch_windows` — алгоритмическая задача: найти непрерывные последовательности
часов, где все условия выполняются.

**Тесты:** `uv run pytest tests/test_task3_analysis.py -v`

---

### Задача 4: REST API эндпоинты (25 баллов)

**Файл:** `app/routes/api.py`

Реализуйте обработчики HTTP-запросов:

| Эндпоинт | Описание | Баллы |
|----------|----------|-------|
| `GET /api/spaceports` | Список всех космодромов | 3 |
| `GET /api/spaceports/{name}/weather` | Текущая погода | 6 |
| `GET /api/spaceports/{name}/forecast?hours=24` | Прогноз (1-72 ч) | 6 |
| `GET /api/spaceports/{name}/launch-status` | Вердикт + окна запуска | 7 |
| Обработка ошибок (404, 502) | | 3 |

Космодромы (`SPACEPORTS`) уже определены в файле. Используйте функции из задач 2 и 3.

**Тесты:** `uv run pytest tests/test_task4_api.py -v`

> После реализации откройте `http://localhost:8000/docs` — все ваши эндпоинты
> будут видны в Swagger UI.

---

### Задача 5: Веб-дашборд (бонус, 15 баллов)

**Файлы:** `app/routes/pages.py`, `templates/index.html`, `templates/spaceport.html`

| Задача | Описание | Баллы |
|--------|----------|-------|
| Индикаторы на index.html | Цветные кружки (go/no-go/caution) рядом с космодромами | 5 |
| Страница spaceport.html | Детали: погода, вердикт, окна запуска | 7 |
| Page route | `GET /spaceports/{name}` с обработкой ошибок | 3 |

Шаблон `base.html` (тёмная тема "mission control") и CSS уже предоставлены.

**Тесты:** `uv run pytest tests/test_task5_pages.py -v`

---

## Оценивание

| Компонент | Баллов |
|-----------|--------|
| Задача 1: Pydantic-модели | 15 |
| Задача 2: API-клиент (httpx + async) | 25 |
| Задача 3: Логика анализа | 20 |
| Задача 4: REST API эндпоинты | 25 |
| ruff check (lint) | 10 |
| ruff format (форматирование) | 5 |
| **Итого** | **100** |
| Задача 5: Веб-дашборд (бонус) | +15 |
| **Максимум** | **115** |

Проверка полностью автоматическая через GitHub Actions.

---

## Структура проекта

```
hw1/
├── app/
│   ├── main.py          # Точка входа (НЕ ИЗМЕНЯТЬ)
│   ├── models.py        # ← Задача 1
│   ├── weather.py       # ← Задача 2
│   ├── analysis.py      # ← Задача 3
│   └── routes/
│       ├── api.py       # ← Задача 4
│       └── pages.py     # ← Задача 5 (бонус)
├── templates/           # Jinja2-шаблоны
├── static/              # CSS
├── tests/               # Тесты (НЕ ИЗМЕНЯТЬ)
└── pyproject.toml       # Конфигурация (НЕ ИЗМЕНЯТЬ)
```

---

## Полезные ссылки

- [FastAPI документация](https://fastapi.tiangolo.com/)
- [Open-Meteo API](https://open-meteo.com/en/docs)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [httpx](https://www.python-httpx.org/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [uv](https://docs.astral.sh/uv/)
- [ruff](https://docs.astral.sh/ruff/)

---

## Правила

- **Не изменяйте** файлы в `tests/`, `pyproject.toml`, `.github/`, `app/main.py`
- Весь ваш код — в файлах, помеченных `← Задача N`
- Задачи можно выполнять в любом порядке, но рекомендуется 1 → 2 → 3 → 4 → 5
- Коммитьте и пушьте часто — GitHub Actions покажет прогресс
