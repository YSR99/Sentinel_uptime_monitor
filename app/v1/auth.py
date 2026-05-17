from fastapi import Depends , HTTPException  , APIRouter
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user_auth import UserCreate , UserResponse
from app.services.user_service  import create_user , authenticate_user 

from app.core.security import create_access_token ,   get_current_user 
from fastapi.security import OAuth2PasswordRequestForm







router   = APIRouter(prefix= "/auth" , tags=["Authentication"])

@router.post("/register" , response_model= UserResponse)
def register_user(user_data : UserCreate  , db : Session = Depends(get_db)):
    user = create_user(db, user_data)

    if not user:
       raise HTTPException(
        status_code=400,
         detail="Email already registered"
            )

    return user


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    access_token = create_access_token(
        {"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    

    
@router.get("/profile")
def profile(current_user  = Depends(get_current_user)):
     return current_user 
     