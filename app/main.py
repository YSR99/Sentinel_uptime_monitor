from fastapi import FastAPI
from app.db.database import Base , engine 

from app.v1.monitors import router as monitor_router
from app.v1.health import router as health_router 

from app.v1.auth import router as auth_router 


app = FastAPI()
print(Base.metadata.tables.keys())

Base.metadata.create_all(bind = engine)
app.include_router(auth_router, prefix= "/v1")
app.include_router(monitor_router  , prefix= "/v1")
app.include_router(health_router , prefix= "/v1")



