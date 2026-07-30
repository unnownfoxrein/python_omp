import pytest

from solution.task4 import retry


class FirstError(Exception): ...


class SecondError(Exception): ...


def test_retry_does_multiple_calls() -> None:
    """Тест проверяет, что retry делает повторные вызовы функции."""

    call_count = 0

    @retry((FirstError, SecondError), max_attempt=5)
    def f():
        nonlocal call_count
        call_count += 1

        if call_count == 1:
            raise FirstError()
        elif call_count == 2:
            raise SecondError()
        else:
            return 42

    f()

    assert call_count == 3


def test_retry_ignores_non_arg_errors() -> None:
    """Тест проверяет, что retry реагирует только на нужные исключения."""

    @retry(FirstError, max_attempt=4)
    def f():
        raise SecondError

    with pytest.raises(SecondError):
        f()


def test_retry_raises_after_failed_retry() -> None:
    """Тест проверяет, что retry выбрасывает исключение, если все вызовы завершились неудачно."""

    @retry(ValueError, max_attempt=10)
    def always_raise():
        raise ValueError

    with pytest.raises(ValueError):
        always_raise()
