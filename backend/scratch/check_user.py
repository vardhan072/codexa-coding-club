import os
import json
from firebase_admin import credentials, firestore
import firebase_admin

# Set up credentials JSON
cred_path = "../firebase-credentials.json"
if os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
else:
    # Try parent directory
    cred_path = "firebase-credentials.json"
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        print("Error: firebase-credentials.json not found")
        exit(1)

db = firestore.client()
users_ref = db.collection("users")
docs = users_ref.where("email", "==", "codexa@sitam.co.in").get()

if docs:
    print(f"Success: User codexa@sitam.co.in exists in the database!")
    for doc in docs:
        print(doc.to_dict())
else:
    print("Warning: User codexa@sitam.co.in does NOT exist in the database! That is why no email is sent.")
