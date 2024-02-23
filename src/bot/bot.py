from aiogram import Bot, Dispatcher

from core import settings
from bot.handlers import router as handlers_router
from bot.languages import Translator
from bot.middlewares import setup as setup_middlewares


async def run() -> None:
    bot = Bot(settings.bot.token, parse_mode="HTML")
    dispatcher = Dispatcher()

    setup_middlewares(dispatcher)
    dispatcher.include_routers(handlers_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, translator=Translator())
