from repositories.database import db


def authorization(adminId):
    admins = getAdmin()
    if adminId in admins.keys():
        return admins[adminId]
    else:
        return False


def getAdmin() -> dict:
    admins = {}
    try:
        tempAdmins = Use
    except TypeError:
        tempAdmins = {}
    for id, name in tempAdmins.items():
        admins[int(id)] = name
    return admins
