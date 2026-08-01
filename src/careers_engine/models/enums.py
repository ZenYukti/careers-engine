from enum import Enum


class EmploymentType(str, Enum):
    INTERN = "Internship"
    NEW_GRAD = "New Grad"
    APPRENTICESHIP = "Apprenticeship"
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    UNKNOWN = "Unknown"


class Priority(str, Enum):
    HIGH = "High"
    NORMAL = "Normal"
    LOW = "Low"
