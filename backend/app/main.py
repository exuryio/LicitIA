"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.scheduler import start_scheduler, shutdown_scheduler
from app.core.logging import setup_logging
from app.api.v1 import health, tenders, subscriptions, experiences
from app.services.tender_ingestion import fetch_and_store_new_tenders
from app.config import settings

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="LicitIA API",
    description="API for road supervision tender alerts",
    version="1.0.0",
)

# CORS middleware (allow frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(tenders.router, prefix="/api/v1", tags=["tenders"])
app.include_router(subscriptions.router, prefix="/api/v1", tags=["subscriptions"])
app.include_router(experiences.router, prefix="/api/v1", tags=["experiences"])


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    start_scheduler()
    
    # Schedule the tender fetching job
    from apscheduler.triggers.interval import IntervalTrigger
    from app.core.scheduler import scheduler
    
    scheduler.add_job(
        fetch_and_store_new_tenders,
        trigger=IntervalTrigger(hours=settings.FETCH_INTERVAL_HOURS),
        id="fetch_tenders",
        name="Fetch and store new tenders from SECOP",
        replace_existing=True,
    )


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    shutdown_scheduler()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

