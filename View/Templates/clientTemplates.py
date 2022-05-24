info = 'Главный - @biruytskovskynf\n ' \
       'Если заметили некорректную работу бота, пишите - @vcdddk'


def getCategoryMenu(categoryInfo: dict, noveltyInfo: dict):
    text = 'Количество вещей в каждой категории\n\n'
    for category in categoryInfo.keys():
        text += f'{category} - {categoryInfo[category]}{" NEW!" if category in noveltyInfo else ""}\n'
    text += '\nВыберите категорию'
    return text
