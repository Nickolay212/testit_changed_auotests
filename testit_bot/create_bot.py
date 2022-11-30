from testit_bot.config import load_config

from aiogram import Bot, Dispatcher

from testit_bot.db.db import ConnectionMongoDBMotor
from testit_bot.testit.testit_client import TestitClient


config = load_config()

testit_client = TestitClient(url=config.testit.url,
                             private_token=config.testit.token)
connect_mongodb = ConnectionMongoDBMotor(host=config.mongodb.host,
                                         port=config.mongodb.port).connect_db()

bot = Bot(token=config.tg_bot.token)
dp = Dispatcher()
