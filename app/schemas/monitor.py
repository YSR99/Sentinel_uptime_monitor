from enum import Enum
from pydantic import BaseModel
from datetime import datetime 
class Monitor_Type(Enum):
    WEBAPP = "webapp"
    API = "api"

class MonitorCreate(BaseModel):
    url : str
    interval_sec : int 
    monitor_type : Monitor_Type

class MonitorResponse (BaseModel ):
    id : int
    url: str
    monitor_type: Monitor_Type
    interval_sec: int
    current_status : str
    created_at : datetime
    
    class Config :
        from_attributes = True



