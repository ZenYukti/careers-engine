from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256
from typing import Self

from pydantic import BaseModel, ConfigDict, Field

from careers_engine.models.enums import EmploymentType, Priority


class Job(BaseModel):
    model_config = ConfigDict(frozen=True)

    company: str
    role: str
    location: str

    apply_url: str

    employment_type: EmploymentType = EmploymentType.INTERN

    eligibility: str | None = None
    stipend: str | None = None
    deadline: str | None = None

    priority: Priority = Priority.NORMAL

    discovered_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @property
    def identifier(self) -> str:
        key = f"{self.company}|{self.role}|{self.location}|{self.apply_url}"
        return sha256(key.encode()).hexdigest()

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**data)

    def to_dict(self) -> dict:
        return self.model_dump()
