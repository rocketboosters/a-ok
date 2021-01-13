import typing

from pytest import mark

import aok

NOT_NULL_SCENARIOS = ("a", 1, 0, True)


@mark.parametrize("value", NOT_NULL_SCENARIOS)
def test_not_null(value: typing.Any):
    """Should pass if the value is not null."""
    aok.Okay({"a": aok.not_null()}).assert_all({"a": value})
