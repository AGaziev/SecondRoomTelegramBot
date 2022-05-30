from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from Model.cloth import categoriesInfo
from Model.users.adminController import authorization

panelButs = [
    'Каталог',
    'Информация'
]

backBut = [
    ('Назад', 'back')
]

flipperButs = ['<<', 'Назад', '>>']

flipperAdminButs = ['Удалить']

panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(
    *(KeyboardButton(text) for text in panelButs))

category: InlineKeyboardMarkup = InlineKeyboardMarkup().add(
    *(InlineKeyboardButton(text, callback_data=text) for text in categoriesInfo.getCategories().keys())).add(
    *(InlineKeyboardButton(text, callback_data=data) for text, data in backBut))

flipper: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(
    *(KeyboardButton(text) for text in flipperButs))


def getSubCategoryKeyboard(categoryForSearch) -> InlineKeyboardMarkup:
    subcategoriesToShow = []
    for sub, count in categoriesInfo.getCategories()[categoryForSearch].items():
        if count > 0:
            subcategoriesToShow.append(sub)
    return InlineKeyboardMarkup().add(
        *(InlineKeyboardButton(subName, callback_data=subName) for subName in
          subcategoriesToShow)).add(
        *(InlineKeyboardButton(text, callback_data=data) for text, data in backBut))


def getFlipperKeyboard(clientId):
    flipperKb = ReplyKeyboardMarkup(flipper.keyboard, resize_keyboard=True, row_width=3)
    if authorization(clientId):
        flipperKb.add(*(KeyboardButton(text) for text in flipperAdminButs))
    return flipperKb
