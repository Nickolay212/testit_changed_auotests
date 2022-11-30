from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class MongoDbConfig:
    host: str
    port: int


@dataclass
class TestitConfig:
    token: str
    url: str


@dataclass
class TgBot:
    token: str
    #admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBot
    mongodb: MongoDbConfig
    testit: TestitConfig


#admin_ids=list(map(int, env.list("ADMINS"))),
def load_config():
    return Config(
        tg_bot=TgBot(
            token=os.getenv('TOKEN'),
        ),
        mongodb=MongoDbConfig(
            host=os.getenv('host'),
            port=int(os.getenv('port')),
        ),
        testit=TestitConfig(
            token=os.getenv('private_token_testit'),
            url=os.getenv('url_testit')
        )
    )
