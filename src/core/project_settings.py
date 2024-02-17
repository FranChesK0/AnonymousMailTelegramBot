import os
import sys

from pydantic_settings import BaseSettings, SettingsConfigDict

project_directory = os.path.dirname(os.path.abspath(__file__)).removesuffix(
    os.path.join("src", "core")
)


class MailSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(project_directory, ".env"), env_prefix="MAIL_"
    )

    api: str = "xxx"


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(project_directory, ".env"), env_prefix="BOT_"
    )

    token: str = "xxx"


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(project_directory, ".env"), env_prefix="REDIS_"
    )

    host: str = "xxx"
    port: int = 1000
    password: str = "xxx"
    db: int = 0


class Settings(BaseSettings):
    project_directory: str = project_directory
    debug: bool = "-d" in sys.argv or "--debug" in sys.argv
    mail: MailSettings = MailSettings()
    bot: BotSettings = BotSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
