from typing import Any, Callable, Optional, Awaitable

from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import User, TelegramObject

from bot.languages import Text, LocalizedTranslator
from storages.redis_tools import get_keys, get_value, set_value


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(
        self, limit: Optional[int] = None, lifetime: Optional[int] = None
    ) -> None:
        self._limit = limit or 2
        self._lifetime = lifetime or 1

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        bot: Bot = data["bot"]
        user: User = data["event_from_user"]
        translator: LocalizedTranslator = data["translator"]

        count_key = f"thr-count-{user.id}"
        user_key = f"thr-{user.id}"

        user_key_number = len(await get_keys(f"{user_key}-*"))
        if user_key_number >= self._limit:
            await bot.send_message(user.id, text=translator.get(Text.THROTTLING_MESSAGE))
            return

        count = await get_value(count_key)
        if count is None:
            count = 0

        await set_value(f"{user_key}-{count}", 1, expire=self._lifetime)
        await set_value(count_key, count + 1, expire=self._lifetime)

        return await handler(event, data)


def setup(dispatcher: Dispatcher) -> None:
    dispatcher.update.outer_middleware(ThrottlingMiddleware())
