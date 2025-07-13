from pydantic import BaseModel
from datetime import datetime

class loginmodel(BaseModel):
    username: str
    password: str

class Token(BaseModel):
     access_token : str
     token_type : str

class chatcreate(BaseModel):
     content : str     

class chatout(BaseModel):
     chat_id : int
     content : str         
     created_at : datetime

     class Config:
        orm_mode = True