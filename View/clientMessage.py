from aiogram import types

import View.Templates.clientTemplates as templates
from repositories.bot import bot


async def info(userId):
    await bot.send_message(userId, text=templates.info)


async def start(userId, startKeyboard):
    await bot.send_message(userId,
                           text='Привет, это бот-каталог вещей магазина SecondRoom',
                           reply_markup=startKeyboard)


async def catalogOpen(userId, categoryInfo, categoryKeyboard, noveltyInfo):
    await bot.send_message(userId, 'Открываю каталог', reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(userId,
                           templates.getCategoryMenu(categoryInfo, noveltyInfo),
                           reply_markup=categoryKeyboard)


async def subcategoryChoose(message: types.Message, subcategoryInfo, subcategoryKeyboard, noveltyInfo, backed=False):
    if not backed:
        await message.edit_text(
            text=templates.getSubcategoryMenu(subcategoryInfo, noveltyInfo),
            reply_markup=subcategoryKeyboard)
    else:
        await bot.send_message(message.chat.id,
                               text=templates.getSubcategoryMenu(subcategoryInfo, noveltyInfo),
                               reply_markup=subcategoryKeyboard)


async def startClothShow(userId, flipperKeyboard):
    await bot.send_message(userId, 'Вывод вещей по выбранной категории',
                           reply_markup=flipperKeyboard)


async def showClothAndReturnMessages(userId, cloth, currentClothCount, totalAmountOfClothes):
    return await bot.send_media_group(chat_id=userId,
                                      media=templates.createMediaGroup(cloth, currentClothCount, totalAmountOfClothes))


async def toStart(userId):
    await bot.send_message(userId, templates.toStart)


async def backing(userId):
    await bot.send_message(userId, 'Возвращаюсь...', reply_markup=types.ReplyKeyboardRemove())
