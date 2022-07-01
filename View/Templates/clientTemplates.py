from aiogram import types

import emoji
import datetime

info = 'Главный - @biruytskovskynf\n ' \
       'Если заметили некорректную работу бота, пишите - @vcdddk'

toStart = 'Введите /start для открытия контекстного меню'

def getCategoryMenu(categoryInfo: dict, noveltyInfo: dict):
    newEmoji = '🆕'
    text = 'Количество вещей в каждой категории\n\n'
    for category in categoryInfo.keys():
        text += f'{category} - {categoryInfo[category]}{f" {newEmoji}" if category in noveltyInfo else ""}\n'
    text += '\nВыберите категорию'
    return text


def getSubcategoryMenu(subcategoryInfo: dict, noveltyInfo: dict):
    start = 'Количество вещей в каждой подкатегории\n\n'
    text = ''
    for subcategory in subcategoryInfo.keys():
        if subcategoryInfo[subcategory] != 0:
            text += f'{subcategory} - {subcategoryInfo[subcategory]}{" 🆕" if subcategory in noveltyInfo else ""}\n'

    if text == '':
        text = 'Нет вещей в выбранной категории'
    else:
        text += '\nВыберите категорию'
    return start + text


def createMediaGroup(cloth, current, total):
    media = types.MediaGroup()
    for i in range(len(cloth['photo'])):
        media.attach_photo(
            types.InputMediaPhoto(cloth['photo'][i],
                                  caption=getClothInfoForBot(cloth, current, total) if i == 0 else '',
                                  parse_mode=types.ParseMode.HTML))
    return media


def getClothInfoForBot(data: dict, current, total):
    try:                    # splitting dd-mm-yyyy
        if getDataDifference(data['date'].split('-')) < 3:
            dateText = ' 🆕'
        else:
            dateText = ''
    except:
        dateText = ''
    try:
        userMention = f"<a href=\"tg://user?id={data['userId']}\">{data['user']}</a>"
    except:
        userMention = data['user']
    name = (f'\"{data["name"]}\"' if data["name"] != 'None' else '')
    return f'{current}/{total}\n' \
           f'{data["subCategory"]}{dateText}\n' \
           f'{data["brand"]} {name}\n\n' \
           f'{data["price"]}\n\n' \
           f'Состояние: {data["condition"]}\n' \
           f'Размер: {data["size"]}\n' \
           f'За покупкой {userMention}'


def getDataDifference(date):
    date = list(map(int, date))
    return (datetime.date.today() - datetime.date(*date)).days
