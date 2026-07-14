import asyncio
import os
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import api_router
from app.models.event import Event

async def delete_expired_events():
    from google.cloud.firestore_v1.base_query import FieldFilter
    while True:
        try:
            from app.core.database import get_db
            db = get_db()
            now = datetime.utcnow()
            # Fetch and delete events whose date has passed
            events_ref = db.collection("events")
            docs = events_ref.where(filter=FieldFilter("date", "<", now)).get()
            deleted_count = 0
            for doc in docs:
                events_ref.document(doc.id).delete()
                deleted_count += 1
            if deleted_count > 0:
                print(f"INFO:     Deleted {deleted_count} expired events automatically.")
        except Exception as e:
            print(f"ERROR:    Failed to delete expired events: {e}")
        await asyncio.sleep(60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Firebase Admin SDK and Firestore client
    await init_db()
    
    # Start background cleanup task
    bg_task = asyncio.create_task(delete_expired_events())
    
    yield
    
    # Shutdown:
    bg_task.cancel()
    try:
        await bg_task
    except asyncio.CancelledError:
        pass
    print("INFO:     Firebase connection closed.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Serve uploads directory as static files
uploads_dir = os.path.join(os.getcwd(), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Set up CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include core routes
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "docs_url": "/docs"
    }
