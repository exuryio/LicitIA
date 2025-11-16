"""Background job scheduler setup."""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

scheduler = BackgroundScheduler()


def start_scheduler():
    """Start the background scheduler."""
    if not scheduler.running:
        scheduler.start()
        logger.info("Background scheduler started")


def shutdown_scheduler():
    """Shutdown the background scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Background scheduler stopped")

