from aiogram import Dispatcher

from .outer import middlewares_setup as outer_middlewares


def setup(dispatcher: Dispatcher) -> None:
    for middleware_setup in outer_middlewares:
        middleware_setup(dispatcher)


__all__ = ["setup"]
