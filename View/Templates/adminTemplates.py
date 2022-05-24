import os

from aiogram import types

channelIdForPosting = os.getenv("SHOP_CHANNEL_ID")

adminGreeting = 'Успешный вход на панель админа'

authorizationRejection = 'Недостаточно прав'


def getTextForPropertyRequest(name, isOptional=False):
    text = f'Напишите {name}'
    if isOptional:
        text += '(\'-\' для пропуска)'
    return text


def getClothInfoForChannel(data: dict):
    userMention = f"<a href=\"tg://user?id={data['userId']}\">{data['user']}</a>"
    name = (f'\"{data["name"]}\"' if data["name"] != 'None' else '')
    return f'{data["brand"]}\n\n' \
           f'{data["subCategory"]} {name}\n\n' \
           f'{data["size"]}\n\n' \
           f'{data["price"]}\n\n' \
           f'За покупкой {userMention}'


def createMediaGroupForPost(clothInfo: dict):
    media = types.MediaGroup()
    for i in range(len(clothInfo['photo'])):
        media.attach_photo(photo=types.InputMediaPhoto(clothInfo['photo'][i],
                                                       caption=getClothInfoForChannel(clothInfo) if i == 0 else '',
                                                       parse_mode=types.ParseMode.HTML))
    return media
