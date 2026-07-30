import asyncio

TIMEOUT = 5

writers = set()


async def handle_client(reader, writer):
    raise NotImplementedError


async def main(host, port):
    raise NotImplementedError


if __name__ == "__main__":
    asyncio.run(main("localhost", 8080))
