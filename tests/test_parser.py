from pathlib import Path

from careers_engine.parsers import MarkdownTableParser

FIXTURE = Path(__file__).parent / "fixtures" / "intern_intl.md"


def test_markdown_parser():
    parser = MarkdownTableParser()

    rows = parser.parse(FIXTURE.read_text())

    assert rows

    first = rows[0]

    assert "company" in first
    assert "role" in first
    assert "location" in first
    assert "posting" in first
    assert "category" in first
