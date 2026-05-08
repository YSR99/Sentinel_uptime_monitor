from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker , declarative_base

Database_url = "postgresql+psycopg2://postgres:admin123@localhost:5432/sentinel_db" 

engine = create_engine(Database_url)

SessionLocal = sessionmaker(autoflush=False, autocommit = False , bind = engine  )

Base  = declarative_base()

try:
    connection = engine.connect()
    print ("Connected Successfully_")
    connection.close()

except Exception as e :
    print(e)

