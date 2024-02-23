from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from bot.languages import LocalizedTranslator

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, translator: LocalizedTranslator) -> None:
    await message.answer(text=translator.get("start_command"))


@router.message(Command(commands="help"))
async def help_command(message: Message, translator: LocalizedTranslator) -> None:
    await message.answer(text=translator.get("help_command"))
