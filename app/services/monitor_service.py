from app.models.monitor import Monitor
import httpx
import time 
from app.models.checkresults import CheckResults


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


def perform_monitor_check(url):
    try:
        start = time.time()

        response = httpx.get(url, timeout=10)

        end = time.time()

        response_time = (end - start) * 1000
 
        return {
            "status_code": response.status_code,
            "response_time_ms": round(response_time, 2),
            "is_up": response.status_code < 400
        }

    except httpx.TimeoutException:
        return {
            "status_code": None,
            "response_time_ms": None,
            "is_up": False,
            "error": "Request timed out"
        }

    except httpx.RequestError as e:
        return {
            "status_code": None,
            "response_time_ms": None,
            "is_up": False,
            "error": str(e)
        }


def run_monitor_check(db, monitor):

    result = perform_monitor_check(monitor.url)

    monitor.current_status = "UP" if result["is_up"] else "DOWN"

    new_result = CheckResults(
        monitor_id=monitor.id,
        status_code=result["status_code"],
        response_time=result["response_time_ms"],
        is_up=result["is_up"],
        error=result.get("error")
    )

    db.add(new_result)

    db.commit()