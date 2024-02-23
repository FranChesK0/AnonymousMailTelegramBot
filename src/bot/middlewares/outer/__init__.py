from .translator import setup as translator_setup
from .throttling import setup as throttling_setup

middlewares_setup = [translator_setup, throttling_setup]

__all__ = ["middlewares_setup"]
