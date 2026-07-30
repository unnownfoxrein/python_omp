import asyncio


def virtualize(dir_path):
    raise NotImplementedError


async def getlist_handler(reader, writer, vfs):
    raise NotImplementedError


async def main(host, port, dir_path):
    raise NotImplementedError


if __name__ == "__main__":
    asyncio.run(main("localhost", 8080, "/tmp"))
