import logging

import datetime
from Model.model import *
from Model.users import noveltyController
from .categoriesInfo import getNumberOfClothes
from repositories.database import db

showInfo = ['subCategory', 'brand', 'name', 'price', 'condition', 'photo', 'size', 'user', 'userId', 'date']


def addClothToDB(data):
    logging.info(
        f'Adding new cloth in base {data["category"]},{data["subCategory"]} with name: {data["brand"]} \"{data["name"]}\"')

    with db:
        clothData = Cloth(**data)  # brand, condition, size, price
        # seller id
        clothData.seller_id = User.get(User.telegram_id == data['userId']).id
        # name
        clothData.cloth_name = data.get('name')
        print(data.get('name'))
        # timestamp
        dateInfo = data.get('date', '2022-01-01')
        date = list(map(int, dateInfo.split('-')))
        clothData.timestamp = datetime.datetime(*date)
        # subcat, cat
        catId = Subcategory.get(Subcategory.title == data['subCategory']).of_category
        subcatId = Subcategory.get(Subcategory.title == data['subCategory']).id
        clothData.category = catId
        clothData.subcategory = subcatId
        #saving
        clothData.save()
        # photo
        for photoId in data['photo']:
            Photo.create(photoId=photoId, of_cloth_id=clothData.id)

    noveltyController.setNoveltyToUsers(data['category'], data['subCategory'], True)


def deleteClothFromDB(category, subCategory, clothId):
    logging.info(
        f'Deleting cloth from base {category}, {subCategory} with id: {clothId}')
    with db:
        Cloth.delete().where(Cloth.id == '1').execute()
    count = getNumberOfClothes(category, subCategory)
    if count == 0:
        noveltyController.setNoveltyToUsers(category, subCategory, False)


def getClothesList(category, subCategory):
    with db:
        clothesList = Cloth.select(Cloth.id,
                                   Cloth.brand,
                                   Cloth.condition,
                                   Cloth.cloth_name.alias('name'),
                                   Cloth.price,
                                   Cloth.size,
                                   Subcategory.title.alias('subCategory'),
                                   Category.title.alias('category')) \
            .left_outer_join(Category, on=Cloth.category == Category.id) \
            .left_outer_join(Subcategory, on=Cloth.subcategory == Subcategory.id) \
            .where(Category.title == category and Subcategory.title == subCategory).dicts()
    return list(clothesList)
