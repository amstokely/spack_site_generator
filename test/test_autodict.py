from spack_site_generator.utils.autodict import AutoDict


def test_autodict_getitem_creates_nested():
    """Accessing a missing key should create and return a nested AutoDict."""
    d = AutoDict()
    assert isinstance(d["config"], AutoDict)
    d["config"]["settings"]["theme"] = "dark"
    assert d["config"]["settings"]["theme"] == "dark"


def test_autodict_setitem_converts_dict():
    """Assigning a plain dict should recursively convert it into AutoDict."""
    d = AutoDict()
    d["nested"] = {"a": 1, "b": {"c": 2}}
    assert isinstance(d["nested"], AutoDict)
    assert isinstance(d["nested"]["b"], AutoDict)
    assert d["nested"]["a"] == 1
    assert d["nested"]["b"]["c"] == 2


def test_autodict_setitem_with_autodict():
    """Assigning an existing AutoDict should store it unchanged."""
    d = AutoDict()
    sub = AutoDict()
    sub["x"] = 42
    d["key"] = sub
    assert d["key"] is sub
    assert d["key"]["x"] == 42


def test_to_dict_converts_all_levels():
    """Converting to dict should unwrap all nested AutoDicts to plain dicts."""
    d = AutoDict()
    d["a"]["b"] = 1
    d["c"] = {"d": {"e": 2}}
    result = d.to_dict()
    assert result == {"a": {"b": 1}, "c": {"d": {"e": 2}}}
    assert not isinstance(result["c"], AutoDict)


def test_empty_method():
    """empty() should return True for an empty dict and False otherwise."""
    d = AutoDict()
    assert d.empty() is True
    d["key"] = "value"
    assert d.empty() is False


def test_overwrite_existing_key():
    """Overwriting an existing key should replace the old value."""
    d = AutoDict()
    d["x"] = 1
    d["x"] = 99
    assert d["x"] == 99


def test_repr_and_str_consistency():
    """String representation should show nested keys and values."""
    d = AutoDict()
    d["foo"]["bar"] = "baz"
    s = str(d)
    assert "foo" in s and "bar" in s and "baz" in s


def test_nested_chain_assignment_and_lookup():
    """Deeply nested chain assignment should work and convert properly."""
    d = AutoDict()
    d["lvl1"]["lvl2"]["lvl3"] = "deep"
    assert d["lvl1"]["lvl2"]["lvl3"] == "deep"
    assert d.to_dict() == {"lvl1": {"lvl2": {"lvl3": "deep"}}}
