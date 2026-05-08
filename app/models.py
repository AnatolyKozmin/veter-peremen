from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Registration(Base):
    __tablename__ = "registrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    full_name: Mapped[str] = mapped_column(String, nullable=False)
    age_group: Mapped[str] = mapped_column(String, nullable=False)

    is_student: Mapped[bool] = mapped_column(Boolean, nullable=False)
    student_of: Mapped[str | None] = mapped_column(String, nullable=True)
