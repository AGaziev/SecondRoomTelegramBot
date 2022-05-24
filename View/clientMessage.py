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