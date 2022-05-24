from aiogram import types

import View.adminTemplates as adminTemplates
from repositories.bot import bot


async def onAdminPanelEnter(adminId: int, keyboard: types.InlineKeyboardMarkup):
    await bot.send_message(chat_id=adminId,
                           text=adminTemplates.adminGreeting,
                           reply_markup=keyboard)


async def adminPanelReject(adminId: int):
    await bot.send_message(chat_id=adminId,
                           text=adminTemplates.authorizationRejection)


async def chooseCategory(callback: types.CallbackQuery, categoryKeyboard: types.ReplyKeyboardMarkup):
    await callback.message.edit_text('Добавление вещи...')
    await bot.send_message(chat_id=callback.from_user.id,
                           text='Выберите категорию',
                           reply_markup=categoryKeyboard)
    await callback.answer('start adding new cloth', show_alert=False)


async def chooseSubCategory(message: types.Message, subCategoryKeyboard):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Выберите подкатегорию',
                           reply_markup=subCategoryKeyboard)


async def chooseProperty(message: types.Message, nameOfProperty, propertyKeyboard=types.ReplyKeyboardRemove(),
                         isOptional=False):
    await bot.send_message(chat_id=message.from_user.id,
                           text=adminTemplates.getTextForPropertyRequest(nameOfProperty, isOptional),
                           reply_markup=propertyKeyboard)


async def waitForPhoto(message: types.Message, endAddingKeyboard=types.ReplyKeyboardRemove()):
    await bot.send_message(message.from_user.id,
                           'Загрузите фото',
                           reply_markup=endAddingKeyboard)


async def deletePhoto(photoId: bool | str, chatId):
    if photoId is False:
        await bot.send_message(chatId, 'Еще ни одного фото не было добавлено')
    else:
        await bot.send_photo(chatId,
                             photoId,
                             caption='Было удалено фото:')


async def endAddingPhoto(message: types.Message, endAddingKeyboard):
    await bot.send_message(message.from_user.id,
                           'Фото добавлено. Ещё фото?',
                           reply_markup=endAddingKeyboard)


async def postNewClothInChannel(clothInfo: dict):
    await bot.send_media_group(adminTemplates.channelIdForPosting,
                               media=adminTemplates.createMediaGroupForPost(clothInfo))
