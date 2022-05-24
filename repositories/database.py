import logging

from pyrebase import pyrebase

import config

try:
    firebase = pyrebase.initialize_app(config.FIREBASE_CONFIG)
    db = firebase.database()
    storage = firebase.storage()
except Exception as e:
    logging.error(e)
else:
    logging.info('dbRepository successfully authorized')
