from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from Model.cloth import categoriesInfo

panelButs = [
    'Каталог',
    'Информация'
]

panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(
    *(KeyboardButton(text) for text in panelButs))

category: InlineKeyboardMarkup = InlineKeyboardMarkup().add(
    *(InlineKeyboardButton(text, callback_data=text) for text in categoriesInfo.getCategories().keys()))


def getSubCategoryKeyboard(categoryForSearch) -> InlineKeyboardMarkup:
    subcategoriesToShow = []
    for sub, count in categoriesInfo.getCategories()[categoryForSearch]:
        if count > 0:
            subcategoriesToShow.append(sub)
    return InlineKeyboardMarkup().add(
        *(InlineKeyboardButton(subName, callback_data=subName) for subName in
          subcategoriesToShow)
    )
