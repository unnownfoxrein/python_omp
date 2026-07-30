"""Тесты для задачи «Implicit»."""

import typing as tp

import pytest

try:
    from solution.task2 import implicit
except ImportError:
    pytest.skip("Task 2 has not been implemented yet", allow_module_level=True)


class Person:
    kind: tp.ClassVar[str] = "Person"

    def __init__(self, name: str, age: int) -> None:
        self.name: str = name
        self.age: str = age


class User:
    kind: tp.ClassVar[str] = "User"

    def __init__(self, user_id: int, name: str) -> None:
        self.user_id: int = user_id
        self.name: str = name


@implicit(Person("Vasya", 20))
class Vasya20Person:
    pass


@pytest.mark.parametrize(
    "delegates,attr,value",
    [
        (Person("Vasya", 20), "name", "Vasya"),
        ((Person("Igor", 18), User(1, "igor1337")), "name", "igor1337"),
        ((User(1, "igor1337"), Person("Igor", 18)), "name", "Igor"),
        ((Person("Petya", 21), Person("Vasya", 20), User(1, "Igor")), "age", 20),
        (Person, "kind", "Person"),
        ((Person, User), "kind", "User"),
    ],
)
def test_implicit_adds_attrs_simple(
    delegates: tp.Any | tuple[tp.Any, ...],
    attr: str,
    value: tp.Any,
) -> None:
    """Тест проверяет, что приписывание implicit добавляет атрибуты переданных объектов."""

    @implicit(delegates)
    class ImplicitCls:
        pass

    assert getattr(ImplicitCls(), attr) == value


def test_implicit_adds_atrts_trans() -> None:
    """Тест проверяет, что implicit транзитивно добавляет новые атрибуты."""

    vasya = Vasya20Person()

    @implicit(vasya)
    class ImplicitCls:
        pass

    assert ImplicitCls().kind == vasya.kind
    assert ImplicitCls().name == vasya.name
    assert ImplicitCls().age == vasya.age


def test_implicit_adds_undeclared_attrs() -> None:
    """Тест проверяет, что implicit добавляет все атрибуты, которые имеет объект на момент декорирования."""

    vasya = Vasya20Person()
    vasya.secret_attr = 42

    @implicit(vasya)
    class ImplicitCls:
        pass

    assert ImplicitCls().secret_attr == 42


def test_implicit_does_not_override_attr() -> None:
    """Тест проверяет, что implicit не перекрывает существующие атрибуты."""

    @implicit(Vasya20Person())
    class IgorPerson:
        def __init__(self) -> None:
            self.name: str = "Igor"
            self.age: int = 42

    assert IgorPerson().name == "Igor"
    assert IgorPerson().age == 42


def test_implicit_adds_only_declared_attrs() -> None:
    """Тест проверяет, что implicit не добавляет объекту лишних атрибутов."""

    @implicit(Vasya20Person())
    class ImplicitCls:
        pass

    assert hasattr(ImplicitCls(), "name")
    assert hasattr(ImplicitCls(), "age")
    assert not hasattr(ImplicitCls(), "this_attr_does_not_exist")
