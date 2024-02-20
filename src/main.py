import asyncio
from asyncio.exceptions import CancelledError

import bot
from core import logger
from storages.redis_tools import redis


async def main() -> None:
    try:
        await bot.run()
    except (CancelledError, KeyboardInterrupt):
        logger.info("Bot stopped.")
    except Exception as err:
        logger.error(f"ERROR: {err}")
    finally:
        await redis.aclose()


if __name__ == "__main__":
    asyncio.run(main())
