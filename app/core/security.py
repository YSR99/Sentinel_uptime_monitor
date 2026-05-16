from jose import jwt
from datetime import timedelta , datetime
from app.core.config import SECRET_KEY , ALGORITHM , ACCESS_TOKEN_MINUTE
from fastapi.security  import OAuth2PasswordBearer 
from typing import Annotated 
from fastapi import Depends , HTTPException

from jose import JWTError

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"] , deprecated = "auto")

def get_hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_pass: str , hash_pass:str):
    return pwd_context.verify(plain_pass , hash_pass)


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_MINUTE)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode ,SECRET_KEY , algorithm  = ALGORITHM)
    return encoded_jwt


oauth2_scheme  = OAuth2PasswordBearer(tokenUrl ='/auth/login')

def get_current_user(token : Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY , algorithms = [ALGORITHM])
        username : str = payload.get("sub")
        if username is None :
            raise HTTPException(status_code=401)
        return {"username":username}
    except JWTError:
        raise HTTPException(status_code=401)
    
