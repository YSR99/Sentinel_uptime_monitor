from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_auth import UserCreate
from app.schemas.user_auth import UserResponse
from app.core.security import get_hash_password
from fastapi import HTTPException

def create_user(db : Session , user_data: UserCreate):
    existing_user= db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code= 200 , detail = "Email already registered")
    
    else:
        hash_password = get_hash_password(user_data.password)

        new_user   = User(email = user_data.email, password_hash = hash_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user 
    


