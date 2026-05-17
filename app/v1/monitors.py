from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session 
from typing import List
from app.db.database import get_db
from app.schemas.monitor import MonitorCreate  , MonitorResponse 
from app.services.monitor_service import get_user_monitors
from app.services.monitor_service import create_monitor 
from app.models.user import User
from app.core.security import get_current_user


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
                       



