"""Тесты для задачи «FixedSizeQueue»."""

import pytest

try:
    from solution.task1 import FixedSizeQueue
except ImportError:
    pytest.skip("Task 1 has not been implemented yet", allow_module_level=True)


def test_len():
    """Тест проверяет корректность работы метода __len__."""
    queue = FixedSizeQueue(maxlen=3)
    assert len(queue) == 0
    queue.put(1)
    assert len(queue) == 1


def test_empty_property():
    """Тест проверяет работу свойства empty."""
    queue = FixedSizeQueue(maxlen=3)
    assert queue.empty is True
    queue.put(1)
    assert queue.empty is False


def test_full_property():
    """Тест проверяет работу свойства full."""
    queue = FixedSizeQueue(maxlen=2)
    assert queue.full is False
    queue.put(1)
    assert queue.full is False
    queue.put(2)
    assert queue.full is True


def test_put():
    """Тест проверяет метод put и генерацию исключения при переполнении."""
    queue = FixedSizeQueue(maxlen=2)
    queue.put(1)
    queue.put(2)
    with pytest.raises(ValueError):
        queue.put(3)


def test_get():
    """Тест проверяет метод get и генерацию исключения при попытке извлечения из пустой очереди."""
    queue = FixedSizeQueue(maxlen=2)
    queue.put(1)
    queue.put(2)
    assert queue.get() == 1
    assert queue.get() == 2
    with pytest.raises(ValueError):
        queue.get()


def test_contains():
    """Тест проверяет работу оператора in."""
    queue = FixedSizeQueue(maxlen=3)
    queue.put(1)
    queue.put(2)
    assert 1 in queue
    assert 3 not in queue


def test_clone():
    """Тест проверяет создание независимой копии очереди."""
    queue = FixedSizeQueue(maxlen=3)
    queue.put(1)
    queue.put(2)
    clone = queue.clone()
    # Проверяем, что клон содержит те же элементы
    assert len(clone) == 2
    assert 1 in clone
    assert 2 in clone
    # Проверяем независимость
    clone.put(3)
    assert 3 in clone
    assert 3 not in queue


def test_iadd():
    """Тест проверяет работу оператора += (in-place addition)."""
    queue = FixedSizeQueue(maxlen=3)
    queue.put(1)
    queue += 2
    assert len(queue) == 2
    assert 1 in queue
    assert 2 in queue


def test_add():
    """Тест проверяет работу оператора + и создание новой очереди."""
    queue = FixedSizeQueue(maxlen=3)
    queue.put(1)
    new_queue = queue + 2
    assert len(new_queue) == 2
    assert 1 in new_queue
    assert 2 in new_queue
    # Проверяем, что оригинальная очередь не изменилась
    assert len(queue) == 1
    assert 2 not in queue