from fastapi import Depends , HTTPException  , APIRouter
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user_auth import UserCreate , UserResponse
from app.services.user_service  import create_user 

router   = APIRouter(prefix= "/auth" , tags=["Authentication"])

@router.post("/register" , response_model= UserResponse)
def register_user(user_data : UserCreate  , db : Session = Depends(get_db)):
    return create_user(db , user_data)