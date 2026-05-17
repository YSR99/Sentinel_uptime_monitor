from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_auth import UserCreate
from app.core.security import get_hash_password
from app.core.security import verify_password 

def create_user( db: Session , user_data: UserCreate  ):
    existing_user= db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        return None 
    
    else:
        hash_password = get_hash_password(user_data.password)

        new_user   = User(email = user_data.email, password_hash = hash_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user 
    

def authenticate_user( db: Session , email: str , password : str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None     
    
    if not verify_password(password , user.password_hash):
            return None
        
    return user  
        
        







