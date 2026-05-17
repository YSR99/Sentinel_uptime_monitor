from app.models.monitor import Monitor


def create_monitor(db , monitor_data  , user_id):
    monitor = Monitor(
        url = monitor_data.url,
        interval_sec  = monitor_data.interval_sec,
        user_id = user_id,
        monitor_type = monitor_data.monitor_type)

    db.add(monitor)
    db.commit()
    db.refresh(monitor)
    return monitor


def get_user_monitors(
    db , 
    user_id: int
):

    return db.query(Monitor).filter(
        Monitor.user_id == user_id
    ).all()