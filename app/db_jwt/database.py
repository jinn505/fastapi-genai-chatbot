from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String,ForeignKey,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapped_column,Mapped, relationship
from datetime import datetime

db_urll = "sqlite:///./chats_data.db"
engine = create_engine(db_urll, connect_args={"check_same_thread": False})

sessionlocal = sessionmaker(autocommit = False,autoflush=False, bind = engine)

Base = declarative_base()

class Chat(Base):
    __tablename__ = "user_chats"
    chat_id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chat_content : Mapped[str] = mapped_column(String,index = True)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("user_data.user_id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="chats")

class User(Base):
    __tablename__ = "user_data"
    user_id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username : Mapped[str] = mapped_column(String,nullable = False,index = True,unique=True)
    hashed_password : Mapped[str] = mapped_column(String, nullable=False)
    chats = relationship("Chat", back_populates="owner")