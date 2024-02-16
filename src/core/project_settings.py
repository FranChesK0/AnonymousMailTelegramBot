import os
import sys

from pydantic_settings import BaseSettings, SettingsConfigDict

project_directory = os.path.dirname(os.path.abspath(__file__)).removesuffix(
    os.path.join("src", "core")
)


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(project_directory, ".env"), env_prefix="BOT_"
    )

    token: str = "xxx"


class Settings(BaseSettings):
    project_directory: str = project_directory
    debug: bool = "-d" in sys.argv or "--debug" in sys.argv
    bot: BotSettings = BotSettings()


settings = Settings()
