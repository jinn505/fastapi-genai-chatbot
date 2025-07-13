from sqlalchemy.orm import Session
from app.db_jwt.database import *
from app.db_jwt.schemas import *

# authentication crud

def get_user(username : str , db:Session):
   return db.query(User).filter(User.username == username).first()

def create_user(username : str , hashed_password : str , db:Session):
   db_user = User(username=username, hashed_password=hashed_password)
   existing_user = db.query(User).filter(User.username == username).first()
   if existing_user:
      return {"error": "User already exists"}
   
   db.add(db_user)
   db.commit()
   db.refresh(db_user)
   return db_user

def add_chat(user_id : int, content : str, db:Session):
   chat = Chat(user_id= user_id, chat_content = content)
   db.add(chat)
   db.commit()
   db.refresh(chat)
   return {"message" : "chat added successfully"}

def get_chats_by_user(user_id : int, db:Session):
   return db.query(Chat).filter(Chat.user_id == user_id).all()

