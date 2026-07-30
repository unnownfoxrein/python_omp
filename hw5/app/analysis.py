"""Логика анализа погодных условий для принятия решения о запуске.

Задача 3: реализовать функции анализа, определяющие, можно ли запускать ракету.

Все функции в этом модуле — чистые (не обращаются к API, не имеют побочных эффектов).
Это делает их легко тестируемыми.
"""

from app.models import (  # noqa: F401
    LaunchConditions,
    LaunchStatus,
    LaunchVerdict,
    LaunchWindow,
    WeatherCurrent,
    WeatherForecast,
)

# ---------------------------------------------------------------------------
# Задача 3.1: evaluate_current — оценка текущих условий
# ---------------------------------------------------------------------------
#
# Логика принятия решения:
#
# NO_GO (запуск невозможен) — если хотя бы одно:
#   - wind_speed > conditions.max_wind_speed
#   - precipitation > conditions.max_precipitation
#
# CAUTION (запуск под вопросом) — если хотя бы одно:
#   - cloud_cover > conditions.max_cloud_cover
#   - temperature < conditions.min_temperature
#   - temperature > conditions.max_temperature
#
# GO (запуск разрешён) — если все условия в норме
#
# Поле reasons должно содержать СПИСОК строк, описывающих КАЖДОЕ нарушение.
# Например: ["Ветер 35.0 км/ч превышает максимум 30.0 км/ч"]
#
# Если нарушений нет (GO), reasons должен быть пустым списком.


def evaluate_current(weather: WeatherCurrent, conditions: LaunchConditions) -> LaunchVerdict:
    """Оценить текущие погодные условия для запуска.

    Args:
        weather: текущие погодные данные
        conditions: критерии допустимых условий

    Returns:
        LaunchVerdict с вердиктом и списком причин
    """
    # TODO: реализуйте функцию
    raise NotImplementedError("Задача 3.1: реализуйте evaluate_current")


# ---------------------------------------------------------------------------
# Задача 3.2: find_launch_windows — поиск окон для запуска
# ---------------------------------------------------------------------------
#
# Проанализируйте почасовой прогноз и найдите непрерывные временные окна,
# в которых ВСЕ условия выполняются одновременно.
#
# Условия для каждого часа (аналогично evaluate_current, но без CAUTION):
#   - wind_speed <= conditions.max_wind_speed
#   - precipitation_probability <= 20 (вероятность осадков ≤ 20%)
#   - cloud_cover <= conditions.max_cloud_cover
#   - min_temperature <= temperature <= max_temperature
#
# Алгоритм: пройдите по прогнозу и найдите непрерывные последовательности
# часов, где все условия выполняются. Каждая такая последовательность —
# одно окно (start = timestamp первого часа, end = timestamp последнего).
#
# Пример:
#   Прогноз: [OK, OK, OK, BAD, OK, OK, BAD, OK]
#   Окна:    [(t0, t2), (t4, t5), (t7, t7)]


def find_launch_windows(
    forecast: list[WeatherForecast], conditions: LaunchConditions
) -> list[LaunchWindow]:
    """Найти временные окна, подходящие для запуска.

    Args:
        forecast: почасовой прогноз (отсортирован по времени)
        conditions: критерии допустимых условий

    Returns:
        Список LaunchWindow с непрерывными окнами
    """
    # TODO: реализуйте функцию
    raise NotImplementedError("Задача 3.2: реализуйте find_launch_windows")


# ---------------------------------------------------------------------------
# Задача 3.3: best_launch_window — лучшее окно для запуска
# ---------------------------------------------------------------------------
#
# Верните самое длинное окно из списка, или None если окон нет.
# Длина окна = end - start.


def best_launch_window(windows: list[LaunchWindow]) -> LaunchWindow | None:
    """Найти лучшее (самое длинное) окно для запуска.

    Args:
        windows: список найденных окон

    Returns:
        Самое длинное окно или None, если окон нет
    """
    # TODO: реализуйте функцию
    raise NotImplementedError("Задача 3.3: реализуйте best_launch_window")
