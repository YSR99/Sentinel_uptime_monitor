from fastapi import FastAPI
from app.db.database import Base , engine 
from app.models.user import User 

from app.v1.auth import router as auth_router 

app = FastAPI()
print(Base.metadata.tables.keys())

Base.metadata.create_all(bind = engine)
app.include_router(auth_router, prefix= "/v1")


