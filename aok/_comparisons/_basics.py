import typing

import yaml

from aok import _definitions
from aok import _operations


class Equals(_definitions.Comparator):
    """Compares two values as an equality."""

    def _compare(
        self,
        observed: typing.Any,
        subset: bool = False,
    ) -> typing.Union[_definitions.Comparison, bool]:
        """Make an equals comparison."""
        return _operations.cast_compatible(self.value, observed) == observed


class Anything(_definitions.Comparator):
    """Allows anything for the given value."""

    def _compare(
        self,
        observed: typing.Any,
        subset: bool = False,
    ) -> typing.Union[_definitions.Comparison, bool]:
        """Anything will always be true."""
        return True

    @classmethod
    def from_yaml(cls, loader: yaml.Loader, node: yaml.Node) -> "Anything":
        return cls(None)


class Less(_definitions.Comparator):
    """Allows anything less than the given value."""

    def _compare(
        self,
        observed: typing.Any,
        subset: bool = False,
    ) -> typing.Union[_definitions.Comparison, bool]:
        """Less than will be true."""
        return _operations.cast_compatible(self.value, observed) > observed


class LessOrEqual(_definitions.Comparator):
    """Allows anything less than or equal the given value."""

    def _compare(
        self,
        observed: typing.Any,
        subset: bool = False,
    ) -> typing.Union[_definitions.Comparison, bool]:
        """Less than or equal will be true."""
        return _operations.cast_compatible(self.value, observed) >= observed


class Greater(_definitions.Comparator):
    """Allows anything greater than the given value."""

    def _compare(
        self,
        observed: typing.Any,
        subset: bool = False,
    ) -> typing.Union[_definitions.Comparison, bool]:
        """Greater than will be true."""
        return _operations.cast_compatible(self.value, observed) < observed


class GreaterOrEqual(_definitions.Comparator):
    """Allows anything greater than or equal to the given value."""

    def _compare(
        self,
        observed: typing.Any,
        subset: bool = False,
    ) -> typing.Union[_definitions.Comparison, bool]:
        """Greater than or equal will be true."""
        return _operations.cast_compatible(self.value, observed) <= observed


class Between(_definitions.Comparator):
    """Allows between the given values."""

    def _compare(
        self,
        observed: typing.Any,
        subset: bool = False,
    ) -> typing.Union[_definitions.Comparison, bool]:
        """Greater than or equal will be true."""
        casted_min = _operations.cast_compatible(self.value["min"], observed)
        casted_max = _operations.cast_compatible(self.value["max"], observed)
        return casted_min <= observed <= casted_max

    @classmethod
    def construct(cls, minimum: typing.Any, maximum: typing.Any) -> "Between":
        return cls({"min": minimum, "max": maximum})

    @classmethod
    def _from_yaml(cls, loader: yaml.Loader, node: yaml.Node) -> "Between":
        if isinstance(node, yaml.SequenceNode):
            loaded = loader.construct_sequence(node, deep=True)
            value = {"min": loaded[0], "max": loaded[1]}
        else:
            value = loader.construct_mapping(node, deep=True)
        return cls(value)


Anything.register()
anything = getattr(Anything, "constructor", Anything)

Between.register()
between = getattr(Between, "constructor", Between)

Equals.register()
equals = getattr(Equals, "constructor", Equals)

Greater.register()
greater = getattr(Greater, "constructor", Greater)

GreaterOrEqual.register()
greater_or_equal = getattr(GreaterOrEqual, "constructor", GreaterOrEqual)

Less.register()
less = getattr(Less, "constructor", Less)

LessOrEqual.register()
less_or_equal = getattr(LessOrEqual, "constructor", LessOrEqual)

__all__ = [
    "Anything",
    "anything",
    "Between",
    "between",
    "Equals",
    "equals",
    "Greater",
    "greater",
    "GreaterOrEqual",
    "greater_or_equal",
    "Less",
    "less",
    "LessOrEqual",
    "less_or_equal",
]
