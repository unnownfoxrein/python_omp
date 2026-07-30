import collections


def pause():
    return "pause", None


def schedule(target):
    return "schedule", target


class EventLoop:
    def __init__(self):
        self.tasks = collections.deque()

    def add_task(self, task):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
