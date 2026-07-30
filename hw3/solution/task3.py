class Heap:
    def __init__(self):
        self.data = []

    def push(self, value):
        """Вставляет элемент в кучу"""
        # TODO: Реализовать heapify-up
        raise NotImplementedError

    def pop(self):
        """Извлекает минимальный элемент"""
        # TODO: Реализовать heapify-down
        raise NotImplementedError

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"Heap({self.data})"

    def __iter__(self):
        """
        Возвращает итератор.
        ВАЖНО: итератор должен работать на КОПИИ данных!
        """
        # TODO: вернуть HeapIterator(...)
        raise NotImplementedError


class HeapIterator:
    def __init__(self, data_snapshot):
        """
        Принимает копию массива кучи.
        На основе этой копии должен уметь извлекать элементы в порядке возрастания.
        """
        # TODO: сохранить снимок данных
        # TODO: возможно, построить вспомогательную "внутреннюю" кучу
        raise NotImplementedError

    def __iter__(self):
        return self

    def __next__(self):
        """
        Должен возвращать следующий минимальный элемент или
        вызвать StopIteration, если элементов больше нет.
        """
        # TODO: реализовать
        raise NotImplementedError
