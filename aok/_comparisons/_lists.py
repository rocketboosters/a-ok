import dataclasses
import typing

import aok
from aok import _definitions


@dataclasses.dataclass()
class List(_definitions.Comparator):
    """Container class for list comparisons, which compare the lists element-wise."""

    def compare(
        self,
        observed: typing.List[typing.Any],
        subset: bool = False,
    ) -> _definitions.Comparison:
        value = typing.cast(typing.List[typing.Any], self.value or [])
        other = observed or []

        if len(value) != len(other):
            return _definitions.Comparison(
                operation="list_length",
                success=False,
                expected=len(value),
                observed=len(other),
            )

        results: typing.List[_definitions.Comparison] = [
            aok.to_comparator(exp).compare(obs, subset)
            for exp, obs in zip(value, other)
        ]

        return _definitions.Comparison(
            operation=self.operation_name(),
            success=all([r.success for r in results]),
            expected=self.value,
            observed=observed,
            children={f"index_{i}": r for i, r in enumerate(results)},
        )


@dataclasses.dataclass()
class Tuple(_definitions.Comparator):
    """Container class for tuple comparisons, which compare the tuples element-wise."""

    def compare(
        self,
        observed: typing.Tuple[typing.Any, ...],
        subset: bool = False,
    ) -> _definitions.Comparison:
        value = typing.cast(typing.Tuple[typing.Any, ...], self.value or tuple())
        other = observed or tuple()

        if len(value) != len(other):
            return _definitions.Comparison(
                operation="tuple_length",
                success=False,
                expected=len(value),
                observed=len(other),
            )

        results: typing.List[_definitions.Comparison] = [
            aok.to_comparator(exp).compare(obs, subset)
            for exp, obs in zip(value, other)
        ]

        return _definitions.Comparison(
            operation=self.operation_name(),
            success=all([r.success for r in results]),
            expected=self.value,
            observed=observed,
            children={f"index_{i}": r for i, r in enumerate(results)},
        )


List.register()
Tuple.register()

__all__ = ["List", "Tuple"]
