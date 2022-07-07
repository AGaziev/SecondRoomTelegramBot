import json
import logging
import os

from cryptocode import decrypt
from dotenv import load_dotenv

try:
    load_dotenv(__file__ + '/../.env.local')
except Exception as e:
    print(e)
    logging.error('no env file found')
else:
    logging.info('all variables have loaded to env')

FIREBASE_CONFIG = {
    'apiKey': os.getenv("FIREBASE_API_KEY"),
    'authDomain': os.getenv("FIREBASE_AUTH_DOMAIN"),
    'databaseURL': os.getenv("FIREBASE_DATABASE_URL"),
    'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET"),
    'serviceAccount': json.loads(
        decrypt(os.getenv("SERVICEACCOUNT_KEY"), os.getenv("SERVICEACCOUNT_PASSWORD_TO_ENCRYPT")))
}
# FIREBASE_CONFIG = {
#   'apiKey': "AIzaSyDW7I7Dapmfm3bLbPT816drfEtJfJwG1Ng",
#   'authDomain': "testforbotdb.firebaseapp.com",
#   'databaseURL': "https://testforbotdb-default-rtdb.europe-west1.firebasedatabase.app",
#   'projectId': "testforbotdb",
#   'storageBucket': "testforbotdb.appspot.com",
#   'messagingSenderId': "790834335753",
#   'appId': "1:790834335753:web:443b7f5d74d6b68bdfa8d8",
#   'measurementId': "G-PLSFZ9L610"
# }

BOT_TOKEN = os.getenv("BOT_TOKEN")
