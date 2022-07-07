import logging
from Model.model import *
from repositories.database import db

def getCategories() -> dict:
    with db:
        subInfo = Subcategory.select(Subcategory.title.alias('sub'),
                                     Category.title.alias('cat'),
                                     fn.Count(Cloth.id != 'None').alias('c')) \
            .join(Category) \
            .left_outer_join(Cloth, on=Cloth.subcategory == Subcategory.id).group_by(Subcategory.id).dicts()
    categoryList = {k.title: {} for k in Category.select(Category.title)}
    for i in subInfo:
        categoryList[i['cat']].update({i['sub']: i['c']})
    return categoryList

def getInfoAboutCategories() -> dict:
    categoriesInfo = {}
    for category, subsInfo in getCategories().items():
        categoriesInfo[category] = sum(subsInfo.values())
    return categoriesInfo

# TODO DELETE
# def getMainCategoryCount(category) -> int:
#     categoryCount = 0
#     countersOfCategory = db.child('categories').child(category).get().each()
#     if countersOfCategory is not None:
#         for subCategoryCounter in countersOfCategory:
#             categoryCount += subCategoryCounter.val()
#     return categoryCount


def getNumberOfClothes(category, subCategory) -> int:
    return getCategories()[category][subCategory]

#TODO after novelty creator
def categoriesWithNew(id):  # get categories with new items
    id = str(id)
    catsWithNew = []
    indicatorsForId = db.child('userInfo').child(id).child('noveltyCheck').get().val()
    for cat, subCatDict in indicatorsForId.items():
        if True in subCatDict.values():
            catsWithNew.append(cat)
    return catsWithNew

#TODO after novelty creator
def subcatWithNew(id, category):  # get subcategories with new items
    id = str(id)
    subCatsWithNew = []
    indicatorsForId = db.child('userInfo').child(id).child('noveltyCheck').child(category).get().val()
    for subCat, isNew in indicatorsForId.items():
        if isNew:
            subCatsWithNew.append(subCat)
    return subCatsWithNew
