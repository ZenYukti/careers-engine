from careers_engine.company import COMPANY_BRANDS, DEFAULT_BRAND


def test_google_brand_exists() -> None:
    assert "Google" in COMPANY_BRANDS


def test_default_brand_has_color() -> None:
    assert DEFAULT_BRAND.color == 0x5865F2
