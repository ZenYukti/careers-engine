from __future__ import annotations

import re

from careers_engine.filters.base import JobFilter
from careers_engine.models import Job


class EligibilityFilter(JobFilter):
    """Keep technical and software roles relevant to applicants in India."""

    INDIA_PATTERN = re.compile(r"\bindia\b", re.IGNORECASE)

    # must match at least one tech/engineering/product keyword
    TECH_ROLE_KEYWORDS = re.compile(
        r"\b("
        r"software|sde|swe|engineer|developer|frontend|front-end|backend|back-end|"
        r"full[- ]?stack|fullstack|data\s+scientist|data\s+engineer|data\s+analyst|"
        r"machine\s+learning|ml\b|ai\s+engineer|applied\s+scientist|research\s+scientist|"
        r"research\s+intern|devops|sre|site\s+reliability|cloud|security\s+engineer|"
        r"cybersecurity|android|ios|mobile|qa\b|sdet|test\s+engineer|systems\s+engineer|"
        r"platform\s+engineer|firmware|embedded|silicon|hardware|asic|fpga|vlsi|"
        r"product\s+manager|apm\b|quant|quantitative|blockchain|web3"
        r")\b",
        re.IGNORECASE,
    )

    # Reject non-tech, medical, financial, legal, and senior/management roles
    EXCLUDED_ROLE_KEYWORDS = re.compile(
        r"\b("
        r"radiologist|physician|medical|nurse|clinical|dental|"
        r"investment\s+banking|investor\s+relations|private\s+equity|transaction\s+advisory|"
        r"account\s+executive|sales|accountant|tax|audit|legal|counsel|paralegal|"
        r"recruiter|recruiting|talent\s+acquisition|human\s+resources|\bhr\b|"
        r"marketing|copywriter|social\s+media|customer\s+success|customer\s+support|"
        r"annotation|annotator|ai\s+tutor|ai\s+trainer|research\s+contributor|domain\s+expert|"
        r"staff\b|principal\b|director\b|\bvp\b|vice\s+president|head\s+of|lead\b|manager\b|"
        r"senior\b|\bsr\.?\b|iii\b|iv\b"
        r")\b",
        re.IGNORECASE,
    )

    def match(self, job: Job) -> bool:
        # 1. Location check
        if not bool(self.INDIA_PATTERN.search(job.location)):
            return False

        # 2. Employment type check
        if job.employment_type and job.employment_type.lower() == "contract":
            return False

        title = job.role or ""

        # 3. Exclude non-tech / senior roles (not needed at this stage for ZenYukti)
        if self.EXCLUDED_ROLE_KEYWORDS.search(title):
            return False

        # 4. Must contain a tech keyword
        if not self.TECH_ROLE_KEYWORDS.search(title):
            return False

        return True
