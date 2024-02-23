from aiogram import Bot, Dispatcher

from core import settings
from bot.languages import Translator
from bot.middlewares import setup as setup_middlewares


async def run() -> None:
    bot = Bot(settings.bot.token, parse_mode="HTML")
    dispatcher = Dispatcher()

    setup_middlewares(dispatcher)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, translator=Translator())
