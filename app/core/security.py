from jose import jwt
from datetime import timedelta , datetime
from app.core.config import settings

from fastapi.security  import OAuth2PasswordBearer 
from typing import Annotated 
from fastapi import Depends , HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User

from jose import JWTError

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"] , deprecated = "auto")

def get_hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_pass: str , hash_pass:str):
    return pwd_context.verify(plain_pass , hash_pass)


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode ,settings.SECRET_KEY
 , algorithm  = settings.ALGORITHM)
    return encoded_jwt


oauth2_scheme  = OAuth2PasswordBearer(tokenUrl ="/v1/auth/login")

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        raise credentials_exception

    return user