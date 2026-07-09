from careers_engine.sources import PrivateSource


def test_private_source_name():
    source = PrivateSource()

    assert source.name == "private"


def test_private_source_is_source():
    source = PrivateSource()

    assert hasattr(source, "fetcher")
    assert callable(source.collect)
