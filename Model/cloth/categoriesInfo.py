import logging

from repositories.database import db


def getCategories() -> dict:
    try:
        categoryList = dict(db.child('categories').get().val())
    except TypeError:
        categoryList = {}
    return categoryList


def getMainCategoryCount(category) -> int:
    categoryCount = 0
    countersOfCategory = db.child('categories').child(category).get().each()
    if countersOfCategory is not None:
        for subCategoryCounter in countersOfCategory:
            categoryCount += subCategoryCounter.val()
    return categoryCount


def getNumberOfClothes(category, subCategory, justCheck=False) -> int:
    clothes = db.child('CLOTHES').child(category).child(subCategory).get().each()
    if clothes is not None:
        count = len(clothes)
    else:
        count = 0
    if not justCheck:
        db.child('categories').child(category).child(subCategory).set(count)
    return count


def updateAllClothesCounter():
    clothesCount = 0
    for category in getCategories().keys():
        clothesCount += getMainCategoryCount(category)
    db.child('statistics/counterOfItemsInStore').set(clothesCount)
    logging.info('Updated Counter of all clothes')
    return clothesCount


def totalUpdate():
    for cat, subcat in getCategories().items():
        for sub in subcat.keys():
            getNumberOfClothes(cat, sub)
    updateAllClothesCounter()


def categoriesWithNew(id):  # get categories with new items
    id = str(id)
    catsWithNew = []
    indicatorsForId = db.child('userInfo').child(id).child('noveltyCheck').get().val()
    for cat, subCatDict in indicatorsForId.items():
        if True in subCatDict.values():
            catsWithNew.append(cat)
    return catsWithNew


def subcatWithNew(id, category):  # get subcategories with new items
    id = str(id)
    subCatsWithNew = []
    indicatorsForId = db.child('userInfo').child(id).child('noveltyCheck').child(category).get().val()
    for subCat, isNew in indicatorsForId.items():
        if isNew:
            subCatsWithNew.append(subCat)
    return subCatsWithNew
