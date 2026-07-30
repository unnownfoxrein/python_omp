import asyncio
import os
import time

import pytest

from solution.task4 import virtualize


RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "resources", "task3")


async def send_request_async(host, port, request):
    """Send a GETLIST request asynchronously and return the response."""
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(request.encode() + b"\r\n\r\n")
    await writer.drain()

    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = await asyncio.wait_for(reader.read(4096), timeout=5)
        if not chunk:
            break
        buf += chunk

    writer.close()
    return buf.decode()


# --- Tests for virtualize ---


class TestVirtualize:
    def test_returns_dict(self):
        result = virtualize(RESOURCES_DIR)
        assert isinstance(result, dict)

    def test_keys_are_bytes(self):
        result = virtualize(RESOURCES_DIR)
        for key in result:
            assert isinstance(key, bytes), f"Key {key!r} is not bytes"

    def test_values_are_bytes(self):
        result = virtualize(RESOURCES_DIR)
        for val in result.values():
            assert isinstance(val, bytes), f"Value {val!r} is not bytes"

    def test_contains_expected_files(self):
        result = virtualize(RESOURCES_DIR)
        assert b"foo.txt" in result
        assert b"bar.txt" in result

    def test_file_content(self):
        result = virtualize(RESOURCES_DIR)
        assert result[b"foo.txt"] == b"Hello, world!\n"
        assert result[b"bar.txt"] == b"Some test data\nwith multiple lines\n"

    def test_empty_directory(self, tmp_path):
        result = virtualize(str(tmp_path))
        assert result == {}

    def test_ignores_subdirectories(self, tmp_path):
        (tmp_path / "file.txt").write_bytes(b"data")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "nested.txt").write_bytes(b"nested")
        result = virtualize(str(tmp_path))
        assert b"file.txt" in result
        assert b"subdir" not in result
        assert b"nested.txt" not in result


# --- Tests for GETLIST async server ---


class TestGetlistAsyncServer:
    @pytest.fixture(autouse=True)
    def setup_server(self):
        try:
            from solution.task4 import getlist_handler
        except (ImportError, NotImplementedError):
            pytest.skip("getlist_handler not implemented")

        self.host = "127.0.0.1"
        self.vfs = virtualize(RESOURCES_DIR)

    def _find_free_port(self):
        import socket

        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]

    def _run_test(self, coro_func):
        """Run an async test with server lifecycle."""
        from solution.task4 import getlist_handler

        port = self._find_free_port()
        vfs = self.vfs

        async def run():
            async def handler(reader, writer):
                await getlist_handler(reader, writer, vfs)

            server = await asyncio.start_server(handler, self.host, port)
            async with server:
                await asyncio.sleep(0.1)
                result = await coro_func(self.host, port)
                server.close()
                return result

        return asyncio.run(run())

    def test_list(self):
        async def check(host, port):
            return await send_request_async(host, port, "LIST")

        resp = self._run_test(check)
        assert resp.startswith("OK ")
        assert "bar.txt" in resp
        assert "foo.txt" in resp

    def test_get_existing_file(self):
        async def check(host, port):
            return await send_request_async(host, port, "GET foo.txt")

        resp = self._run_test(check)
        assert resp.startswith("OK ")
        assert "Hello, world!" in resp

    def test_get_nonexistent_file(self):
        async def check(host, port):
            return await send_request_async(host, port, "GET nonexistent")

        resp = self._run_test(check)
        assert resp.startswith("ERROR")

    def test_invalid_command(self):
        async def check(host, port):
            return await send_request_async(host, port, "INVALID COMMAND")

        resp = self._run_test(check)
        assert resp.startswith("ERROR")

    def test_multiple_clients(self):
        async def check(host, port):
            r1 = await send_request_async(host, port, "LIST")
            r2 = await send_request_async(host, port, "GET foo.txt")
            return r1, r2

        r1, r2 = self._run_test(check)
        assert r1.startswith("OK ")
        assert r2.startswith("OK ")
        assert "Hello, world!" in r2

    def test_get_no_argument(self):
        async def check(host, port):
            return await send_request_async(host, port, "GET")

        resp = self._run_test(check)
        assert resp.startswith("ERROR")

    def test_multiple_requests_one_connection(self):
        """Send two requests over a single TCP connection."""

        async def check(host, port):
            reader, writer = await asyncio.open_connection(host, port)
            writer.write(b"LIST\r\n\r\nGET foo.txt\r\n\r\n")
            await writer.drain()

            buf = b""
            while buf.count(b"\r\n\r\n") < 2:
                chunk = await asyncio.wait_for(reader.read(4096), timeout=5)
                if not chunk:
                    break
                buf += chunk

            writer.close()
            parts = buf.split(b"\r\n\r\n")
            return parts[0].decode(), parts[1].decode()

        resp1, resp2 = self._run_test(check)
        assert resp1.startswith("OK ")
        assert "foo.txt" in resp1
        assert resp2.startswith("OK ")
        assert "Hello, world!" in resp2


# --- Tests for SLOW command ---


class TestSlowCommand:
    @pytest.fixture(autouse=True)
    def setup_server(self):
        try:
            from solution.task4 import getlist_handler
        except (ImportError, NotImplementedError):
            pytest.skip("getlist_handler not implemented")

        self.host = "127.0.0.1"
        self.vfs = virtualize(RESOURCES_DIR)

    def _find_free_port(self):
        import socket

        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]

    def _run_test(self, coro_func):
        from solution.task4 import getlist_handler

        port = self._find_free_port()
        vfs = self.vfs

        async def run():
            async def handler(reader, writer):
                await getlist_handler(reader, writer, vfs)

            server = await asyncio.start_server(handler, self.host, port)
            async with server:
                await asyncio.sleep(0.1)
                result = await coro_func(self.host, port)
                server.close()
                return result

        return asyncio.run(run())

    def test_slow_valid(self):
        async def check(host, port):
            start = time.monotonic()
            resp = await send_request_async(host, port, "SLOW 1")
            elapsed = time.monotonic() - start
            return resp, elapsed

        resp, elapsed = self._run_test(check)
        assert resp.startswith("OK 0")
        assert elapsed >= 0.9

    def test_slow_invalid(self):
        async def check(host, port):
            return await send_request_async(host, port, "SLOW abc")

        resp = self._run_test(check)
        assert resp.startswith("ERROR")

    def test_slow_negative(self):
        async def check(host, port):
            return await send_request_async(host, port, "SLOW -1")

        resp = self._run_test(check)
        assert resp.startswith("ERROR")

    def test_slow_concurrent(self):
        """While one client does SLOW, another should get instant responses."""

        async def check(host, port):
            # Start SLOW in background
            slow_task = asyncio.create_task(
                send_request_async(host, port, "SLOW 1")
            )
            await asyncio.sleep(0.2)  # let SLOW start

            # Send a fast request while SLOW is running
            start = time.monotonic()
            fast_resp = await send_request_async(host, port, "LIST")
            fast_elapsed = time.monotonic() - start

            # Wait for SLOW to complete
            slow_resp = await slow_task

            return fast_resp, fast_elapsed, slow_resp

        fast_resp, fast_elapsed, slow_resp = self._run_test(check)
        assert fast_resp.startswith("OK ")
        assert "foo.txt" in fast_resp
        assert fast_elapsed < 0.5  # should be instant, not blocked by SLOW
        assert slow_resp.startswith("OK 0")

    def test_slow_zero(self):
        async def check(host, port):
            return await send_request_async(host, port, "SLOW 0")

        resp = self._run_test(check)
        assert resp.startswith("OK 0")

    def test_slow_float(self):
        async def check(host, port):
            return await send_request_async(host, port, "SLOW 1.5")

        resp = self._run_test(check)
        assert resp.startswith("ERROR")
