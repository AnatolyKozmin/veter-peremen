from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(
    prefix="/healthcheck",
    tags=["Healthcheck"],
)


@router.get("/")
async def healthcheck(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
        }
    except Exception:
        return {
            "status": "error",
            "database": "disconnected",
        }
