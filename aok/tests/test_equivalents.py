import aok


def test_equivalent_list_tuple():
    """Should allow a tuple in place of a list."""
    observed = (1, 2, {"a": 12, "b": False}, "hello")
    expected = aok.OkayList([1, 2, {"a": 12, "b": False}, aok.unequals("goodbye")])
    expected.assert_all(observed)


def test_strict_equivalent_list_tuple():
    """Should fail when a tuple is compared to a strict list."""
    observed = (1, 2, {"a": 12, "b": False}, "hello")
    expected = aok.StrictList([1, 2, {"a": 12, "b": False}, aok.unequals("goodbye")])
    result = expected.compare(observed)
    assert not result.success
    assert result.operation == "list_type"
