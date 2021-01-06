import dataclasses
import textwrap
import typing

import yaml
import yaml.constructor

import aok
from aok import _definitions

ArbitraryDict = typing.Dict[typing.Any, typing.Any]


@dataclasses.dataclass()
class Dict(_definitions.Comparator):
    """Main class in which aok assertions are made."""

    def compare(
        self,
        observed: ArbitraryDict,
        subset: bool = False,
    ) -> _definitions.Comparison:
        value = typing.cast(ArbitraryDict, self.value or {})
        other = observed or {}

        keys = set(list(value.keys()))
        if not subset:
            keys.update(set(list(other.keys())))

        results: typing.Dict[typing.Any, _definitions.Comparison] = {
            key: aok.to_comparator(self.value.get(key)).compare(other.get(key), subset)
            for key in keys
        }

        return _definitions.Comparison(
            operation=self.operation_name(),
            success=all([r.success for r in results.values()]),
            expected=self.value,
            observed=observed,
            children=results,
        )


@dataclasses.dataclass()
class Okay(Dict):
    """Root dictionary object for comparison."""

    def assert_subset(self, observed: ArbitraryDict, message: str = None):
        result = self.compare(observed, subset=True)
        heading = message or "One or more subset differences were found"
        assert result.success, "{}\n{}".format(
            heading,
            textwrap.indent(result.to_diff_info() or "", "  "),
        )

    def assert_all(self, observed: ArbitraryDict, message: str = None):
        result = self.compare(observed, subset=False)
        heading = message or "One or more exact differences were found"
        assert result.success, "{}\n{}".format(
            heading,
            textwrap.indent(result.to_diff_info() or "", "  "),
        )

    @classmethod
    def _from_yaml(cls, loader: yaml.Loader, node: yaml.Node) -> "Okay":
        """Loads the dict from a yaml parser."""
        try:
            return cls(value=loader.construct_mapping(node, deep=True))
        except yaml.constructor.ConstructorError:
            if node.value == "":
                return cls(value={})
            raise

    @classmethod
    def register(cls):
        """Overrides the registration in this case for base registration."""
        yaml.add_constructor("!aok", Okay.parse_yaml)


Okay.register()

__all__ = ["Okay", "Dict"]
