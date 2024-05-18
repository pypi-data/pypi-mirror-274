import pytest
from meta_json import MetaJson


def test_meta_json_empty():
    """Read the TESTING.md document for more information.
    """
    meta = MetaJson(response={})
    assert meta.types() == {}
    assert meta.attributes() == [[], []]
    assert meta.layers() == {}
