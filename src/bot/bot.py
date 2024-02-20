from aiogram import Bot, Dispatcher

from core import settings


async def run() -> None:
    bot = Bot(settings.bot.token, parse_mode="HTML")
    dispatcher = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)
