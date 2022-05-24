from aiogram.utils import executor
from repositories.bot import dp
import datetime
import logging

from Presenter.handlers.handlerRegistrar import handlerRegistrate
from Model.cloth.categoriesInfo import totalUpdate


async def on_startup(_):
    print('Bot online!')
    logging.info('Bot online! timestamp:' + str(datetime.datetime.now()))


handlerRegistrate(dp)
totalUpdate()
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
