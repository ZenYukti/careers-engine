import pytest

from careers_engine.employment import (
    infer_employment_type,
    parse_employment_type,
)
from careers_engine.models import EmploymentType


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Internship", EmploymentType.INTERN),
        ("internship", EmploymentType.INTERN),
        ("New Grad", EmploymentType.NEW_GRAD),
        ("graduate", EmploymentType.NEW_GRAD),
        ("Full Time", EmploymentType.FULL_TIME),
        ("full-time", EmploymentType.FULL_TIME),
        ("fulltime", EmploymentType.FULL_TIME),
        ("Part Time", EmploymentType.PART_TIME),
        ("part-time", EmploymentType.PART_TIME),
        ("Contract", EmploymentType.CONTRACT),
        ("contractor", EmploymentType.CONTRACT),
        ("Apprenticeship", EmploymentType.APPRENTICESHIP),
        ("apprentice", EmploymentType.APPRENTICESHIP),
    ],
)
def test_parse_employment_type(value: str, expected: EmploymentType) -> None:
    assert parse_employment_type(value) == expected


def test_parse_employment_type_invalid() -> None:
    with pytest.raises(
        ValueError,
        match="Unsupported employment type",
    ):
        parse_employment_type("Volunteer")


@pytest.mark.parametrize(
    ("role", "expected"),
    [
        (
            "Software Engineer Intern",
            EmploymentType.INTERN,
        ),
        (
            "Backend Engineering Internship",
            EmploymentType.INTERN,
        ),
        (
            "Software Engineer - New Grad",
            EmploymentType.NEW_GRAD,
        ),
        (
            "Graduate Software Engineer",
            EmploymentType.NEW_GRAD,
        ),
        (
            "Software Development Apprenticeship",
            EmploymentType.APPRENTICESHIP,
        ),
        (
            "Apprentice Software Engineer",
            EmploymentType.APPRENTICESHIP,
        ),
        (
            "Backend Engineer (Contract)",
            EmploymentType.CONTRACT,
        ),
        (
            "Software Engineer Contractor",
            EmploymentType.CONTRACT,
        ),
        (
            "Software Engineer",
            EmploymentType.FULL_TIME,
        ),
        (
            "Senior Software Engineer",
            EmploymentType.FULL_TIME,
        ),
        (
            "Staff Software Engineer",
            EmploymentType.FULL_TIME,
        ),
    ],
)
def test_infer_employment_type(
    role: str,
    expected: EmploymentType,
) -> None:
    assert infer_employment_type(role) == expected
