from aiogram.utils import executor
from repositories.bot import dp


async def on_startup(_):
    print('Bot online!')


from Presenter.handlers.handlerRegistrar import handlerRegistrate
from Model.cloth.categoriesInfo import totalUpdate

handlerRegistrate(dp)
totalUpdate()
print('bot online')
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)