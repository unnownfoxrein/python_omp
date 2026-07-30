"""Тесты для задачи «FixedSizeQueue Iterator»."""

import pytest

try:
    from solution.task4 import FixedSizeQueue, FixedSizeQueueIterator
except ImportError:
    pytest.skip("Task 4 has not been implemented yet", allow_module_level=True)


@pytest.fixture(scope="function")
def empty_queue() -> FixedSizeQueue:
    """Возвращает пустую очередь."""
    return FixedSizeQueue(maxlen=5)


@pytest.fixture(scope="function")
def filled_queue() -> FixedSizeQueue:
    """Возвращает очередь с элементами [1, 2, 3]."""
    queue = FixedSizeQueue(maxlen=5)
    for i in [1, 2, 3]:
        queue.put(i)
    return queue


class TestForwardIterator:
    """Тесты для прямого итератора (__iter__)."""

    def test_iter_empty_queue(self, empty_queue: FixedSizeQueue) -> None:
        """Тест проверяет итерацию по пустой очереди."""
        result = list(empty_queue)
        assert result == []

    def test_iter_single_element(self, empty_queue: FixedSizeQueue) -> None:
        """Тест проверяет итерацию по очереди с одним элементом."""
        empty_queue.put(42)
        result = list(empty_queue)
        assert result == [42]

    def test_iter_multiple_elements(self, filled_queue: FixedSizeQueue) -> None:
        """Тест проверяет итерацию по очереди с несколькими элементами."""
        result = list(filled_queue)
        assert result == [1, 2, 3]

    def test_iter_full_queue(self, empty_queue: FixedSizeQueue) -> None:
        """Тест проверяет итерацию по полной очереди."""
        for i in range(1, 6):
            empty_queue.put(i)
        result = list(empty_queue)
        assert result == [1, 2, 3, 4, 5]

    def test_iter_does_not_modify_queue(self, filled_queue: FixedSizeQueue) -> None:
        """Тест проверяет, что итерация не изменяет состояние очереди."""
        original_len = len(filled_queue)
        _ = list(filled_queue)
        assert len(filled_queue) == original_len
        # Проверяем, что можем извлечь первый элемент
        assert filled_queue.get() == 1

    def test_iter_with_wraparound(self, empty_queue: FixedSizeQueue) -> None:
        """Тест проверяет корректную работу итератора с wrap-around."""
        # Заполняем очередь
        for i in range(1, 6):
            empty_queue.put(i)
        # Извлекаем несколько элементов (создаём wrap-around)
        empty_queue.get()
        empty_queue.get()
        # Добавляем новые элементы
        empty_queue.put(6)
        empty_queue.put(7)

        result = list(empty_queue)
        assert result == [3, 4, 5, 6, 7]

    def test_multiple_iterations(self, filled_queue: FixedSizeQueue) -> None:
        """Тест проверяет, что можно итерироваться несколько раз."""
        result1 = list(filled_queue)
        result2 = list(filled_queue)
        assert result1 == result2 == [1, 2, 3]

    def test_iter_after_modification(self, filled_queue: FixedSizeQueue) -> None:
        """Тест проверяет, что итератор создаётся на snapshot данных."""
        iterator = iter(filled_queue)
        # Модифицируем очередь после создания итератора
        filled_queue.put(4)
        # Итератор должен видеть только старые данные
        result = list(iterator)
        assert result == [1, 2, 3]
        assert 4 not in result


class TestReverseIterator:
    """Тесты для обратного итератора (__reversed__)."""

    def test_reversed_empty_queue(self, empty_queue: FixedSizeQueue) -> None:
        """Тест проверяет обратную итерацию по пустой очереди."""
        result = list(reversed(empty_queue))
        assert result == []

    def test_reversed_single_element(self, empty_queue: FixedSizeQueue) -> None:
        """Тест проверяет обратную итерацию по очереди с одним элементом."""
        empty_queue.put(42)
        result = list(reversed(empty_queue))
        assert result == [42]

    def test_reversed_multiple_elements(self, filled_queue: FixedSizeQueue) -> None:
        """Тест проверяет обратную итерацию по очереди с несколькими элементами."""
        result = list(reversed(filled_queue))
        assert result == [3, 2, 1]

    def test_reversed_full_queue(self, empty_queue: FixedSizeQueue) -> None:
        """Тест проверяет обратную итерацию по полной очереди."""
        for i in range(1, 6):
            empty_queue.put(i)
        result = list(reversed(empty_queue))
        assert result == [5, 4, 3, 2, 1]

    def test_reversed_does_not_modify_queue(
        self, filled_queue: FixedSizeQueue
    ) -> None:
        """Тест проверяет, что обратная итерация не изменяет состояние очереди."""
        original_len = len(filled_queue)
        _ = list(reversed(filled_queue))
        assert len(filled_queue) == original_len
        # Проверяем, что можем извлечь первый элемент
        assert filled_queue.get() == 1

    def test_reversed_with_wraparound(self, empty_queue: FixedSizeQueue) -> None:
        """Тест проверяет корректную работу обратного итератора с wrap-around."""
        # Заполняем очередь
        for i in range(1, 6):
            empty_queue.put(i)
        # Извлекаем несколько элементов (создаём wrap-around)
        empty_queue.get()
        empty_queue.get()
        # Добавляем новые элементы
        empty_queue.put(6)
        empty_queue.put(7)

        result = list(reversed(empty_queue))
        assert result == [7, 6, 5, 4, 3]

    def test_multiple_reversed_iterations(self, filled_queue: FixedSizeQueue) -> None:
        """Тест проверяет, что можно обратно итерироваться несколько раз."""
        result1 = list(reversed(filled_queue))
        result2 = list(reversed(filled_queue))
        assert result1 == result2 == [3, 2, 1]


class TestIteratorProtocol:
    """Тесты для проверки протокола итератора."""

    def test_iterator_is_iterator(self, filled_queue: FixedSizeQueue) -> None:
        """Тест проверяет, что __iter__ возвращает итератор."""
        iterator = iter(filled_queue)
        assert iter(iterator) is iterator

    def test_iterator_raises_stop_iteration(
        self, filled_queue: FixedSizeQueue
    ) -> None:
        """Тест проверяет, что итератор вызывает StopIteration в конце."""
        iterator = iter(filled_queue)
        # Проходим по всем элементам
        for _ in range(3):
            next(iterator)
        # Следующий вызов должен вызвать StopIteration
        with pytest.raises(StopIteration):
            next(iterator)

    def test_reversed_iterator_is_iterator(
        self, filled_queue: FixedSizeQueue
    ) -> None:
        """Тест проверяет, что __reversed__ возвращает итератор."""
        iterator = reversed(filled_queue)
        assert iter(iterator) is iterator

    def test_reversed_iterator_raises_stop_iteration(
        self, filled_queue: FixedSizeQueue
    ) -> None:
        """Тест проверяет, что обратный итератор вызывает StopIteration в конце."""
        iterator = reversed(filled_queue)
        # Проходим по всем элементам
        for _ in range(3):
            next(iterator)
        # Следующий вызов должен вызвать StopIteration
        with pytest.raises(StopIteration):
            next(iterator)


class TestIteratorIndependence:
    """Тесты для проверки независимости итераторов."""

    def test_forward_and_reverse_independent(
        self, filled_queue: FixedSizeQueue
    ) -> None:
        """Тест проверяет независимость прямого и обратного итераторов."""
        forward = list(filled_queue)
        reverse = list(reversed(filled_queue))
        assert forward == [1, 2, 3]
        assert reverse == [3, 2, 1]

    def test_multiple_iterators_independent(
        self, filled_queue: FixedSizeQueue
    ) -> None:
        """Тест проверяет, что несколько итераторов независимы."""
        iter1 = iter(filled_queue)
        iter2 = iter(filled_queue)

        # Продвигаем первый итератор
        assert next(iter1) == 1
        assert next(iter1) == 2

        # Второй итератор должен начинаться с начала
        assert next(iter2) == 1
        assert next(iter2) == 2


@pytest.mark.parametrize(
    "elements,expected_forward,expected_reverse",
    [
        ([1], [1], [1]),
        ([1, 2], [1, 2], [2, 1]),
        ([1, 2, 3], [1, 2, 3], [3, 2, 1]),
        ([5, 4, 3, 2, 1], [5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
    ],
)
def test_forward_and_reverse_iteration(
    elements: list[int],
    expected_forward: list[int],
    expected_reverse: list[int],
) -> None:
    """Параметризованный тест для прямой и обратной итерации."""
    queue = FixedSizeQueue(maxlen=10)
    for elem in elements:
        queue.put(elem)

    assert list(queue) == expected_forward
    assert list(reversed(queue)) == expected_reverse
