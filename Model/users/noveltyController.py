from Model.cloth import categoriesInfo
from repositories.database import db


def setNoveltyToUsers(category, subCategory, novelty):
    listOfUsersId = db.child('userInfo').get().val().keys()
    for userId in listOfUsersId:
        db.child(f'userInfo/{userId}/noveltyCheck/{category}/{subCategory}').set(novelty)


def notNewAnymore(id, category, subCategory):  # falsing new for subcategory
    db.child('userInfo').child(id).child('noveltyCheck').child(category).child(subCategory).set(False)


def listForNewUser():  # get list for new users depended on clothes counters (false if no cloth in subcategory
    categoryNovelties = {}
    for category, subCategory in categoriesInfo.getCategories().items():
        subNovelties = {}
        for sub in subCategory.keys():
            subNovelties[sub] = bool(subCategory[sub])
        categoryNovelties[category] = subNovelties
    return categoryNovelties
