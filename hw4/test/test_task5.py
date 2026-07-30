import asyncio
import socket

import pytest


def find_free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(autouse=True)
def cleanup_writers():
    """Clear global writers set between tests to prevent state leaks."""
    try:
        import solution.task5 as mod

        mod.writers.clear()
    except (ImportError, AttributeError):
        pass
    yield
    try:
        import solution.task5 as mod

        mod.writers.clear()
    except (ImportError, AttributeError):
        pass


class TestCountedEcho:
    @pytest.fixture(autouse=True)
    def setup(self):
        try:
            from solution.task5 import handle_client
        except (ImportError, NotImplementedError):
            pytest.skip("handle_client not implemented")

    def _find_free_port(self):
        return find_free_port()

    def test_single_message(self):
        """Test that a single message gets prefix '1: '."""
        from solution.task5 import handle_client

        port = self._find_free_port()

        async def run():
            server = await asyncio.start_server(handle_client, "127.0.0.1", port)
            async with server:
                await asyncio.sleep(0.1)

                r, w = await asyncio.open_connection("127.0.0.1", port)
                w.write(b"hello\n")
                await w.drain()

                msg = await asyncio.wait_for(r.readline(), timeout=2)
                decoded = msg.decode().strip()
                assert decoded == "1: hello"

                w.close()
                server.close()

        asyncio.run(run())

    def test_multiple_messages(self):
        """Test that message counter increments."""
        from solution.task5 import handle_client

        port = self._find_free_port()

        async def run():
            server = await asyncio.start_server(handle_client, "127.0.0.1", port)
            async with server:
                await asyncio.sleep(0.1)

                r, w = await asyncio.open_connection("127.0.0.1", port)

                w.write(b"hello\n")
                await w.drain()
                msg = await asyncio.wait_for(r.readline(), timeout=2)
                assert msg.decode().strip() == "1: hello"

                w.write(b"world\n")
                await w.drain()
                msg = await asyncio.wait_for(r.readline(), timeout=2)
                assert msg.decode().strip() == "2: world"

                w.write(b"foo\n")
                await w.drain()
                msg = await asyncio.wait_for(r.readline(), timeout=2)
                assert msg.decode().strip() == "3: foo"

                w.close()
                server.close()

        asyncio.run(run())

    def test_independent_counters(self):
        """Test that each client has its own counter."""
        from solution.task5 import handle_client

        port = self._find_free_port()

        async def run():
            server = await asyncio.start_server(handle_client, "127.0.0.1", port)
            async with server:
                await asyncio.sleep(0.1)

                r1, w1 = await asyncio.open_connection("127.0.0.1", port)
                r2, w2 = await asyncio.open_connection("127.0.0.1", port)
                await asyncio.sleep(0.1)

                # Client 1 sends two messages
                w1.write(b"a\n")
                await w1.drain()
                msg = await asyncio.wait_for(r1.readline(), timeout=2)
                assert msg.decode().strip() == "1: a"

                w1.write(b"b\n")
                await w1.drain()
                msg = await asyncio.wait_for(r1.readline(), timeout=2)
                assert msg.decode().strip() == "2: b"

                # Client 2 sends one message — counter starts from 1
                w2.write(b"x\n")
                await w2.drain()
                msg = await asyncio.wait_for(r2.readline(), timeout=2)
                assert msg.decode().strip() == "1: x"

                w1.close()
                w2.close()
                server.close()

        asyncio.run(run())

    def test_empty_message_skipped(self):
        """Empty lines should be ignored and not increment counter."""
        from solution.task5 import handle_client

        port = self._find_free_port()

        async def run():
            server = await asyncio.start_server(handle_client, "127.0.0.1", port)
            async with server:
                await asyncio.sleep(0.1)

                r, w = await asyncio.open_connection("127.0.0.1", port)

                # Send empty line, then a real message
                w.write(b"\n")
                await w.drain()
                await asyncio.sleep(0.1)

                w.write(b"hello\n")
                await w.drain()
                msg = await asyncio.wait_for(r.readline(), timeout=2)
                assert msg.decode().strip() == "1: hello"

                w.close()
                server.close()

        asyncio.run(run())


class TestIdleTimeout:
    @pytest.fixture(autouse=True)
    def setup(self):
        try:
            from solution.task5 import handle_client, TIMEOUT
        except (ImportError, NotImplementedError):
            pytest.skip("handle_client not implemented")

    def _find_free_port(self):
        return find_free_port()

    def test_timeout_disconnect(self):
        """Test that idle client gets disconnected with a message."""
        import solution.task5 as task5_mod
        from solution.task5 import handle_client

        port = self._find_free_port()

        original_timeout = task5_mod.TIMEOUT
        task5_mod.TIMEOUT = 1

        async def run():
            server = await asyncio.start_server(handle_client, "127.0.0.1", port)
            async with server:
                await asyncio.sleep(0.1)

                r, w = await asyncio.open_connection("127.0.0.1", port)

                # Send one message to confirm connection works
                w.write(b"hello\n")
                await w.drain()
                msg = await asyncio.wait_for(r.readline(), timeout=2)
                assert msg.decode().strip() == "1: hello"

                # Wait for timeout
                msg = await asyncio.wait_for(r.readline(), timeout=3)
                decoded = msg.decode().strip()
                assert "Timeout" in decoded or "timeout" in decoded
                assert "1" in decoded  # TIMEOUT value

                w.close()
                server.close()

        try:
            asyncio.run(run())
        finally:
            task5_mod.TIMEOUT = original_timeout

    def test_active_client_no_timeout(self):
        """Test that active client does not get disconnected."""
        import solution.task5 as task5_mod
        from solution.task5 import handle_client

        port = self._find_free_port()

        original_timeout = task5_mod.TIMEOUT
        task5_mod.TIMEOUT = 1

        async def run():
            server = await asyncio.start_server(handle_client, "127.0.0.1", port)
            async with server:
                await asyncio.sleep(0.1)

                r, w = await asyncio.open_connection("127.0.0.1", port)

                # Send messages faster than the timeout
                for i in range(3):
                    await asyncio.sleep(0.5)
                    w.write(f"msg{i}\n".encode())
                    await w.drain()
                    msg = await asyncio.wait_for(r.readline(), timeout=2)
                    assert msg.decode().strip() == f"{i + 1}: msg{i}"

                w.close()
                server.close()

        try:
            asyncio.run(run())
        finally:
            task5_mod.TIMEOUT = original_timeout


class TestBroadcast:
    @pytest.fixture(autouse=True)
    def setup(self):
        try:
            from solution.task5 import handle_client
        except (ImportError, NotImplementedError):
            pytest.skip("handle_client not implemented")

    def _find_free_port(self):
        return find_free_port()

    def test_broadcast_received_by_others(self):
        """Test that broadcast message is received by other clients."""
        import solution.task5 as task5_mod
        from solution.task5 import handle_client

        port = self._find_free_port()

        original_timeout = task5_mod.TIMEOUT
        task5_mod.TIMEOUT = 10

        async def run():
            server = await asyncio.start_server(handle_client, "127.0.0.1", port)
            async with server:
                await asyncio.sleep(0.1)

                r1, w1 = await asyncio.open_connection("127.0.0.1", port)
                r2, w2 = await asyncio.open_connection("127.0.0.1", port)
                await asyncio.sleep(0.1)

                # Client 1 sends a broadcast
                w1.write(b"!broadcast greetings\n")
                await w1.drain()
                await asyncio.sleep(0.2)

                # Client 2 should receive it
                msg = await asyncio.wait_for(r2.readline(), timeout=2)
                decoded = msg.decode().strip()
                assert decoded == "greetings"

                w1.close()
                w2.close()
                server.close()

        try:
            asyncio.run(run())
        finally:
            task5_mod.TIMEOUT = original_timeout

    def test_broadcast_not_echoed_to_sender(self):
        """Test that broadcast message is not sent back to the sender."""
        import solution.task5 as task5_mod
        from solution.task5 import handle_client

        port = self._find_free_port()

        original_timeout = task5_mod.TIMEOUT
        task5_mod.TIMEOUT = 10

        async def run():
            server = await asyncio.start_server(handle_client, "127.0.0.1", port)
            async with server:
                await asyncio.sleep(0.1)

                r1, w1 = await asyncio.open_connection("127.0.0.1", port)
                r2, w2 = await asyncio.open_connection("127.0.0.1", port)
                await asyncio.sleep(0.1)

                # Client 1 sends broadcast, then a regular message
                w1.write(b"!broadcast test\n")
                await w1.drain()
                await asyncio.sleep(0.2)

                w1.write(b"regular\n")
                await w1.drain()

                # Client 1 should receive "1: regular", not the broadcast
                msg = await asyncio.wait_for(r1.readline(), timeout=2)
                decoded = msg.decode().strip()
                assert decoded == "1: regular"

                w1.close()
                w2.close()
                server.close()

        try:
            asyncio.run(run())
        finally:
            task5_mod.TIMEOUT = original_timeout

    def test_broadcast_does_not_increment_counter(self):
        """Test that broadcast messages don't increment sender's counter."""
        import solution.task5 as task5_mod
        from solution.task5 import handle_client

        port = self._find_free_port()

        original_timeout = task5_mod.TIMEOUT
        task5_mod.TIMEOUT = 10

        async def run():
            server = await asyncio.start_server(handle_client, "127.0.0.1", port)
            async with server:
                await asyncio.sleep(0.1)

                r1, w1 = await asyncio.open_connection("127.0.0.1", port)
                r2, w2 = await asyncio.open_connection("127.0.0.1", port)
                await asyncio.sleep(0.1)

                # Client 1: regular -> broadcast -> regular
                w1.write(b"hello\n")
                await w1.drain()
                msg = await asyncio.wait_for(r1.readline(), timeout=2)
                assert msg.decode().strip() == "1: hello"

                w1.write(b"!broadcast test\n")
                await w1.drain()
                await asyncio.sleep(0.2)

                # Drain broadcast on client 2
                await asyncio.wait_for(r2.readline(), timeout=2)

                w1.write(b"world\n")
                await w1.drain()
                msg = await asyncio.wait_for(r1.readline(), timeout=2)
                # Counter should be 2, not 3
                assert msg.decode().strip() == "2: world"

                w1.close()
                w2.close()
                server.close()

        try:
            asyncio.run(run())
        finally:
            task5_mod.TIMEOUT = original_timeout

    def test_broadcast_three_clients(self):
        """Broadcast should reach all other connected clients."""
        import solution.task5 as task5_mod
        from solution.task5 import handle_client

        port = self._find_free_port()

        original_timeout = task5_mod.TIMEOUT
        task5_mod.TIMEOUT = 10

        async def run():
            server = await asyncio.start_server(handle_client, "127.0.0.1", port)
            async with server:
                await asyncio.sleep(0.1)

                r1, w1 = await asyncio.open_connection("127.0.0.1", port)
                r2, w2 = await asyncio.open_connection("127.0.0.1", port)
                r3, w3 = await asyncio.open_connection("127.0.0.1", port)
                await asyncio.sleep(0.1)

                w1.write(b"!broadcast hey\n")
                await w1.drain()
                await asyncio.sleep(0.2)

                msg2 = await asyncio.wait_for(r2.readline(), timeout=2)
                msg3 = await asyncio.wait_for(r3.readline(), timeout=2)
                assert msg2.decode().strip() == "hey"
                assert msg3.decode().strip() == "hey"

                w1.close()
                w2.close()
                w3.close()
                server.close()

        try:
            asyncio.run(run())
        finally:
            task5_mod.TIMEOUT = original_timeout

    def test_broadcast_single_client(self):
        """Broadcast with no other clients should not crash."""
        import solution.task5 as task5_mod
        from solution.task5 import handle_client

        port = self._find_free_port()

        original_timeout = task5_mod.TIMEOUT
        task5_mod.TIMEOUT = 10

        async def run():
            server = await asyncio.start_server(handle_client, "127.0.0.1", port)
            async with server:
                await asyncio.sleep(0.1)

                r, w = await asyncio.open_connection("127.0.0.1", port)

                # Broadcast with no other clients
                w.write(b"!broadcast alone\n")
                await w.drain()
                await asyncio.sleep(0.1)

                # Regular message still works
                w.write(b"hello\n")
                await w.drain()
                msg = await asyncio.wait_for(r.readline(), timeout=2)
                assert msg.decode().strip() == "1: hello"

                w.close()
                server.close()

        try:
            asyncio.run(run())
        finally:
            task5_mod.TIMEOUT = original_timeout

    def test_broadcast_without_space(self):
        """'!broadcast' without trailing space is treated as regular echo."""
        import solution.task5 as task5_mod
        from solution.task5 import handle_client

        port = self._find_free_port()

        original_timeout = task5_mod.TIMEOUT
        task5_mod.TIMEOUT = 10

        async def run():
            server = await asyncio.start_server(handle_client, "127.0.0.1", port)
            async with server:
                await asyncio.sleep(0.1)

                r, w = await asyncio.open_connection("127.0.0.1", port)

                w.write(b"!broadcast\n")
                await w.drain()
                msg = await asyncio.wait_for(r.readline(), timeout=2)
                assert msg.decode().strip() == "1: !broadcast"

                w.close()
                server.close()

        try:
            asyncio.run(run())
        finally:
            task5_mod.TIMEOUT = original_timeout
