from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse
import bcrypt
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")

auth_router = APIRouter()

def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def create_token(user_id: int):
    return jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm="HS256")

@auth_router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return db_user

@auth_router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_token(db_user.id)
    return {"access_token": token}
