from app.db.database import Base
from sqlalchemy import Column, Integer , ForeignKey , DateTime , String , func
from sqlalchemy.orm import relationship 



class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True)

    monitor_id = Column(
        Integer,
        ForeignKey("monitors.id")
    )

    started_at = Column(
        DateTime(timezone=True),
        default=func.now()
    )

    resolved_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    status = Column(
        String,
        default="OPEN"
    )

    reason = Column(String)



    monitor = relationship(
        "Monitor",
        back_populates="incidents"
    )