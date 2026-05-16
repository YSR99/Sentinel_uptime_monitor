from pydantic import BaseModel, Field
from pydantic import EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)



class UserResponse(BaseModel):
    id: int 
    email: EmailStr
    
