import typing

from aok import _definitions


class Optional(_definitions.Comparator):
    """Compares two value as an equality or allow None."""

    def _compare(
        self,
        observed: typing.Any,
        subset: bool = False,
    ) -> typing.Union[_definitions.Comparison, bool]:
        """Make an optional equality comparison."""
        return self.value is None or self.value == observed


class NotNull(_definitions.Comparator):
    """Won't allow a value to be null."""

    def _compare(
        self,
        observed: typing.Any,
        subset: bool = False,
    ) -> typing.Union[_definitions.Comparison, bool]:
        """Make an optional equality comparison."""
        return self.value is not None


NotNull.register()
not_null = getattr(NotNull, "constructor", NotNull)

Optional.register()
optional = getattr(Optional, "constructor", Optional)

__all__ = [
    "NotNull",
    "not_null",
    "Optional",
    "optional",
]
