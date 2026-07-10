from careers_engine.sources import UpstreamSource


def test_upstream_source_name():
    source = UpstreamSource()

    assert source.name == "upstream"


def test_upstream_source_is_source():
    source = UpstreamSource()

    assert hasattr(source, "fetcher")
    assert callable(source.collect)
