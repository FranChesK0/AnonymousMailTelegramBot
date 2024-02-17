import asyncio

from storages.redis_tools import redis


async def main() -> None:
    await redis.aclose()


if __name__ == "__main__":
    asyncio.run(main())
