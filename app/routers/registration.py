from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Registration
from app.schemas import RegistrationCreate, RegistrationResponse

router = APIRouter(
    prefix="/registration",
    tags=["Registration"],
)


@router.post(
    "/",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_registration(
    data: RegistrationCreate,
    db: AsyncSession = Depends(get_db),
):
    registration = Registration(
        full_name=data.full_name,
        age_group=data.age_group.value,
        is_student=data.is_student,
        student_of=data.student_of,
    )

    db.add(registration)
    await db.commit()
    await db.refresh(registration)

    return registration
