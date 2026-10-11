import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.conversations import router as conversations_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Samantha-inspired personal voice AI assistant"
)

# Include API Routers
app.include_router(conversations_router)


@app.get("/health/live")
async def health_live():
    return {"status": "ok"}


@app.get("/health/ready")
async def health_ready():
    return {
        "status": "ready",
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "elevenlabs_configured": bool(settings.ELEVENLABS_API_KEY),
    }


# Static and Web UI files
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Samantha Assistant API is running. Access /docs for Swagger UI."}
