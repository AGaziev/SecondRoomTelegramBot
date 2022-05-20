from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

try:
    fsm = MemoryStorage()
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher(bot, storage=fsm)
except Exception as e:
    print(e)
else:
    print('Bot successfully authorized')