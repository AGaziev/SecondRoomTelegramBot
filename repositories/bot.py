from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import os

import config

fsm = MemoryStorage()

try:
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(bot, storage=fsm)
except:
    logging.critical('Произошла ошибка при авторизации токена')