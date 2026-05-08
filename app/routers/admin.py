from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin_auth import verify_admin
from app.database import get_db
from app.models import Registration
from app.schemas import RegistrationResponse

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

ADMIN_HTML = Path(__file__).resolve().parents[2] / "frontend" / "admin.html"


@router.get("", include_in_schema=False)
async def admin_page(_: str = Depends(verify_admin)):
    return FileResponse(ADMIN_HTML)


@router.get("/registrations", response_model=list[RegistrationResponse])
async def list_registrations(
    _: str = Depends(verify_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Registration).order_by(Registration.id.desc()))
    return result.scalars().all()


@router.get("/stats")
async def stats(
    _: str = Depends(verify_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Registration))
    rows = result.scalars().all()

    by_age: dict[str, int] = {}
    students = 0
    for r in rows:
        by_age[r.age_group] = by_age.get(r.age_group, 0) + 1
        if r.is_student:
            students += 1

    return {
        "total": len(rows),
        "students": students,
        "non_students": len(rows) - students,
        "by_age_group": by_age,
    }
