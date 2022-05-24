from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from Model.cloth import categoriesInfo

panelButs = [
    ('Добавить', 'addCloth')
]

endAddingPhotoButs = [
    ('Нет', 'returnToPanel')
]

conditionButs = [
    'Хорошее',
    'Отличное',
]

panel: InlineKeyboardMarkup = InlineKeyboardMarkup().add(
    *(InlineKeyboardButton(text, callback_data=data) for text, data in panelButs))

isLastPhoto: InlineKeyboardMarkup = InlineKeyboardMarkup().add(
    *(InlineKeyboardButton(text, callback_data=data) for text, data in endAddingPhotoButs))

category: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    *(KeyboardButton(text) for text in categoriesInfo.getCategories().keys()))

condition: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    *(KeyboardButton(text) for text in conditionButs))


def getSubCategoryKeyboard(categoryForSearch) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        *(KeyboardButton(text) for text in categoriesInfo.getCategories()[categoryForSearch])
    )

