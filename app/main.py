from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers.admin import router as admin_router
from app.routers.healthcheck import router as healthcheck_router
from app.routers.registration import router as registration_router

FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    title="Veter Peremen Backend",
    description="Backend for Telegram Mini App",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthcheck_router)
app.include_router(registration_router)
app.include_router(admin_router)


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
