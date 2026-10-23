"""
scanet — Backend Entry Point
FastAPI application factory and server startup.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pathlib import Path
import uvicorn

from config import settings
from database.connection import init_db
from api.routes import targets, jobs, results, system, pipelines, advisor, topology, os_detect, web_audit


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    # Startup
    await init_db()
    yield
    # Shutdown — cleanup if needed


app = FastAPI(
    title="scanet API",
    description="Lightweight, Modular Cybersecurity Reconnaissance Platform",
    version="0.2.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── API Routes ────────────────────────────────────────────────────────────────
app.include_router(targets.router,   prefix="/api/v1/targets",   tags=["Targets"])
app.include_router(jobs.router,      prefix="/api/v1/jobs",      tags=["Jobs"])
app.include_router(results.router,   prefix="/api/v1/results",   tags=["Results"])
app.include_router(system.router,    prefix="/api/v1/system",    tags=["System"])
app.include_router(pipelines.router, prefix="/api/v1/pipelines", tags=["Pipelines"])
app.include_router(advisor.router,   prefix="/api/v1/advisor",   tags=["AI Advisor"])
app.include_router(topology.router,  prefix="/api/v1/topology",  tags=["Topology Graph"])
app.include_router(os_detect.router, prefix="/api/v1/os-detect", tags=["OS Detection"])
app.include_router(web_audit.router, prefix="/api/v1/web-audit", tags=["Web Security Auditor"])



# ── Serve Frontend Static Files ───────────────────────────────────────────────
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
ASSETS_DIR = FRONTEND_DIR / "assets"
EMBLEM_PATH = ASSETS_DIR / "images" / "scanet_emblem.svg"

app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

@app.get("/", include_in_schema=False)
async def serve_frontend():
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/favicon.ico", include_in_schema=False)
@app.get("/favicon.svg", include_in_schema=False)
async def serve_favicon():
    return FileResponse(str(EMBLEM_PATH))



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
