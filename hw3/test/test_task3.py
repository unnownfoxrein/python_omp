import pytest

try:
    from solution.task3 import Heap, HeapIterator
except ImportError:
    pytest.skip("Task 3 has not been implemented yet", allow_module_level=True)


@pytest.fixture(scope="function")
def empty_heap() -> Heap:
    """Возвращает пустую кучу."""
    return Heap()


class TestHeapPush:
    """Тесты для метода push."""

    def test_push_single_element(self, empty_heap: Heap) -> None:
        """Тест проверяет добавление одного элемента в кучу."""
        empty_heap.push(42)

        assert len(empty_heap) == 1
        assert empty_heap.data[0] == 42

    def test_push_multiple_elements_maintains_heap_property(self, empty_heap: Heap) -> None:
        """Тест проверяет, что после добавления нескольких элементов минимум находится в корне."""
        empty_heap.push(5)
        empty_heap.push(3)
        empty_heap.push(8)
        empty_heap.push(1)

        assert empty_heap.data[0] == 1

    def test_push_sorted_elements(self, empty_heap: Heap) -> None:
        """Тест проверяет добавление элементов в отсортированном порядке."""
        for i in range(1, 6):
            empty_heap.push(i)

        assert len(empty_heap) == 5
        assert empty_heap.data[0] == 1

    def test_push_reverse_sorted_elements(self, empty_heap: Heap) -> None:
        """Тест проверяет добавление элементов в обратном порядке."""
        for i in range(5, 0, -1):
            empty_heap.push(i)

        assert len(empty_heap) == 5
        assert empty_heap.data[0] == 1

    def test_push_duplicate_elements(self, empty_heap: Heap) -> None:
        """Тест проверяет добавление одинаковых элементов."""
        empty_heap.push(5)
        empty_heap.push(5)
        empty_heap.push(5)

        assert len(empty_heap) == 3
        assert empty_heap.data[0] == 5


class TestHeapPop:
    """Тесты для метода pop."""

    def test_pop_single_element(self, empty_heap: Heap) -> None:
        """Тест проверяет извлечение единственного элемента."""
        empty_heap.push(42)

        result = empty_heap.pop()

        assert result == 42
        assert len(empty_heap) == 0

    def test_pop_returns_minimum(self, empty_heap: Heap) -> None:
        """Тест проверяет, что pop возвращает минимальный элемент."""
        empty_heap.push(5)
        empty_heap.push(3)
        empty_heap.push(8)
        empty_heap.push(1)

        result = empty_heap.pop()

        assert result == 1

    def test_pop_multiple_times_returns_sorted(self, empty_heap: Heap) -> None:
        """Тест проверяет, что последовательные pop возвращают элементы в порядке возрастания."""
        values = [5, 2, 8, 1, 9, 3]
        for v in values:
            empty_heap.push(v)

        results = []
        while len(empty_heap) > 0:
            results.append(empty_heap.pop())

        assert results == sorted(values)

    def test_pop_from_empty_heap_raises(self, empty_heap: Heap) -> None:
        """Тест проверяет, что pop из пустой кучи вызывает исключение."""
        with pytest.raises(IndexError):
            empty_heap.pop()

    def test_pop_maintains_heap_property(self, empty_heap: Heap) -> None:
        """Тест проверяет, что после pop свойство кучи сохраняется."""
        for v in [10, 5, 20, 3, 7, 15, 25]:
            empty_heap.push(v)

        empty_heap.pop()  # удаляем 3

        # минимум теперь должен быть 5
        assert empty_heap.data[0] == 5


class TestHeapLen:
    """Тесты для метода __len__."""

    def test_len_empty_heap(self, empty_heap: Heap) -> None:
        """Тест проверяет длину пустой кучи."""
        assert len(empty_heap) == 0

    def test_len_after_push(self, empty_heap: Heap) -> None:
        """Тест проверяет длину после добавления элементов."""
        empty_heap.push(1)
        assert len(empty_heap) == 1

        empty_heap.push(2)
        assert len(empty_heap) == 2

    def test_len_after_pop(self, empty_heap: Heap) -> None:
        """Тест проверяет длину после удаления элементов."""
        empty_heap.push(1)
        empty_heap.push(2)
        empty_heap.pop()

        assert len(empty_heap) == 1


class TestHeapRepr:
    """Тесты для метода __repr__."""

    def test_repr_empty_heap(self, empty_heap: Heap) -> None:
        """Тест проверяет строковое представление пустой кучи."""
        assert repr(empty_heap) == "Heap([])"

    def test_repr_with_elements(self, empty_heap: Heap) -> None:
        """Тест проверяет строковое представление кучи с элементами."""
        empty_heap.push(1)
        empty_heap.push(2)

        # repr должен содержать данные кучи
        result = repr(empty_heap)
        assert result.startswith("Heap(")
        assert result.endswith(")")


class TestHeapIterator:
    """Тесты для итератора кучи."""

    def test_iter_returns_elements_in_sorted_order(self, empty_heap: Heap) -> None:
        """Тест проверяет, что итератор возвращает элементы в порядке возрастания."""
        values = [5, 2, 8, 1, 9, 3]
        for v in values:
            empty_heap.push(v)

        result = list(empty_heap)

        assert result == sorted(values)

    def test_iter_does_not_modify_original_heap(self, empty_heap: Heap) -> None:
        """Тест проверяет, что итерация не изменяет исходную кучу."""
        values = [5, 2, 8, 1, 9, 3]
        for v in values:
            empty_heap.push(v)

        original_len = len(empty_heap)

        # проходим по итератору
        _ = list(empty_heap)

        assert len(empty_heap) == original_len

    def test_iter_works_on_copy(self, empty_heap: Heap) -> None:
        """Тест проверяет, что итератор работает на копии данных."""
        for v in [3, 1, 2]:
            empty_heap.push(v)

        iterator = iter(empty_heap)

        # добавляем элемент после создания итератора
        empty_heap.push(0)

        # итератор должен видеть только старые данные
        result = list(iterator)
        assert 0 not in result
        assert result == [1, 2, 3]

    def test_iter_empty_heap(self, empty_heap: Heap) -> None:
        """Тест проверяет итерацию по пустой куче."""
        result = list(empty_heap)

        assert result == []

    def test_iter_single_element(self, empty_heap: Heap) -> None:
        """Тест проверяет итерацию по куче с одним элементом."""
        empty_heap.push(42)

        result = list(empty_heap)

        assert result == [42]

    def test_multiple_iterations(self, empty_heap: Heap) -> None:
        """Тест проверяет, что можно итерироваться несколько раз."""
        for v in [3, 1, 2]:
            empty_heap.push(v)

        result1 = list(empty_heap)
        result2 = list(empty_heap)

        assert result1 == result2 == [1, 2, 3]

    def test_iter_with_duplicates(self, empty_heap: Heap) -> None:
        """Тест проверяет итерацию по куче с дубликатами."""
        for v in [3, 1, 2, 1, 3]:
            empty_heap.push(v)

        result = list(empty_heap)

        assert result == [1, 1, 2, 3, 3]


class TestHeapIteratorProtocol:
    """Тесты для проверки протокола итератора."""

    def test_iterator_is_iterator(self, empty_heap: Heap) -> None:
        """Тест проверяет, что HeapIterator является итератором."""
        empty_heap.push(1)
        iterator = iter(empty_heap)

        assert iter(iterator) is iterator

    def test_iterator_raises_stop_iteration(self, empty_heap: Heap) -> None:
        """Тест проверяет, что итератор вызывает StopIteration в конце."""
        empty_heap.push(1)
        iterator = iter(empty_heap)

        next(iterator)

        with pytest.raises(StopIteration):
            next(iterator)


@pytest.mark.parametrize(
    "values,expected",
    [
        ([1], [1]),
        ([2, 1], [1, 2]),
        ([3, 2, 1], [1, 2, 3]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        ([10, 5, 15, 3, 7, 12, 20], [3, 5, 7, 10, 12, 15, 20]),
    ],
)
def test_heap_sort_via_iteration(
    values: list[int],
    expected: list[int],
) -> None:
    """Тест проверяет, что итерация по куче эквивалентна сортировке."""
    heap = Heap()
    for v in values:
        heap.push(v)

    result = list(heap)

    assert result == expected


@pytest.mark.parametrize(
    "values,expected",
    [
        ([1], [1]),
        ([2, 1], [1, 2]),
        ([3, 2, 1], [1, 2, 3]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
    ],
)
def test_heap_sort_via_pop(
    values: list[int],
    expected: list[int],
) -> None:
    """Тест проверяет heap sort через последовательные pop."""
    heap = Heap()
    for v in values:
        heap.push(v)

    result = []
    while len(heap) > 0:
        result.append(heap.pop())

    assert result == expected
