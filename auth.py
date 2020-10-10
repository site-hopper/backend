import json
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth





def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })

    r = requests.post(rest_api_url,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)

    return r.json()["idToken"]

def get_uid_from_token(id_token: str):
    result = auth.verify_id_token(id_token)
    return result.get("uid", None)
