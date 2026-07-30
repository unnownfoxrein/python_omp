import asyncio
import time

import pytest


class TestRunConcurrently:
    @pytest.fixture(autouse=True)
    def setup(self):
        try:
            from solution.task3 import run_concurrently
        except (ImportError, NotImplementedError):
            pytest.skip("run_concurrently not implemented")

    def test_preserves_order(self):
        from solution.task3 import run_concurrently

        async def make(val, delay):
            await asyncio.sleep(delay)
            return val

        async def run():
            results = await run_concurrently([
                make("slow", 0.3),
                make("fast", 0.1),
                make("mid", 0.2),
            ])
            assert results == ["slow", "fast", "mid"]

        asyncio.run(run())

    def test_runs_concurrently(self):
        """All tasks should run at the same time, not sequentially."""
        from solution.task3 import run_concurrently

        async def make(val, delay):
            await asyncio.sleep(delay)
            return val

        async def run():
            start = time.monotonic()
            await run_concurrently([
                make("a", 0.2),
                make("b", 0.2),
                make("c", 0.2),
            ])
            elapsed = time.monotonic() - start
            # Should take ~0.2s, not ~0.6s
            assert elapsed < 0.5

        asyncio.run(run())

    def test_empty_list(self):
        from solution.task3 import run_concurrently

        async def run():
            results = await run_concurrently([])
            assert results == []

        asyncio.run(run())

    def test_single_coroutine(self):
        from solution.task3 import run_concurrently

        async def make():
            return 42

        async def run():
            results = await run_concurrently([make()])
            assert results == [42]

        asyncio.run(run())

    def test_exception_propagates(self):
        from solution.task3 import run_concurrently

        async def failing():
            raise ValueError("boom")

        async def run():
            with pytest.raises(ValueError, match="boom"):
                await run_concurrently([failing()])

        asyncio.run(run())


class TestFirstResult:
    @pytest.fixture(autouse=True)
    def setup(self):
        try:
            from solution.task3 import first_result
        except (ImportError, NotImplementedError):
            pytest.skip("first_result not implemented")

    def test_returns_fastest(self):
        from solution.task3 import first_result

        async def make(val, delay):
            await asyncio.sleep(delay)
            return val

        async def run():
            result = await first_result([
                make("slow", 0.5),
                make("fast", 0.1),
                make("mid", 0.3),
            ])
            assert result == "fast"

        asyncio.run(run())

    def test_cancels_remaining(self):
        """Other tasks should be cancelled after first completes."""
        from solution.task3 import first_result

        cancelled = []

        async def tracked(val, delay):
            try:
                await asyncio.sleep(delay)
                return val
            except asyncio.CancelledError:
                cancelled.append(val)
                raise

        async def run():
            result = await first_result([
                tracked("slow", 1.0),
                tracked("fast", 0.1),
            ])
            await asyncio.sleep(0.1)  # give time for cancellation
            assert result == "fast"
            assert "slow" in cancelled

        asyncio.run(run())

    def test_completes_quickly(self):
        """Should not wait for slow tasks."""
        from solution.task3 import first_result

        async def make(val, delay):
            await asyncio.sleep(delay)
            return val

        async def run():
            start = time.monotonic()
            await first_result([
                make("slow", 2.0),
                make("fast", 0.1),
            ])
            elapsed = time.monotonic() - start
            assert elapsed < 0.5

        asyncio.run(run())

    def test_single_coroutine(self):
        from solution.task3 import first_result

        async def make():
            return 42

        async def run():
            result = await first_result([make()])
            assert result == 42

        asyncio.run(run())


class TestRunWithTimeout:
    @pytest.fixture(autouse=True)
    def setup(self):
        try:
            from solution.task3 import run_with_timeout
        except (ImportError, NotImplementedError):
            pytest.skip("run_with_timeout not implemented")

    def test_all_complete_in_time(self):
        from solution.task3 import run_with_timeout

        async def make(val, delay):
            await asyncio.sleep(delay)
            return val

        async def run():
            results = await run_with_timeout(
                [make("a", 0.1), make("b", 0.1)],
                timeout=1.0,
            )
            assert results == ["a", "b"]

        asyncio.run(run())

    def test_some_timeout(self):
        from solution.task3 import run_with_timeout

        async def make(val, delay):
            await asyncio.sleep(delay)
            return val

        async def run():
            results = await run_with_timeout(
                [make("slow", 1.0), make("fast", 0.1), make("mid", 0.5)],
                timeout=0.3,
            )
            assert results == [None, "fast", None]

        asyncio.run(run())

    def test_custom_default(self):
        from solution.task3 import run_with_timeout

        async def make(val, delay):
            await asyncio.sleep(delay)
            return val

        async def run():
            results = await run_with_timeout(
                [make("slow", 1.0), make("fast", 0.1)],
                timeout=0.3,
                default="TIMEOUT",
            )
            assert results == ["TIMEOUT", "fast"]

        asyncio.run(run())

    def test_preserves_order(self):
        from solution.task3 import run_with_timeout

        async def make(val, delay):
            await asyncio.sleep(delay)
            return val

        async def run():
            results = await run_with_timeout(
                [make("c", 0.3), make("a", 0.1), make("b", 0.2)],
                timeout=0.5,
            )
            assert results == ["c", "a", "b"]

        asyncio.run(run())

    def test_empty_list(self):
        from solution.task3 import run_with_timeout

        async def run():
            results = await run_with_timeout([], timeout=1.0)
            assert results == []

        asyncio.run(run())

    def test_all_timeout(self):
        from solution.task3 import run_with_timeout

        async def slow():
            await asyncio.sleep(10)
            return "done"

        async def run():
            results = await run_with_timeout(
                [slow(), slow()],
                timeout=0.1,
                default="TIMEOUT",
            )
            assert results == ["TIMEOUT", "TIMEOUT"]

        asyncio.run(run())
