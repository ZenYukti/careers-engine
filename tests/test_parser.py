from careers_engine.parsers import MarkdownTableParser


def test_parser_exists():
    parser = MarkdownTableParser()

    assert callable(parser.parse)
