import aok


def test_call():
    """Should assert the expected dictionary meets the conditions."""
    result: dict = {
        "mother": {"age": 54, "full_name": "Hannah Doe"},
        "father": {"age": 55, "full_name": "Bill Doe"},
        "younger_brother": {"age": 8, "full_name": "Eric Doe"},
    }

    ok = aok.Okay(
        {
            "mother": {
                "age": aok.greater_or_equal(50),
                "full_name": aok.like("* Doe"),
            },
            "father": {
                "age": aok.greater_or_equal(50),
                "full_name": aok.like("* Doe"),
            },
            "younger_brother": {
                "age": aok.less(10),
                "full_name": aok.like("* Doe"),
            },
        }
    )

    # Dictionary "result" must be an exact match with the ok expected values.
    ok.assert_all(result)

    # Dictionary "result" is asserted against ok expected values as a subset, such
    # that other keys/values may exist within the "result" structure.
    ok.assert_subset(result)
