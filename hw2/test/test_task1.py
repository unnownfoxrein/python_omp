"""Тесты для задачи «Функции Фибоначчи».

Note:
    Метка `forked` запускает каждый тест в отдельном процессе.
"""

import pytest
from pytest_mock import MockerFixture

import solution.task1 as _fib


@pytest.mark.forked()
def test_eval_exec_are_forbidden(
    mocker: MockerFixture,
) -> None:
    """Тест проверяет, что функции eval и exec не были использованы при решении."""

    eval_patch = mocker.patch("builtins.eval")
    exec_patch = mocker.patch("builtins.exec")

    getattr(_fib, "fib1")()
    getattr(_fib, "fib2")()
    getattr(_fib, "fib3")()
    getattr(_fib, "fib4")()

    eval_patch.assert_not_called()
    exec_patch.assert_not_called()


@pytest.mark.forked()
def test_fib_exists() -> None:
    """Тест проверяет, что при последовательном вызове генерируются новые функции."""

    n = 10
    fibs = [0, 1, 1]
    for _ in range(n - 2):
        fibs.append(fibs[-2] + fibs[-1])

    for i in range(1, n):
        assert getattr(_fib, f"fib{i}")() == fibs[i]


@pytest.mark.forked()
@pytest.mark.parametrize(
    "fns",
    [
        ["fib4"],
        ["fib1", "fib5"],
        ["fib3", "fib5"],
        ["fib3", "fib3", "fib5"],
        ["fib1", "fib2", "fib3", "fib4", "fib6"],
    ],
)
def test_fib_does_not_exist(
    fns: list[str],
) -> None:
    """Тест проверяет, что функция N не существует до вызова (N - 1) функции."""

    for fn in fns[:-1]:
        getattr(_fib, fn)()

    with pytest.raises(AttributeError):
        getattr(_fib, fns[-1])()

