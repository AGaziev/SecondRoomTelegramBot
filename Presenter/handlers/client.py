# TODO CLIENT HANDLER

usedCommands = ['/start', '/help', '/login', '/admin']

subCategories = ['Кроссовки', 'Кеды', 'Тапки', 'Худи', 'Свитшот', 'Флиска', 'T-shirt', 'Майка', 'Куртка', 'Пальто',
                 'Бомбер', 'Спортивные', 'Обычные']


class FSMClient(StatesGroup):
    defualtClient = State()
    categorySelect = State()
    subCategorySelect = State()
    showClothes = State()

def registerHandlers(dp):
    pass