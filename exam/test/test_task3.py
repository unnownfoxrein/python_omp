"""Тесты для задачи «Transaction»."""

import random

import pytest

try:
    from solution.task3 import Storage
except ImportError:
    pytest.skip("Task 3 has not been implemented yet", allow_module_level=True)


@pytest.fixture(scope="function")
def storage() -> Storage:
    return Storage()


def test_success_one_edit(
    storage: Storage,
) -> None:
    """Тест проверяет корректность добавления нескольких полей в хранилище."""

    number1 = random.randint(a=1, b=1000)
    number2 = random.randint(a=1, b=1000)

    with storage.edit() as se:
        se["number1"] = number1
        se["number2"] = number2

    assert se["number1"] == number1
    assert se["number2"] == number2


def test_success_many_edits(
    storage: Storage,
) -> None:
    """Тест проверяет корректность нескольких добавлений данных в хранилище."""

    number = random.randint(a=1, b=1000)

    with storage.edit() as se:
        se["number"] = number

    with storage.edit() as se:
        se["number"] = number + 1

    assert se["number"] == number + 1


def test_edit_rollbacks_after_error(
    storage: Storage,
) -> None:
    """Тест проверяет, что обновления данных не произойдет при возникновении ошибки."""

    number = random.randint(a=1, b=1000)

    with storage.edit() as se:
        se["number"] = number

    with storage.edit() as se:
        se["number"] = number + 1
        raise RuntimeError()

    assert se["number"] == number


def test_success_commit_after_error(
    storage: Storage,
) -> None:
    """Тест проверяет, что после неудачного изменения удачное пройдет успешно."""

    number = random.randint(a=1, b=1000)

    with storage.edit() as se:
        se["number"] = number

    with storage.edit() as se:
        se["number"] = se["number"] + 1
        raise RuntimeError()

    with storage.edit() as se:
        se["number"] = se["number"] - 1

    assert se["number"] == number - 1


def test_storage_raise_key_error(
    storage: Storage,
) -> None:
    """Тест проверяет, что для неизвестных ключей будет выброшен KeyError."""

    with pytest.raises(KeyError):
        storage["unknown_key"]