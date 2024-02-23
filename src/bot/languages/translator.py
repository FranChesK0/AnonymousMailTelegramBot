import os
from typing import Any

# TODO: Remove ignore when stubs will be added to fluentogram
#  (2 imports and __init__ argument)
from fluentogram import (  # type: ignore[import-untyped]
    TranslatorHub,
    FluentTranslator,
    TranslatorRunner,
)
from fluent_compiler.bundle import FluentBundle  # type: ignore[import-untyped]

from core import settings

locales_dir = os.path.join(settings.project_directory, "resources", "locales")


class Translator:
    def __init__(self) -> None:
        self._t_hub = TranslatorHub(
            locales_map={"ru": ("ru", "en"), "en": ("en",)},
            translators=[
                FluentTranslator(
                    locale="en",
                    translator=FluentBundle.from_files(
                        locale="en-US",
                        filenames=[os.path.join(locales_dir, "en.ftl")],
                    ),
                ),
                FluentTranslator(
                    locale="ru",
                    translator=FluentBundle.from_files(
                        locale="ru-RU",
                        filenames=[os.path.join(locales_dir, "ru.ftl")],
                    ),
                ),
            ],
            root_locale="en",
        )

    def __call__(self, locale: str) -> "LocalizedTranslator":
        return LocalizedTranslator(
            translator=self._t_hub.get_translator_by_locale(locale=locale)
        )


class LocalizedTranslator:
    def __init__(  # type: ignore[no-any-unimported]
        self, translator: TranslatorRunner
    ) -> None:
        self._translator = translator

    def get(self, key: str, **kwargs: Any) -> str:
        return str(self._translator.get(key, **kwargs))
