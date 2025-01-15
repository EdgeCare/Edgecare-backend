from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.user import UserCreate, TokenResponse
from db.models.user import User
from db.database import get_db
from utils.auth_service import hash_password, authenticate_user, save_token, create_access_token
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/signup", response_model=TokenResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):

    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash the user's password
    hashed_password = hash_password(user_data.password)
    
    # Create a new user record
    new_user = User(email=user_data.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate an access token and save in the database
    token_data = {"sub": new_user.email}
    access_token, expires_at = create_access_token(data=token_data, expires_delta=timedelta(minutes=15))
    saved_token = save_token(db, new_user, access_token, expires_at)

    # Prepare the response
    response = {
        "token": saved_token.token,
        "userId": str(new_user.id),
        "expiresAt": saved_token.expires_at,
        "message": "successful"
    }
    
    return response

@router.post("/login", response_model=TokenResponse)
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    
    # Authenticate the user
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Generate a new token
    token_data = {"sub": user.email}
    access_token, expires_at = create_access_token(data=token_data, expires_delta=timedelta(minutes=15))
    saved_token = save_token(db, user, access_token, expires_at)
    
    response = {
        "token": saved_token.token,
        "userId": str(user.id),
        "expiresAt": saved_token.expires_at,
        "message": "successful"
    }
    
    return response
