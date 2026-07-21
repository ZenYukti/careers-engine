from __future__ import annotations

from careers_engine.company.metadata import CompanyMetadata

DEFAULT_BRAND = CompanyMetadata(
    color=0x5865F2,
)

COMPANY_BRANDS = {
    "Google": CompanyMetadata(
        color=0x4285F4,
    ),
    "Microsoft": CompanyMetadata(
        color=0x00A4EF,
    ),
    "Amazon": CompanyMetadata(
        color=0xFF9900,
    ),
    "Meta": CompanyMetadata(
        color=0x1877F2,
    ),
    "NVIDIA": CompanyMetadata(
        color=0x76B900,
    ),
}
