"""Тесты для задачи «Много аргументов»."""

import itertools
import random
from typing import Any, Callable

import pytest

from solution.task3 import compose, lcm, product


@pytest.mark.parametrize(
    "sts",
    [
        [set()],
        [{1}],
        [{1, 2}, {}],
        [{1, 2, 3}, {2, 3}, {3}],
        [{random.randint(a=1, b=100) for _ in range(3)} for _ in range(3)],
    ],
)
def test_product(
    sts: list[set[Any]],
) -> None:
    """Тест проверяет корректность функции product."""

    assert product(*sts) == set(itertools.product(*sts))


@pytest.mark.parametrize(
    "nums,result",
    [
        ([42, 42, 42], 42),
        ([2, 3, 5, 7, 11], 2310),
        ([2, 4, 8, 16, 32], 32),
        ([6, 24, 30], 120),
    ],
)
def test_lcm_ok(
    nums: list[int],
    result: int,
) -> None:
    """Тест проверяет корректность функции lcm."""

    assert lcm(*nums) == result


@pytest.mark.parametrize(
    "nums",
    [
        (),
        (42,),
    ],
)
def test_lcm_no_arg(
    nums: tuple[()] | tuple[int],
) -> None:
    """Тест проверяет, что при неверном числе аргументов lcm выбросит TypeError."""

    with pytest.raises(TypeError):
        lcm(*nums)


@pytest.mark.parametrize(
    "fns,arg,result",
    [
        (
            [
                lambda s: s[::-1],
                str,
                lambda x: x + 1,
            ],
            1234567890,
            "1987654321",
        ),
        (
            [
                lambda s: s + s,
                lambda s: s.upper(),
                lambda s: s[1:-2],
            ],
            "Beautiful is better than ugly.",
            "EAUTIFUL IS BETTER THAN UGLEAUTIFUL IS BETTER THAN UGL",
        ),
        (
            [
                lambda n: n + 2,
                lambda xs: max(xs),
                lambda xs: xs + [40],
                lambda xs: xs[1:],
            ],
            [1337, 1, 4, 5, 10, 20],
            42,
        ),
    ],
)
def test_compose(
    fns: list[Callable[[Any], Any]],
    arg: Any,
    result: Any,
) -> None:
    """Тест проверяет корректность функции compose."""

    assert compose(*fns)(arg) == result

