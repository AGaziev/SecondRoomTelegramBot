import logging
import datetime

from aiogram import types

from .noveltyController import listForNewUser
from repositories.database import db

def checkUserRegistration(userId, message: types.Message):  # check if user used a bot
    if str(userId) not in list(getRegisteredUsers()):
        registerUser(userId, message.from_user.values)
        return False
    else:
        return True


def registerUser(userId, info: dict):
    noveltyListForNewUser = listForNewUser()
    db.child('userInfo').child(userId).child('noveltyCheck').set(noveltyListForNewUser)
    db.child('userInfo').child(userId).update({'info': info})
    db.child('userInfo').child(userId).update({'dateOfRegistration': datetime.datetime.now()})
    logging.info(f'New user registered to bot with id: {userId}')


def getRegisteredUsers():
    try:
        registeredId = db.child('userInfo').get().val().keys()
    except AttributeError:
        registeredId = []
    return registeredId
