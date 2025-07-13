from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext

secret_key = "my-secret-key"
algo = "HS256"
access_token_expire_minutes = 30

def create_access_token(data : dict , expire_Delta : timedelta = None):
    new_data = data.copy()
    expiry_time= datetime.utcnow() + (expire_Delta or timedelta(minutes=access_token_expire_minutes))
    new_data.update({"exp" : expiry_time})
    return jwt.encode(new_data,secret_key,algorithm=algo)

def decode_token(token:str):
    try:
       abc =  jwt.decode(token,secret_key,algorithms=[algo])
       return abc
    except JWTError:
        return None
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password : str):
    return pwd_context.hash(plain_password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)    






