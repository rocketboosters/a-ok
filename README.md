# A-OK

[![PyPI version](https://badge.fury.io/py/okay.svg)](https://pypi.org/project/okay/)
[![build status](https://gitlab.com/rocket-boosters/okay/badges/main/pipeline.svg)](https://gitlab.com/rocket-boosters/okay/commits/main)
[![coverage report](https://gitlab.com/rocket-boosters/okay/badges/main/coverage.svg)](https://gitlab.com/rocket-boosters/okay/commits/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Code style: flake8](https://img.shields.io/badge/code%20style-flake8-white)](https://gitlab.com/pycqa/flake8)
[![Code style: mypy](https://img.shields.io/badge/code%20style-mypy-white)](http://mypy-lang.org/)
[![PyPI - License](https://img.shields.io/pypi/l/okay)](https://pypi.org/project/okay/)

*aok* is a library for simplifying the assertions of complex dictionary returns,
which can be used within Python code or loaded via YAML files.

```python
import aok

import my_application


def test_call():
    """Should return the expected dictionary from my application call."""
    result: dict = my_application.get_family("Jane Doe")
    ok = aok.Okay({
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
        }
    })
    
    # Dictionary "result" must be an exact match with the ok expected values.
    ok.assert_all(result)

    # Dictionary "result" is asserted against ok expected values as a subset, such
    # that other keys/values may exist within the "result" structure.
    ok.assert_subset(result)
```

The same thing can be archived from a YAML file:

```yaml
ok: !aok
  mother:
    age: !aok.greater_or_equal 50
    full_name: !aok.like '* Doe'
  father:
    age: !aok.greater_or_equal 50
    full_name: !aok.like '* Doe'
  younger_brother:
    age: !aok.less 10
    full_name: !aok.like '* Doe'
```

and this can be loaded into a test:

```python
import aok
import yaml
import pathlib

import my_application


def test_call():
    """Should return the expected dictionary from my application call."""
    result: dict = my_application.get_family("Jane Doe")
    data: dict = yaml.full_load(pathlib.Path("expectations.yaml").read_text())
    ok: aok.Okay = data["ok"]
    ok.assert_all(result)
```

The available comparators are:
- `aok.anything()` will always succeed, no matter what the observed value is. 
- `aok.between(min, max)` must be greater than or equal to min and less than or equal
  to the specified min and max values. This can be a numeric or string value.
- `aok.equals(value)` must be an exact match between the values.
- `aok.greater(value)` must be greater than the specified value.
- `aok.greater_or_equal(value)` must be greater than or equal to the specified value.
- `aok.less(value)` must be less than the specified value.
- `aok.less_or_equal(value)` must be less than or equal to the specified value.
- `aok.like(string_value)` string compares against case-insensitive, unix-shell-style
  wildcard expressions, e.g. "foo*" would match "foo-bar".
- `aok.like_case(string_value)` string compares against case-sensitive, 
  unix-shell-style wildcard expressions, e.g. "Foo*" would match "Foo-Bar".
- `aok.match(string_regex_pattern)` matches the string against the specified regex 
  pattern.
- `aok.not_null(value)` must not be null/None, but can be anything else.
- `aok.optional(value)` must equal the specified value or be null/None.
