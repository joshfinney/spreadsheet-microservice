import os

class Config:
    DATABASE = 'cells.db'
    FIREBASE_DATABASE_URL='https://spreadsheet-microservice-default-rtdb.europe-west1.firebasedatabase.app'
    FIREBASE_WEB_API_KEY='YourFirebaseWebAPIKey'

class FirebaseConfig:
    FIREBASE_URL = f"https://{os.environ.get('FBASE')}.europe-west1.firebasedatabase.app"