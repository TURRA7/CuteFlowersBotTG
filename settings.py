from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    dbname: str
    user: str
    password: str
    host: str


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int('ADMIN_ID'),
            dbname=env.str("dbname"),
            user=env.str("user"),
            password=env.str("password"),
            host=env.str("host"),
        )
    )


settings = get_settings('input')
