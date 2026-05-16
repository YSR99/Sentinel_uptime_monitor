from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"] , deprecated = "auto")

def get_hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_pass: str , hash_pass:str):
    return pwd_context.verify(plain_pass , hash_pass)
