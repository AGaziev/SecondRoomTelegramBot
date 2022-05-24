from repositories.database import db
import logging

def getSellersID() -> list:
    try:
        sellers = list(db.child('sellers').child('sideSellers').get().val().keys())
    except AttributeError:
        sellers = []
    return sellers


def addSeller(sellerId):
    db.child('sellers').child('sideSellers').update({sellerId: ''})


def deleteSeller(sellerId, sellerName=None):
    db.child('sellers').child('sideSellers').child(sellerId).remove()
    logging.info(f'{sellerName if sellerName is not None else sellerId} not more sideSeller')
