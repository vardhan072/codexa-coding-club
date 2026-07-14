import os
import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import settings

# Global Firestore client reference
db = None

async def init_db() -> None:
    global db
    
    # Check if we have already initialized the default app
    try:
        firebase_admin.get_app()
    except ValueError:
        # App is not initialized yet
        cred_path = settings.FIREBASE_CREDENTIALS_PATH
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            # Fall back to environment/default credentials
            firebase_admin.initialize_app()
            
    db = firestore.client()
    print("INFO:    Firebase Firestore client initialized successfully!")

def get_db():
    global db
    if db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return db
