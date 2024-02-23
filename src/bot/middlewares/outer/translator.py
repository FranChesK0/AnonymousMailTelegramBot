from typing import Any, Callable, Awaitable

from aiogram import Dispatcher, BaseMiddleware
from aiogram.types import User, TelegramObject

from bot.languages import Translator


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User = data["event_from_user"]
        translator: Translator = data["translator"]

        data["translator"] = translator(locale=(user.language_code or "en"))
        return await handler(event, data)


def setup(dispatcher: Dispatcher) -> None:
    dispatcher.update.outer_middleware(TranslatorMiddleware())
