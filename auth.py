from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas, utils, models
from database import db_run

SECRET_KEY = "1d4dcef57b40717b225927177a3862f3539b62ec998a87b956e3f06107726b09"
security = HTTPBearer()
router = APIRouter(tags=["Authentication"])

def create_token(user_id: int):
    expire = datetime.now() + timedelta(minutes=30)
    return jwt.encode({"user_id": user_id, "exp": expire}, SECRET_KEY, algorithm="HS256")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(db_run)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(401, "Invalid token")
        return user
    except JWTError:
        raise HTTPException(401, "Invalid token")

@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(user_data: schemas.UserCreate, db: Session = Depends(db_run)):
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(400, "Email already registered")
    
    new_user = models.User(email=user_data.email, password=utils.hash(user_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(user_data: schemas.UserCreate, db: Session = Depends(db_run)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user or not utils.verify(user_data.password, user.password):
        raise HTTPException(403, "Invalid credentials")
    
    access_token = create_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}