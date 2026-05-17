from sqlalchemy import Column , Integer , String , ForeignKey, Enum as Sqlenum
from app.db.database import Base 
from datetime import datetime 
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.schemas.monitor import Monitor_Type
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func



class Monitor(Base):
    __tablename__ = "monitors" 
    id = Column( Integer  , primary_key = True , index= True )
    user_id=Column( Integer , ForeignKey("users.id")  , index= True )
    url = Column(String ,  nullable= False )
    monitor_type= Column(Sqlenum(Monitor_Type))
    interval_sec = Column(Integer  , default= 60)

    current_status = Column(String , default = "Unknown")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates= "monitor")