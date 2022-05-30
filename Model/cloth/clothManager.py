import logging

from Model.users import noveltyController
from .categoriesInfo import getNumberOfClothes, updateAllClothesCounter
from repositories.database import db

showInfo = ['subCategory', 'brand', 'name', 'price', 'condition', 'photo', 'size', 'user', 'userId', 'date']


def addClothToDB(data):
    logging.info(
        f'Adding new cloth in base {data["category"]},{data["subCategory"]} with name: {data["brand"]} \"{data["name"]}\"')

    db.child('CLOTHES').child(data['category']).child(data['subCategory']).push(
        {k: v for k, v in data.items() if k in showInfo})

    getNumberOfClothes(data['category'], data['subCategory'])
    noveltyController.setNoveltyToUsers(data['category'], data['subCategory'], True)
    updateAllClothesCounter()


def deleteClothFromDB(category, subCategory, clothId):
    logging.info(
        f'Deleting cloth from base {category}, {subCategory} with id: {clothId}')
    db.child('CLOTHES').child(category).child(subCategory).child(clothId).remove()
    count = getNumberOfClothes(category, subCategory)
    if count == 0:
        noveltyController.setNoveltyToUsers(category, subCategory, False)
    updateAllClothesCounter()


def getClothesList(category, subCategory) -> dict:
    clothesList = db.child('CLOTHES').child(category).child(subCategory).get().val()
    if clothesList is None:
        return {}
    else:
        return clothesList
