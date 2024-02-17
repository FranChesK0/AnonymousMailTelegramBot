from typing import Any, Protocol, NamedTuple

import aiohttp

from core import settings
from services.mail import Mailbox, Message


class _RequestParameter(Protocol):
    @property
    def url(self) -> str:
        raise NotImplementedError


class _GenRandomMailbox(NamedTuple):
    count_: int

    @property
    def url(self) -> str:
        return f"{settings.mail.api}?action=genRandomMailbox&count={self.count_}"


class _GetMessages(NamedTuple):
    mail: Mailbox

    @property
    def url(self) -> str:
        return (
            f"{settings.mail.api}"
            f"?action=getMessages"
            f"&login={self.mail.login}"
            f"&domain={self.mail.domain}"
        )


class _ReadMessage(NamedTuple):
    mail: Mailbox
    message_id: int

    @property
    def url(self) -> str:
        return (
            f"{settings.mail.api}"
            f"?action=readMessage"
            f"&login={self.mail.login}"
            f"&domain={self.mail.domain}"
            f"&id={self.message_id}"
        )


async def get_mailbox() -> Mailbox:
    """
    :return: random mailbox.
    """
    response = await _get_response(_GenRandomMailbox(count_=2))
    login, domain = response[0].split("@")
    return Mailbox(login=login, domain=domain)


async def get_messages(mail: Mailbox) -> list[int]:
    """
    :param mail: a mail to check for messages.
    :return: a list of message ids.
    """
    response = await _get_response(_GetMessages(mail=mail))
    return [message.get("id", -1) for message in response]


async def read_message(mail: Mailbox, message_id: int) -> Message:
    """
    :param mail: a mail from which to get the message.
    :param message_id: id of the message.
    :return: message from the mail.
    """
    response = await _get_response(_ReadMessage(mail=mail, message_id=message_id))
    return Message.model_validate(response)


async def _get_response(request_parameters: _RequestParameter) -> Any:
    async with aiohttp.ClientSession() as session:
        async with session.get(request_parameters.url) as response:
            return await response.json()
