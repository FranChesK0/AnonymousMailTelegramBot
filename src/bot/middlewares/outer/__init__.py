from .translator import setup as translator_setup

middlewares_setup = [translator_setup]

__all__ = ["middlewares_setup"]
