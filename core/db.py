import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, firestore

# Global variable for caching
_db_client = None

def get_db():
    global _db_client
    
    if _db_client:
        return _db_client

    if not firebase_admin._apps:
        # 1. TRY VERCEL ENVIRONMENT VARIABLE
        env_creds = os.environ.get('FIREBASE_CREDENTIALS')
        
        cred = None
        
        if env_creds:
            try:
                # OPTION A: It's Base64 Encoded (The Bulletproof Way)
                # We try to decode it. If it's not base64, this might fail, 
                # catch the error and try Option B.
                decoded_json = base64.b64decode(env_creds).decode('utf-8')
                cred_dict = json.loads(decoded_json)
                cred = credentials.Certificate(cred_dict)
            except Exception:
                # OPTION B: It's just a regular JSON string
                try:
                    cred_dict = json.loads(env_creds)
                    cred = credentials.Certificate(cred_dict)
                except Exception as e:
                    print(f"❌ Critical Error: Could not parse FIREBASE_CREDENTIALS. {e}")

        # 2. TRY LOCAL FILE (Offline Testing)
        if not cred:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            key_path = os.path.join(base_path, 'local_admin', 'serviceAccountKey.json')
            
            if os.path.exists(key_path):
                print("Using Local Admin Key")
                cred = credentials.Certificate(key_path)
        
        # 3. INITIALIZE
        if cred:
            firebase_admin.initialize_app(cred)
        else:
            print("⚠️ ERROR: No credentials found! Database will fail.")
            return None

    _db_client = firestore.client()
    return _db_client