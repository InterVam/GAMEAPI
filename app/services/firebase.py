# app/services/firebase.py
import firebase_admin
from firebase_admin import credentials, firestore, auth
from app.config import FIREBASE_CREDENTIALS_PATH

# Initialize Firebase
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_app = firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Collections
users_collection = db.collection('users')
games_collection = db.collection('games')
devices_collection = db.collection('devices')