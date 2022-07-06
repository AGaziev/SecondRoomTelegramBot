import logging
from datetime import date

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from Model.cloth import clothManager, categoriesInfo
from Model.keyboard import adminKeyboardCreator
from Model.users import adminController
from View import adminMessage as sender


class FSMAdmin(StatesGroup):
    category = State()
    subCategory = State()
    brand = State()
    name = State()
    price = State()
    size = State()
    condition = State()
    photo = State()
    GroupStates = {
        'addCloth': [category, subCategory, brand, name, price, size, condition, photo]
    }


# @dp.message_handler(Text(equals='отмена', ignore_case=True),
#                     commands='отмена',
#                     state=FSMAdmin.GroupStates['addCloth'])
async def cancelAdd(message: types.Message, state: FSMContext):
    if adminController.authorization(message.from_user.id):
        logging.info(f'{message.chat.id} exit admin panel')
    await message.reply('Отмена')
    await state.finish()


# @dp.message_handler(commands=['admin'], state=None)
async def admLogin(message: types.Message = None, returnAdminId=None, loggedAlready=False):
    if message is not None:
        returnAdminId = message.from_user.id
    if not loggedAlready:
        authorized = adminController.authorization(
            returnAdminId)  # if not administrator -> False, else -> adminUsername
    else:
        authorized = True
    if authorized:
        await sender.onAdminPanelEnter(returnAdminId,
                                       adminKeyboardCreator.panel)
        logging.info(f'{authorized} entered admin panel')
    else:
        await sender.adminPanelReject(returnAdminId)


# @dp.callback_query_handler(text='addCloth')
async def startAdding(call: types.CallbackQuery):
    logging.info(f'{adminController.authorization(call.from_user.id)} started to add new Cloth')

    await sender.chooseCategory(call, adminKeyboardCreator.category)
    await FSMAdmin.category.set()


async def chooseSubCategory(message: types.Message, state: FSMContext):
    await addPropertyToCloth(state, 'category', message.text)
    await sender.chooseSubCategory(message, adminKeyboardCreator.getSubCategoryKeyboard(message.text))
    await FSMAdmin.next()


# @dp.message_handler(state=FSMAdmin.subCategory)
async def chooseBrand(message: types.Message, state: FSMContext):
    await addPropertyToCloth(state, 'subCategory', message.text)
    await sender.chooseProperty(message, 'бренд', isOptional=True)
    await FSMAdmin.next()


# @dp.message_handler(state=FSMAdmin.brand)
async def chooseName(message: types.Message, state: FSMContext):
    await addPropertyToCloth(state, 'brand', message.text, 'NONAME')
    await sender.chooseProperty(message, 'название', isOptional=True)
    await FSMAdmin.next()


# @dp.message_handler(state=FSMAdmin.name)
async def choosePrice(message: types.Message, state: FSMContext):
    await addPropertyToCloth(state, 'name', message.text)
    await sender.chooseProperty(message, 'цену', isOptional=True)
    await FSMAdmin.next()


# @dp.message_handler(state=FSMAdmin.price)
async def chooseSize(message: types.Message, state: FSMContext):
    await addPropertyToCloth(state, 'price', message.text)
    await sender.chooseProperty(message, 'размер')
    await FSMAdmin.next()


# @dp.message_handler(state=FSMAdmin.size)
async def chooseCondition(message: types.Message, state: FSMContext):
    await addPropertyToCloth(state, 'size', message.text)
    await sender.chooseProperty(message, 'состояние', propertyKeyboard=adminKeyboardCreator.condition)
    await FSMAdmin.next()


# @dp.message_handler(state=FSMAdminAdd.condition)
async def choosePhoto(message: types.Message, state: FSMContext):
    await addPropertyToCloth(state, 'condition', message.text)
    await sender.waitForPhoto(message)
    async with state.proxy() as data:
        data['photo'] = []
    await FSMAdmin.next()


# @dp.message_handler(Text(equals='-'), state=FSMAdmin.photo)
async def deletePhoto(message: types.Message, state: FSMContext):
    await deleteLastPhoto(message, state)
    await sender.waitForPhoto(message, adminKeyboardCreator.isLastPhoto)

# @dp.message_handler(content_types = ['photo'], state=FSMAdmin.photo)
async def endAddingCloth(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'].append(message.photo[0].file_id)
    await sender.endAddingPhoto(message, adminKeyboardCreator.isLastPhoto)


# @dp.callback_query_handler(state=FSMAdmin.photo,text='returnToPanel')
async def returnToAdminPanel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        data['user'] = callback.from_user.mention
        data['userId'] = callback.from_user.id
        data['date'] = str(date.today())
        if adminController.authorization(callback.from_user.id):
            try:
                await sender.postNewClothInChannel(data)
            except Exception as e:
                logging.error('Post in general channel rejected by ' + e)
        clothManager.addClothToDB(data)
    await state.finish()
    await admLogin(returnAdminId=callback.from_user.id)


async def addPropertyToCloth(state: FSMContext, nameOfProperty, propertyInfo, alternativePropertyInfo='None'):
    async with state.proxy() as data:
        if propertyInfo != '-':
            data[nameOfProperty] = propertyInfo
        else:
            data[nameOfProperty] = alternativePropertyInfo


async def deleteLastPhoto(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            print(data['photo'])
            lastPhoto = data['photo'][-1]
            del data['photo'][-1]
            print(data['photo'])
        except:
            lastPhoto = False
    await sender.deletePhoto(lastPhoto, message.from_user.id)


def registerHandlers(dp):
    # cancel state handlers
    dp.register_message_handler(cancelAdd, commands='отмена', state=FSMAdmin.GroupStates['addCloth'])
    dp.register_message_handler(cancelAdd, Text(equals='отмена', ignore_case=True),
                                state=FSMAdmin.GroupStates['addCloth'])
    # admin panel handler
    dp.register_message_handler(admLogin, commands=['admin'])
    # add cloth handlers
    dp.register_callback_query_handler(startAdding, text='addCloth')
    dp.register_message_handler(chooseSubCategory,
                                Text(equals=categoriesInfo.getCategories().keys(), ignore_case=False),
                                state=FSMAdmin.category)
    dp.register_message_handler(chooseBrand, state=FSMAdmin.subCategory)
    dp.register_message_handler(chooseName, state=FSMAdmin.brand)
    dp.register_message_handler(choosePrice, state=FSMAdmin.name)
    dp.register_message_handler(chooseSize, state=FSMAdmin.price)
    dp.register_message_handler(chooseCondition, state=FSMAdmin.size)
    dp.register_message_handler(choosePhoto, state=FSMAdmin.condition)
    dp.register_callback_query_handler(returnToAdminPanel, state=FSMAdmin.photo, text='returnToPanel')
    dp.register_message_handler(endAddingCloth, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(deletePhoto, Text(equals='-'), state=FSMAdmin.photo)
    ###
    logging.info('admin handlers registered')
