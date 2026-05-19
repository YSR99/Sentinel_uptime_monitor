from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker , declarative_base

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)



SessionLocal = sessionmaker(autoflush=False, autocommit = False , bind = engine  )

Base  = declarative_base()

try:
    connection = engine.connect()
    print ("Connected Successfully_")
    connection.close()

except Exception as e :
    print(e)


async def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()