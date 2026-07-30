import pytest

from solution.task2 import EventLoop, pause, schedule


# --- Part A: Basic scheduling tests ---


class TestEventLoopBasic:
    def test_empty_run(self):
        loop = EventLoop()
        loop.run()  # should not raise

    def test_single_task(self, capsys):
        def task():
            print("hello")
            yield pause()
            print("world")
            yield pause()

        loop = EventLoop()
        loop.add_task(task())
        loop.run()
        assert capsys.readouterr().out == "hello\nworld\n"

    def test_two_tasks_interleaved(self, capsys):
        def task_foo():
            print("1 foo")
            yield pause()
            print("2 foo")
            yield pause()

        def task_bar():
            for i in range(3):
                print(f"{i + 1} bar")
                yield pause()

        loop = EventLoop()
        loop.add_task(task_foo())
        loop.add_task(task_bar())
        loop.run()
        output = capsys.readouterr().out
        assert output == "1 foo\n1 bar\n2 foo\n2 bar\n3 bar\n"

    def test_task_completes_early(self, capsys):
        def short():
            print("short")
            yield pause()

        def long():
            for i in range(3):
                print(f"long {i}")
                yield pause()

        loop = EventLoop()
        loop.add_task(short())
        loop.add_task(long())
        loop.run()
        output = capsys.readouterr().out
        assert output == "short\nlong 0\nlong 1\nlong 2\n"

    def test_unknown_tag_raises(self):
        def bad_task():
            yield ("unknown_tag", None)

        loop = EventLoop()
        loop.add_task(bad_task())
        with pytest.raises((ValueError, RuntimeError, KeyError)):
            loop.run()

    def test_immediate_finish(self):
        """Generator that completes without yielding."""

        def instant():
            return
            yield  # noqa: unreachable — makes it a generator

        loop = EventLoop()
        loop.add_task(instant())
        loop.run()  # should not raise

    def test_code_after_last_yield(self, capsys):
        """Task with code after its last yield."""

        def task():
            yield pause()
            print("after yield")

        loop = EventLoop()
        loop.add_task(task())
        loop.run()
        assert capsys.readouterr().out == "after yield\n"


class TestSchedule:
    def test_schedule_simple(self, capsys):
        def parent():
            print("parent start")
            yield schedule(child())
            print("parent end")

        def child():
            print("child")
            yield pause()

        loop = EventLoop()
        loop.add_task(parent())
        loop.run()
        output = capsys.readouterr().out
        assert output == "parent start\nchild\nparent end\n"

    def test_countdown(self, capsys):
        def countdown(n):
            if n:
                print(f"count {n}")
                yield schedule(countdown(n - 1))
                print(f"done  {n}")

        loop = EventLoop()
        loop.add_task(countdown(3))
        loop.run()
        output = capsys.readouterr().out
        expected = "count 3\ncount 2\ndone  3\ncount 1\ndone  2\ndone  1\n"
        assert output == expected

    def test_schedule_order(self, capsys):
        """scheduled task runs before parent resumes."""

        def parent():
            print("A")
            yield schedule(child())
            print("C")

        def child():
            print("B")
            yield pause()

        loop = EventLoop()
        loop.add_task(parent())
        loop.run()
        output = capsys.readouterr().out
        assert output == "A\nB\nC\n"

    def test_multiple_schedule_from_one_task(self, capsys):
        """Parent schedules two children at different points."""

        def child_a():
            print("A")
            yield pause()

        def child_b():
            print("B")
            yield pause()

        def parent():
            print("start")
            yield schedule(child_a())
            print("mid")
            yield schedule(child_b())
            print("end")

        loop = EventLoop()
        loop.add_task(parent())
        loop.run()
        output = capsys.readouterr().out
        assert output == "start\nA\nmid\nB\nend\n"
