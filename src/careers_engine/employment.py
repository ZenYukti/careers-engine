from __future__ import annotations

from careers_engine.models import EmploymentType

EMPLOYMENT_TYPE_ALIASES = {
    "intern": EmploymentType.INTERN,
    "internship": EmploymentType.INTERN,
    "new grad": EmploymentType.NEW_GRAD,
    "graduate": EmploymentType.NEW_GRAD,
    "full time": EmploymentType.FULL_TIME,
    "full-time": EmploymentType.FULL_TIME,
    "fulltime": EmploymentType.FULL_TIME,
    "part time": EmploymentType.PART_TIME,
    "part-time": EmploymentType.PART_TIME,
    "contract": EmploymentType.CONTRACT,
    "contractor": EmploymentType.CONTRACT,
    "fixed term": EmploymentType.CONTRACT,
    "apprentice": EmploymentType.APPRENTICESHIP,
    "apprenticeship": EmploymentType.APPRENTICESHIP,
}


INTERNSHIP_KEYWORDS = (
    "intern",
    "internship",
    "summer intern",
    "summer internship",
)

NEW_GRAD_KEYWORDS = (
    "new grad",
    "graduate",
    "campus",
    "university graduate",
    "university hire",
    "early career",
    "entry level",
)

APPRENTICESHIP_KEYWORDS = (
    "apprentice",
    "apprenticeship",
)

CONTRACT_KEYWORDS = (
    "contract",
    "contractor",
    "fixed term",
    "temporary",
)


def parse_employment_type(value: str) -> EmploymentType:
    """Normalize user input into a supported employment type."""

    key = value.strip().lower()

    try:
        return EMPLOYMENT_TYPE_ALIASES[key]

    except KeyError as exc:
        raise ValueError(
            "Unsupported employment type: "
            f"{value!r}. "
            "Supported values include: Internship, New Grad, "
            "Full Time, Part Time, Contract, Apprenticeship."
        ) from exc


def infer_employment_type(role: str) -> EmploymentType:
    """Infer the employment type from a job title."""

    role = role.lower()

    if any(keyword in role for keyword in INTERNSHIP_KEYWORDS):
        return EmploymentType.INTERN

    if any(keyword in role for keyword in NEW_GRAD_KEYWORDS):
        return EmploymentType.NEW_GRAD

    if any(keyword in role for keyword in APPRENTICESHIP_KEYWORDS):
        return EmploymentType.APPRENTICESHIP

    if any(keyword in role for keyword in CONTRACT_KEYWORDS):
        return EmploymentType.CONTRACT

    return EmploymentType.FULL_TIME
