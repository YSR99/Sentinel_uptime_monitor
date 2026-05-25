from app.db.database import Base
from sqlalchemy import Integer  , String  , Column , ForeignKey  , Boolean , Float
from sqlalchemy.orm import relationship


class CheckResults(Base):
    __tablename__  = "CheckResult"
    id =  Column(Integer , primary_key= True , index= True)
    monitor_id =  Column(Integer, ForeignKey("monitors.id"))

    status_code = Column(Integer, nullable= True )
    response_time = Column(Float, nullable= True)
    is_up = Column(Boolean,  nullable= False)
    error = Column(String )


    monitor = relationship("Monitor", back_populates="check_results")