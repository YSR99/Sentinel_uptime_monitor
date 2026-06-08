from datetime import datetime, timezone
import logging
import time

import httpx

from app.models.monitor import Monitor
from app.models.checkresults import CheckResults
from app.models.incident import Incident
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


def create_monitor(db, monitor_data, user_id):
    monitor = Monitor(
        url=monitor_data.url,
        interval_sec=monitor_data.interval_sec,
        user_id=user_id,
        monitor_type=monitor_data.monitor_type,
    )

    db.add(monitor)
    db.commit()
    db.refresh(monitor)

    return monitor


def get_user_monitors(db, user_id: int):
    return (
        db.query(Monitor)
        .filter(Monitor.user_id == user_id)
        .all()
    )


def perform_monitor_check(url):
    try:
        start = time.time()

        response = httpx.get(url, timeout=10)

        end = time.time()
        response_time = (end - start) * 1000

        return {
            "status_code": response.status_code,
            "response_time_ms": round(response_time, 2),
            "is_up": response.status_code < 400,
            "error": None,
        }

    except httpx.TimeoutException:
        return {
            "status_code": None,
            "response_time_ms": None,
            "is_up": False,
            "error": "Request timed out",
        }

    except httpx.RequestError as e:
        return {
            "status_code": None,
            "response_time_ms": None,
            "is_up": False,
            "error": str(e),
        }


def run_monitor_check(db, monitor_id):
    try:
        monitor = (
            db.query(Monitor)
            .filter(Monitor.id == monitor_id)
            .first()
        )

        if not monitor:
            return

        logger.info(f"Checking monitor {monitor.id}")

        result = perform_monitor_check(monitor.url)

        previous_status = monitor.current_status
        new_status = "UP" if result["is_up"] else "DOWN"

        # Create incident when website goes down
        if previous_status == "UP" and new_status == "DOWN":
            incident = Incident(
                monitor_id=monitor.id,
                reason=result.get("error")
                or f"HTTP {result['status_code']}",
            )

            db.add(incident)
            logger.info(
    f"Sending email to {monitor.owner.email}"
)

            EmailService.send_email(
                recipient=monitor.owner.email,
                subject=f"🚨 Website Down: {monitor.url}",
                message=f"""
Website Down Alert

URL: {monitor.url}

Reason:
{result.get('error') or f'HTTP {result["status_code"]}'}

Time:
{datetime.now(timezone.utc)}
""",
            )

        # Resolve incident when website recovers
        if previous_status == "DOWN" and new_status == "UP":
            incident = (
                db.query(Incident)
                .filter(
                    Incident.monitor_id == monitor.id,
                    Incident.status == "OPEN",
                )
                .first()
            )

            if incident:
                incident.status = "RESOLVED"
                incident.resolved_at = datetime.now(timezone.utc)
                logger.info(
    f"Sending email to {monitor.owner.email}"
)

            EmailService.send_email(
                recipient=monitor.owner.email,
                subject=f"✅ Website Recovered: {monitor.url}",
                message=f"""
Website Recovery Alert

URL: {monitor.url}

The website is reachable again.

Time:
{datetime.now(timezone.utc)}
""",
            )

        monitor.current_status = new_status
        monitor.last_checked_at = datetime.now(timezone.utc)

        logger.info(
            f"Monitor {monitor.id}: {previous_status} -> {new_status}"
        )

        new_result = CheckResults(
            monitor_id=monitor.id,
            status_code=result["status_code"],
            response_time=result["response_time_ms"],
            is_up=result["is_up"],
            error=result.get("error"),
        )

        db.add(new_result)

        db.flush()
        print("FLUSH OK")

        db.commit()
        print("COMMIT OK")

        logger.info(
            f"Monitor {monitor.id} status {new_status}"
        )

    except Exception:
        logger.exception(
            f"Monitor check failed for {monitor_id}"
        )

        db.rollback()
        raise