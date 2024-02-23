import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from core import logger
from services import mail
from bot.languages import Text, LocalizedTranslator
from storages.redis_tools import get_value, set_value

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, translator: LocalizedTranslator) -> None:
    await message.answer(text=translator.get(Text.START_COMMAND))


@router.message(Command(commands="help"))
async def help_command(message: Message, translator: LocalizedTranslator) -> None:
    await message.answer(text=translator.get(Text.HELP_COMMAND))


@router.message(Command(commands="mail"))
async def mail_command(message: Message, translator: LocalizedTranslator) -> None:
    user = message.from_user
    if user is None:
        logger.warning(f"Can't handle command mail with message: {message}")
        return

    mail_key = f"mail-{user.id}"

    if (mailbox := await get_value(mail_key)) is not None:
        message_number = await get_value(f"{mail_key}-number")
        await message.answer(
            text=translator.get(
                Text.MAIL_EXISTS, mailbox=mailbox.mail, message_number=str(message_number)
            )
        )
        return

    new_mailbox = await mail.get_mailbox()
    await set_value(mail_key, new_mailbox, expire=datetime.timedelta(minutes=45))
    await set_value(f"{mail_key}-number", 0, expire=datetime.timedelta(minutes=45))

    await message.answer(text=translator.get(Text.MAIL_CREATED, mailbox=new_mailbox.mail))
    logger.info(f"Created {new_mailbox=} for user={user.id}.")
