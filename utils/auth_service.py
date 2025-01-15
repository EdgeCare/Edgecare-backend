from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from db.models.user import User, Token
import uuid

# Secret key and hashing algorithm
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 min

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Authenticate user
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.password_hash):
        return user
    return None

# Create a new token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token, expire

# Save token in the database
def save_token(db: Session, user: User, token_str: str, expires_at: datetime):
    # Remove any existing expired token for the user
    db.query(Token).filter(Token.user_id == user.id, Token.expires_at < datetime.utcnow()).delete()

    # Add the new token
    token = Token(user_id=user.id, token=token_str, expires_at=expires_at)
    db.add(token)
    db.commit()
    db.refresh(token)

    # Keep only the two most recent tokens for the user
    user_tokens = db.query(Token).filter(Token.user_id == user.id).order_by(Token.expires_at.desc()).all()
    if len(user_tokens) > 2:
        tokens_to_delete = user_tokens[2:]
        for old_token in tokens_to_delete:
            db.delete(old_token)
        db.commit()

    return token
