from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_tokken: str
    admin_id: str
    database: str
    bot_name: str
    chat_id: str
    chat_name: str
    group_id: str
    group_name: str

@dataclass
class Settings:
    bots: Bots


def get_settigns(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_tokken=env.str("TOKKEN"),
            admin_id=env.str("ADMIN_ID"),
            database=env.str("DATABASE"),
            bot_name=env.str("BOT_NAME"),
            chat_id=env.str("CHAT_ID"),
            chat_name=env.str("CHAT_NAME"),
            group_id=env.str("GROUP_ID"),
            group_name=env.str("GROUP_NAME"),
        )
    )


settings = get_settigns(".env")
print(settings)
