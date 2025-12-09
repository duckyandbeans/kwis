import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Global variable to ensure we don't initialize twice
_db_client = None

def get_db():
    global _db_client
    
    # If already connected, return the existing connection
    if _db_client:
        return _db_client

    if not firebase_admin._apps:
        # STRATEGY 1: TRY VERCEL ENVIRONMENT VARIABLE (Online)
        env_creds = os.environ.get('FIREBASE_CREDENTIALS')
        
        if env_creds:
            # We are online!
            cred_dict = json.loads(env_creds)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        
        # STRATEGY 2: TRY LOCAL FILE (Offline/Testing)
        else:
            # Look for key in local_admin folder relative to this file
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            key_path = os.path.join(base_path, 'local_admin', 'serviceAccountKey.json')
            
            if os.path.exists(key_path):
                cred = credentials.Certificate(key_path)
                firebase_admin.initialize_app(cred)
            else:
                print("⚠️ Warning: No Firebase Credentials found. Database calls will fail.")
                return None

    _db_client = firestore.client()
    return _db_client