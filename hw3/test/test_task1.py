"""Тесты для задачи «Полином»."""

import pytest

try:
    from solution.task1 import Poly
except ImportError:
    pytest.skip("Task 1 has not been implemented yet", allow_module_level=True)


@pytest.mark.parametrize(
    "coefs1,coefs2",
    [
        ([], [0]),
        ([1, 2, 3], [1, 2, 3]),
        ([1, 2, 0], [1, 2]),
        ([1, 2, 0, 0], [1, 2, 0]),
    ],
)
def test_poly_eq(
    coefs1: list[int],
    coefs2: list[int],
) -> None:
    """Тест проверяет корректность сравнения полиномов на равенство."""

    assert Poly(coefs1) == Poly(coefs2)


@pytest.mark.parametrize(
    "coefs1,coefs2",
    [
        ([], [1]),
        ([1, 0], [0, 1]),
        ([3, 2, 1], [1, 2, 3]),
    ],
)
def test_poly_neq(
    coefs1: list[int],
    coefs2: list[int],
) -> None:
    """Тест проверяет корректность сравнения полиномов на неравенство."""

    assert Poly(coefs1) != Poly(coefs2)


@pytest.mark.parametrize(
    "coefs1,coefs2,coefs",
    [
        ([], [], []),
        ([1], [0], [1]),
        ([1, 2], [0], [1, 2]),
        ([1, 2, 3], [1, 2, 3], [2, 4, 6]),
        ([1, 2, 3], [4], [5, 2, 3]),
        ([1, 2], [1, 2, 3], [2, 4, 3]),
    ],
)
def test_poly_add(
    coefs1: list[int],
    coefs2: list[int],
    coefs: list[int],
) -> None:
    """Тест проверяет корректность сложения полиномов."""

    assert Poly(coefs1) + Poly(coefs2) == Poly(coefs)


@pytest.mark.parametrize(
    "coefs1,coefs2,coefs",
    [
        ([], [], []),
        ([1], [0], [1]),
        ([1, 2], [0], [1, 2]),
        ([1, 2, 3], [1, 2, 3], [2, 4, 6]),
        ([1, 2, 3], [4], [5, 2, 3]),
        ([1, 2], [1, 2, 3], [2, 4, 3]),
    ],
)
def test_poly_iadd(
    coefs1: list[int],
    coefs2: list[int],
    coefs: list[int],
) -> None:
    """Тест проверяет корректность += для полиномов."""

    poly = Poly(coefs1)

    poly += Poly(coefs2)

    assert poly == Poly(coefs)


@pytest.mark.parametrize(
    "coefs1,coefs2,coefs",
    [
        ([], [], []),
        ([1], [0], [1]),
        ([1, 2, 3], [3, 2, 1], [-2, 0, 2]),
        ([1], [3, 2, 1], [-2, -2, -1]),
        ([3, 2, 1], [1], [2, 2, 1]),
    ],
)
def test_poly_sub(
    coefs1: list[int],
    coefs2: list[int],
    coefs: list[int],
) -> None:
    """Тест проверяет корректность реализации вычитания полиномов."""

    assert Poly(coefs1) - Poly(coefs2) == Poly(coefs)


@pytest.mark.parametrize(
    "coefs1,coefs2,coefs",
    [
        ([], [], []),
        ([1], [0], [1]),
        ([1, 2, 3], [3, 2, 1], [-2, 0, 2]),
        ([1], [3, 2, 1], [-2, -2, -1]),
        ([3, 2, 1], [1], [2, 2, 1]),
    ],
)
def test_poly_sub(
    coefs1: list[int],
    coefs2: list[int],
    coefs: list[int],
) -> None:
    """Тест проверяет корректность -= для полиномов."""

    poly = Poly(coefs1)

    poly -= Poly(coefs2)

    assert poly == Poly(coefs)


@pytest.mark.parametrize(
    "coefs1,scalar,coefs",
    [
        ([], 42, []),
        ([1, 2], 2, [2, 4]),
        ([42, 5, 2, 1], -1, [-42, -5, -2, -1]),
    ],
)
def test_poly_scalar_mul(
    coefs1: list[int],
    scalar: int,
    coefs: list[int],
) -> None:
    """Тест проверяет корректность умножения полинома на число."""

    assert Poly(coefs1) * scalar == Poly(coefs)


@pytest.mark.parametrize(
    "coefs1,scalar,coefs",
    [
        ([], 42, []),
        ([1, 2], 2, [2, 4]),
        ([42, 5, 2, 1], -1, [-42, -5, -2, -1]),
    ],
)
def test_poly_scalar_mul(
    coefs1: list[int],
    scalar: int,
    coefs: list[int],
) -> None:
    """Тест проверяет корректность *= для полиномов."""

    poly = Poly(coefs1)

    poly *= scalar

    assert poly == Poly(coefs)


@pytest.mark.parametrize(
    "coefs1,coefs2,coefs",
    [
        ([1], [1, 2, 3], [1, 2, 3]),
        ([1, 2], [3, 4, 5], [3, 10, 13, 10]),
        ([3, 4], [-1, -2], [-3, -10, -8]),
    ],
)
def test_poly_poly_mul(
    coefs1: list[int],
    coefs2: list[int],
    coefs: list[int],
) -> None:
    """Тест проверяет корректность переменожения двух полиномов."""

    assert Poly(coefs1) @ Poly(coefs2) == Poly(coefs)


@pytest.mark.parametrize(
    "coefs1,coefs2,coefs",
    [
        ([1], [1, 2, 3], [1, 2, 3]),
        ([1, 2], [3, 4, 5], [3, 10, 13, 10]),
        ([3, 4], [-1, -2], [-3, -10, -8]),
    ],
)
def test_poly_poly_mul(
    coefs1: list[int],
    coefs2: list[int],
    coefs: list[int],
) -> None:
    """Тест проверяет корректность @= для полиномов."""

    poly = Poly(coefs1)

    poly @= Poly(coefs2)

    assert poly == Poly(coefs)


@pytest.mark.parametrize(
    "coefs,deg",
    [
        ([], 0),
        ([0], 0),
        ([1], 0),
        ([1, 2, 3], 2),
    ],
)
def test_poly_len(
    coefs: list[int],
    deg: int,
) -> None:
    """Тест проверяет корректность вычисления функции len для полиномов."""

    assert len(Poly(coefs)) == deg


@pytest.mark.parametrize(
    "coefs1,coefs2",
    [
        ([], []),
        ([1], [1, 0]),
        ([1, 2], [1, 2, 1]),
        ([100], [1, 1]),
    ],
)
def test_poly_leq_geq(
    coefs1: list[int],
    coefs2: list[int],
) -> None:
    """Тест проверяет корректность сравнения полинмов на больше-равно и меньше-равно."""

    assert Poly(coefs1) <= Poly(coefs2)
    assert Poly(coefs2) >= Poly(coefs1)


@pytest.mark.parametrize(
    "coefs1,coefs2",
    [
        ([], [1]),
        ([1], [2]),
        ([1, 2], [1, 2, 1]),
        ([1, 2], [0, 3]),
    ],
)
def test_poly_lt_gt(
    coefs1: list[int],
    coefs2: list[int],
) -> None:
    """Тест проверяет корректность сравнения полиномов на больше и меньше."""

    assert Poly(coefs1) < Poly(coefs2)
    assert Poly(coefs2) > Poly(coefs1)


@pytest.mark.parametrize(
    "coefs,idx,coef",
    [
        ([0, 1], 0, 0),
        ([1, 2, 3], 2, 3),
        ([1, 2, 3], 4, 0),
    ],
)
def test_poly_idx(
    coefs: list[int],
    idx: int,
    coef: int,
) -> None:
    """Тест проверяет корректность получения коэффициента полинома по индексу."""

    assert Poly(coefs)[idx] == coef
