from fastapi import FastAPI, Request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
import json
import requests
import auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()




@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    bearer_token_str = request.headers.get("authorization",None)
    print(bearer_token_str)
    if bearer_token_str is None:
        return {"no token"}
    bearer_token = bearer_token_str.split()[1]
    uid = auth.get_uid_from_token(bearer_token)
    print("before")
    #return uid
    print(uid)
    response = await call_next(request)
    print("after")

    return response

@app.get("/")
async def root():


    #user = auth.get_user_by_email("akshayrgund@gmail.com")
    id_token = auth.sign_in_with_email_and_password("akshayrgund@gmail.com", "Password123", True)
    auth.verify_id_token(id_token)
    return id_token
    """ref = db.reference('/')
    ref.set({
        'boxes':
            {
                'box001': {
                    'color': 'red',
                    'width': 1,
                    'height': 3,
                    'length': 2
                },
                'box002': {
                    'color': 'green',
                    'width': 1,
                    'height': 2,
                    'length': 3
                },
                'box003': {
                    'color': 'yellow',
                    'width': 3,
                    'height': 2,
                    'length': 1
                }
            }
    })"""
    #return 'Successfully fetched user data: {0}'.format(user.uid)

