from fastapi import FastAPI
from app.db.database import Base , engine 
from app.models.user import User 

app = FastAPI()
print(Base.metadata.tables.keys())

Base.metadata.create_all(bind = engine)


