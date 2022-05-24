from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.types import MediaGroup

from View import clientMessage as sender
from Model.users import clientController
from Model.keyboard import clientKeyboardCreator
from Model.cloth import categoriesInfo

usedCommands = ['/start', '/help', '/login', '/admin']

subCategories = ['Кроссовки', 'Кеды', 'Тапки', 'Худи', 'Свитшот', 'Флиска', 'T-shirt', 'Майка', 'Куртка', 'Пальто',
                 'Бомбер', 'Спортивные', 'Обычные']


class FSMClient(StatesGroup):
    defualtClient = State()
    categorySelect = State()
    subCategorySelect = State()
    showClothes = State()


# @dp.message_handler(Text(equals='информация', ignore_case=True))
async def info(message: types.Message):
    await sender.info(message.chat.id)


# @dp.message_handler(commands=['start','help'])
async def start(message: types.Message):
    await sender.start(message.chat.id, clientKeyboardCreator.panel)


# @dp.message_handler(Text(equals='каталог', ignore_case=True))
async def catalogEvent(message: types.Message):
    clientController.checkUserRegistration(str(message.from_user.id), message)  # check if user used a bot
    await sender.catalogOpen(message.from_user.id,
                             noveltyInfo=categoriesInfo.categoriesWithNew(message.from_user.id),
                             categoryInfo=categoriesInfo.getInfoAboutCategories(),
                             categoryKeyboard=clientKeyboardCreator.category)
    await FSMClient.categorySelect.set()


# @dp.callback_query_handler(text=['Обувь','Верх','Низ'], state=FSMClient.categorySelect)
async def subcategorySelect(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as show:
        show['category'] = callback.data
    await sender.subcategoryChoose(callback)
    # await callback.message.edit_text(
    #     text=getSubCategoryInfo(callback.data, str(callback.from_user.id)) + '\nВыберите подкатегорию',
    #     reply_markup=getSubCategoryKb(callback.data))
    await FSMClient.next()

def registerHandlers(dp):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(catalogEvent, Text(equals='каталог', ignore_case=True))
    dp.register_message_handler(info, Text(equals='информация', ignore_case=True))
    # dp.register_message_handler(back, Text(equals='Назад', ignore_case=True), state='*')
    # dp.register_callback_query_handler(backCallback, text=['back', 'backToCat'], state='*')
    # dp.register_message_handler(deleteCloth, IDFilter(getAdmin()), Text(equals='удалить', ignore_case=True),
    #                             state=FSMClient.showClothes)
    # dp.register_callback_query_handler(subcategorySelect, text=['Обувь', 'Верх', 'Низ'], state=FSMClient.categorySelect)
    # dp.register_callback_query_handler(showClothes, state=FSMClient.subCategorySelect)
    # dp.register_message_handler(getAnother, Text(equals=['<<', '>>']), state=FSMClient.showClothes)
    # dp.register_message_handler(default, lambda message: message not in usedCommands)
    # InitLogger.info('client handlers registered')
