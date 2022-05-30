from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text, IDFilter

from View import clientMessage as sender
from Model.users import clientController, noveltyController, adminController
from Model.keyboard import clientKeyboardCreator
from Model.cloth import categoriesInfo, clothManager

usedCommands = ['/start', '/help', '/login', '/admin']


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


# @dp.callback_query_handler(text=['back'],state='*')
async def backCallback(callback: types.CallbackQuery, state: FSMContext):
    await back(callback.message, state)
    await callback.answer()


# @dp.message_handler(Text(equals='Назад', ignore_case=True),state='*')
async def back(message: types.Message, state: FSMContext):
    await sender.backing(message.chat.id)
    stateInfo = await state.get_state()
    if stateInfo == "FSMClient:showClothes":
        async with state.proxy() as show:
            await sender.subcategoryChoose(message,
                                           subcategoryInfo=categoriesInfo.getCategories()[show['category']],
                                           subcategoryKeyboard=clientKeyboardCreator.getSubCategoryKeyboard(
                                               show['category']),
                                           noveltyInfo=categoriesInfo.subcatWithNew(message.chat.id,
                                                                                    show['category']),
                                           backed=True)
            await FSMClient.previous()
    elif stateInfo == "FSMClient:subCategorySelect":
        await message.delete()
        await sender.catalogOpen(message.chat.id,
                                 noveltyInfo=categoriesInfo.categoriesWithNew(message.chat.id),
                                 categoryInfo=categoriesInfo.getInfoAboutCategories(),
                                 categoryKeyboard=clientKeyboardCreator.category)
        await FSMClient.previous()
    else:
        await state.finish()
        await start(message)


# @dp.message_handler(Text(equals='каталог', ignore_case=True))
async def catalogEvent(message: types.Message, backed=False):
    if not backed:
        clientController.checkUserRegistration(str(message.from_user.id), message)  # check if user used a bot
        # TODO CATALOG EVENT STATISTICS
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
    await sender.subcategoryChoose(callback.message,
                                   subcategoryInfo=categoriesInfo.getCategories()[show['category']],
                                   subcategoryKeyboard=clientKeyboardCreator.getSubCategoryKeyboard(show['category']),
                                   noveltyInfo=categoriesInfo.subcatWithNew(callback.from_user.id, show['category']))
    await FSMClient.next()


# @dp.callback_query_handler(text=subCategories, state=FSMClient.subCategorySelect)
async def showClothes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as show:
        # TODO SUBCATEGORIES STATISTICS INCR
        show['subCategory'] = callback.data
        noveltyController.notNewAnymore(callback.from_user.id, show['category'], show['subCategory'])
        show['clothes']: dict = dict(clothManager.getClothesList(show['category'], show['subCategory']))
        await sender.startClothShow(userId=callback.from_user.id,
                                    flipperKeyboard=clientKeyboardCreator.getFlipperKeyboard(callback.from_user.id))
        show['currentCloth'] = 0
        show['currentClothId'] = list(show['clothes'].keys())[show['currentCloth']]
        show['countOfCloths'] = categoriesInfo.getNumberOfClothes(show['category'], show['subCategory'])
        await sendCurrentCloth(callback.from_user.id, show)
        await FSMClient.next()


# @dp.message_handler(Text(equals=['<<', '>>']), state=FSMClient.showClothes)
async def getAnother(message: types.Message, state: FSMContext, afterDelete=False):
    async with state.proxy() as show:
        current = show['currentCloth']
        for msg in show['currentClothMessages']:
            await msg.delete()
        if message.text == '<<':
            show['currentCloth'] = await checkIter(current - 1, show['countOfCloths'])
        elif message.text == '>>':
            show['currentCloth'] = await checkIter(current + 1, show['countOfCloths'])
        await sendCurrentCloth(message.from_user.id, show)


# @dp.message_handler(IDFilter(adminId), Text(equals='удалить', ignore_case=True), state=FSMClient.showClothes)
async def deleteCloth(message: types.Message, state: FSMContext):
    async with state.proxy() as show:
        clothManager.deleteClothFromDB(show['category'], show['subCategory'], show['currentClothId'])
        show['clothes']: dict = dict(clothManager.getClothesList(show['category'], show['subCategory']))
        for msg in show['currentClothMessages']:
            await msg.delete()
        if show['countOfCloths'] == 1:
            await sender.subcategoryChoose(message,
                                           subcategoryInfo=categoriesInfo.getCategories()[show['category']],
                                           subcategoryKeyboard=clientKeyboardCreator.getSubCategoryKeyboard(
                                               show['category']),
                                           noveltyInfo=categoriesInfo.subcatWithNew(message.from_user.id,
                                                                                    show['category']),
                                           backed=True)
            await FSMClient.previous()
            return
        else:
            show['countOfCloths'] -= 1
            show['currentCloth'] = await checkIter(show['currentCloth'] - 1, show['countOfCloths'])
            await sendCurrentCloth(message.from_user.id, show)


# @dp.message_handler(lambda message: message not in usedCommands)
async def default(message: types.Message):
    await sender.toStart(message.chat.id)


async def sendCurrentCloth(userId, show):
    cloth = list(show['clothes'].values())[show['currentCloth']]
    show['currentClothId'] = list(show['clothes'].keys())[show['currentCloth']]
    show['currentClothMessages'] = \
        list(await sender.showClothAndReturnMessages(userId,
                                                     cloth=cloth,
                                                     currentClothCount=show['currentCloth'] + 1,
                                                     totalAmountOfClothes=show['countOfCloths']))


async def checkIter(current, total):
    if current < 0:
        return total - 1
    elif current == total:
        return 0
    else:
        return current


def registerHandlers(dp):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(catalogEvent, Text(equals='каталог', ignore_case=True))
    dp.register_message_handler(info, Text(equals='информация', ignore_case=True))
    dp.register_message_handler(back, Text(equals='Назад', ignore_case=True), state='*')
    dp.register_callback_query_handler(backCallback, text=['back', 'backToCat'], state='*')
    dp.register_message_handler(deleteCloth, IDFilter(adminController.getAdmin().keys()),
                                Text(equals='удалить', ignore_case=True),
                                state=FSMClient.showClothes)
    dp.register_callback_query_handler(subcategorySelect,
                                       text=categoriesInfo.getCategories().keys(),
                                       state=FSMClient.categorySelect)
    dp.register_callback_query_handler(showClothes, state=FSMClient.subCategorySelect)
    dp.register_message_handler(getAnother, Text(equals=['<<', '>>']), state=FSMClient.showClothes)
    dp.register_message_handler(default, lambda message: message not in usedCommands)
    # InitLogger.info('client handlers registered')
