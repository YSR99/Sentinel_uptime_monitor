from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session 
from typing import List
from app.db.database import get_db
from app.schemas.monitor import MonitorCreate  , MonitorResponse 
from app.services.monitor_service import get_user_monitors
from app.services.monitor_service import create_monitor 
from app.models.user import User
from app.core.security import get_current_user
from app.services.monitor_service import run_monitor_check
from app.models.monitor import Monitor
from fastapi import HTTPException


router = APIRouter (prefix = "/monitors", tags = ["Monitors"])
@router.post("/", response_model=MonitorResponse)
def create_new_monitor(
    monitor_data: MonitorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_monitor(
        db=db,
        monitor_data=monitor_data,
        user_id=current_user.id
    )


@router.get("/" , response_model = List[MonitorResponse])
def fetch_user(db : Session = Depends(get_db),current_user : User = Depends(get_current_user ) ):
    return get_user_monitors(
        db=db,
        user_id=current_user.id)


@router.get("/{id}/check")
def monitor_check(id: int , db: Session = Depends(get_db), current_user : User = Depends(get_current_user)):
 monitor = db.query(Monitor).filter(
    Monitor.id == id,
    Monitor.user_id == current_user.id
).first()

 if not monitor:
    raise HTTPException(status_code= 404 , detail= "Monitor not found")
 
 run_monitor_check(db , monitor)
 return {"message": "Monitor checked successfully"}



