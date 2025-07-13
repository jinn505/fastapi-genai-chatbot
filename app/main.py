from fastapi import FastAPI, Depends, HTTPException, status,Response,UploadFile,File
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db_jwt.crud import * 
from app.db_jwt.database import * 
from app.db_jwt.auth import * 
from app.db_jwt.schemas import * 
from typing import Annotated
from app.chains.rag_chain import *
from langchain_core.messages import HumanMessage, AIMessage
import os
import shutil
from uuid import uuid4
from fastapi import UploadFile, File
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.retriever.qdrant_wrapper import get_qdrant
from app.retriever.embedder import get_embedder


Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
app = FastAPI()

UPLOAD_DIR = "app/docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

db_dependency = Annotated[Session , Depends(get_db)]
@app.post("/register")
def create(user : loginmodel, db:db_dependency):
    if get_user(user.username,db):
         raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user.password)
    new_user = create_user(user.username, hashed_password,db)
    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # print(fake_db)
    
    return {"message" : "user added successfully"}

@app.post("/login",response_model = Token)
def login( db: db_dependency,response: Response,form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    db_user = get_user(username,db)
    # print(db_user)
    if not db_user:
        raise HTTPException(status_code=401, detail="credentials not found")
    elif not verify_password(password , db_user.hashed_password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    
    token = create_access_token({"sub" : username})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(db:db_dependency,access_token: str = Depends(oauth2_scheme)):
    payload = decode_token(access_token)
    print(payload)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = get_user(username, db)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user

@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you're authorized!"}


rag_chain = get_rag_chain()
@app.post("/chat",response_model=chatout)
def chat_input(chat : chatcreate, db:db_dependency, current_user = Depends(get_current_user)):
    user_chats = (
        db.query(Chat)
        .filter(Chat.user_id == current_user.user_id)
        .order_by(Chat.chat_id)
        .all()
    )
    chat_history = []
    for chats in user_chats:
        try:
            question, answer = chats.chat_content.split("\nA: ")
            question = question.replace("Q: ", "")
            chat_history.append(HumanMessage(content=question))
            chat_history.append(AIMessage(content=answer))
        except Exception:
            continue  # Skip malformed chat entries

    response = rag_chain.invoke({
        "question": chat.content,
        "chat_history": chat_history
    })    

    answer = response["answer"]

    # Step 4: Save new chat to DB
    db_chat = Chat(
        chat_content=f"Q: {chat.content}\nA: {answer}",
        user_id=current_user.user_id,
        created_at = datetime.utcnow()
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    return chatout(
    chat_id=db_chat.chat_id,
    content=db_chat.chat_content,
    created_at=db_chat.created_at
)

@app.post("/upload_pdf")
def upload_pdf(db: db_dependency,file: UploadFile = File(...), current_user=Depends(get_current_user)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # 1. Save PDF to disk
    filename = f"{current_user.user_id}_{uuid4().hex}.pdf"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Load and split PDF
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(pages)

    # 3. Store in Qdrant with user_id as metadata
    qdrant = get_qdrant()
    for doc in docs:
        doc.metadata["user_id"] = current_user.user_id

    qdrant.add_documents(documents=docs)

    return {"message": f"Uploaded and processed {file.filename} successfully."}

