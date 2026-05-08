from enum import Enum

from pydantic import BaseModel, Field, model_validator


class AgeGroup(str, Enum):
    age_6_18 = "6-18"
    age_18_30 = "18-30"
    age_30_50 = "30-50"


class RegistrationCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    age_group: AgeGroup
    is_student: bool
    student_of: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def validate_student_of(self):
        if self.is_student and not self.student_of:
            raise ValueError("Если пользователь студент, нужно указать студент чего")

        if not self.is_student:
            self.student_of = None

        return self


class RegistrationResponse(BaseModel):
    id: int
    full_name: str
    age_group: AgeGroup
    is_student: bool
    student_of: str | None

    model_config = {
        "from_attributes": True
    }
