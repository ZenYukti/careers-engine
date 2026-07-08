from enum import Enum


class EmploymentType(str, Enum):
    INTERN = "Internship"
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    UNKNOWN = "Unknown"


class Priority(str, Enum):
    HIGH = "High"
    NORMAL = "Normal"
    LOW = "Low"
