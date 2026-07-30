"""Тесты для задачи «trace_if»."""

import pytest

try:
    from solution.task2 import trace_if
except ImportError:
    pytest.skip("Task 2 has not been implemented yet", allow_module_level=True)


class TestTraceIfBasic:
    """Базовые тесты для декоратора trace_if."""

    def test_trace_when_predicate_true(self, capsys):
        """Тест проверяет, что вывод происходит, когда предикат возвращает True."""

        @trace_if(lambda x: x > 0)
        def positive(x):
            return x * 2

        result = positive(5)

        # Проверяем результат
        assert result == 10

        # Проверяем вывод
        captured = capsys.readouterr()
        assert "positive" in captured.out
        assert "(5,)" in captured.out or "(5)" in captured.out

    def test_no_trace_when_predicate_false(self, capsys):
        """Тест проверяет, что вывода нет, когда предикат возвращает False."""

        @trace_if(lambda x: x > 0)
        def positive(x):
            return x * 2

        result = positive(-5)

        # Проверяем результат
        assert result == -10

        # Проверяем, что вывода нет
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_function_always_executes(self):
        """Тест проверяет, что функция выполняется независимо от предиката."""
        call_count = 0

        @trace_if(lambda x: x > 0)
        def counter(x):
            nonlocal call_count
            call_count += 1
            return x

        counter(5)  # predicate True
        counter(-5)  # predicate False

        assert call_count == 2


class TestTraceIfWithKwargs:
    """Тесты для декоратора с keyword arguments."""

    def test_trace_with_kwargs(self, capsys):
        """Тест проверяет вывод с keyword arguments."""

        @trace_if(lambda x, y, **kwargs: kwargs.get("integral"))
        def div(x, y, *, integral):
            return x // y if integral else x / y

        result = div(4, 2, integral=True)

        # Проверяем результат
        assert result == 2

        # Проверяем вывод
        captured = capsys.readouterr()
        assert "div" in captured.out
        assert "(4, 2)" in captured.out
        assert "integral" in captured.out
        assert "True" in captured.out

    def test_no_trace_with_kwargs_false(self, capsys):
        """Тест проверяет отсутствие вывода, когда предикат с kwargs возвращает False."""

        @trace_if(lambda x, y, **kwargs: kwargs.get("integral"))
        def div(x, y, *, integral):
            return x // y if integral else x / y

        result = div(4, 2, integral=False)

        # Проверяем результат
        assert result == 2.0

        # Проверяем, что вывода нет
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_trace_with_multiple_kwargs(self, capsys):
        """Тест проверяет вывод с несколькими keyword arguments."""

        @trace_if(lambda **kwargs: kwargs.get("debug", False))
        def process(*, value, debug):
            return value * 2

        result = process(value=10, debug=True)

        # Проверяем результат
        assert result == 20

        # Проверяем вывод
        captured = capsys.readouterr()
        assert "process" in captured.out
        assert "value" in captured.out
        assert "debug" in captured.out


class TestTraceIfMixedArgs:
    """Тесты для декоратора с комбинацией позиционных и именованных аргументов."""

    def test_trace_with_mixed_args(self, capsys):
        """Тест проверяет вывод с комбинацией args и kwargs."""

        @trace_if(lambda x, y, *, flag: flag)
        def compute(x, y, *, flag):
            return x + y if flag else x - y

        result = compute(10, 5, flag=True)

        # Проверяем результат
        assert result == 15

        # Проверяем вывод
        captured = capsys.readouterr()
        assert "compute" in captured.out
        assert "(10, 5)" in captured.out
        assert "flag" in captured.out

    def test_predicate_access_all_args(self, capsys):
        """Тест проверяет, что предикат имеет доступ ко всем аргументам."""

        @trace_if(lambda x, y, *, z: x > 0 and y > 0 and z)
        def triple_check(x, y, *, z):
            return x * y

        result1 = triple_check(5, 3, z=True)
        captured1 = capsys.readouterr()
        assert result1 == 15
        assert "triple_check" in captured1.out

        result2 = triple_check(5, -3, z=True)
        captured2 = capsys.readouterr()
        assert result2 == -15
        assert captured2.out == ""


class TestTraceIfReturnValues:
    """Тесты для проверки корректности возвращаемых значений."""

    def test_return_value_preserved(self):
        """Тест проверяет, что декоратор не изменяет возвращаемое значение."""

        @trace_if(lambda x: True)
        def identity(x):
            return x

        assert identity(42) == 42
        assert identity("test") == "test"
        assert identity([1, 2, 3]) == [1, 2, 3]
        assert identity(None) is None

    def test_return_value_with_complex_logic(self):
        """Тест проверяет возвращаемое значение при сложной логике."""

        @trace_if(lambda x: x % 2 == 0)
        def process(x):
            if x < 0:
                return None
            elif x == 0:
                return 0
            else:
                return x * x

        assert process(4) == 16
        assert process(-4) == None
        assert process(3) == 9


class TestTraceIfEdgeCases:
    """Тесты для граничных случаев."""

    def test_no_arguments(self, capsys):
        """Тест проверяет функцию без аргументов."""

        @trace_if(lambda: True)
        def no_args():
            return "called"

        result = no_args()

        assert result == "called"
        captured = capsys.readouterr()
        assert "no_args" in captured.out

    def test_only_args(self, capsys):
        """Тест проверяет функцию только с позиционными аргументами."""

        @trace_if(lambda x, y, z: x + y + z > 10)
        def sum_three(x, y, z):
            return x + y + z

        result1 = sum_three(5, 6, 1)
        captured1 = capsys.readouterr()
        assert result1 == 12
        assert "sum_three" in captured1.out

        result2 = sum_three(1, 2, 3)
        captured2 = capsys.readouterr()
        assert result2 == 6
        assert captured2.out == ""

    def test_only_kwargs(self, capsys):
        """Тест проверяет функцию только с keyword arguments."""

        @trace_if(lambda *, a, b: a > b)
        def compare(*, a, b):
            return a - b

        result1 = compare(a=10, b=5)
        captured1 = capsys.readouterr()
        assert result1 == 5
        assert "compare" in captured1.out

        result2 = compare(a=3, b=7)
        captured2 = capsys.readouterr()
        assert result2 == -4
        assert captured2.out == ""


@pytest.mark.parametrize(
    "x,y,integral,expected_result,should_trace",
    [
        (10, 2, True, 5, True),
        (10, 3, True, 3, True),
        (10, 2, False, 5.0, False),
        (7, 2, False, 3.5, False),
    ],
)
def test_div_parametrized(x, y, integral, expected_result, should_trace, capsys):
    """Параметризованный тест для функции div из примера."""

    @trace_if(lambda x, y, **kwargs: kwargs.get("integral"))
    def div(x, y, *, integral):
        return x // y if integral else x / y

    result = div(x, y, integral=integral)
    assert result == expected_result

    captured = capsys.readouterr()
    if should_trace:
        assert "div" in captured.out
    else:
        assert captured.out == ""
