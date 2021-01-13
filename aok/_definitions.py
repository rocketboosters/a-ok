import dataclasses
import pprint
import typing

import yaml
import yaml.constructor

from aok import _utils


@dataclasses.dataclass()
class Comparator:
    """Okay style comparison class for comparing values."""

    value: typing.Any

    @classmethod
    def operation_name(cls) -> str:
        """..."""
        return _utils.to_snake_case(cls.__name__)

    def _compare(
        self,
        observed: typing.Any,
        subset: bool = False,
    ) -> typing.Union["Comparison", bool]:
        """Make the comparison."""
        return False

    def compare(self, observed: typing.Any, subset: bool = False) -> "Comparison":
        """
        Compares the observed value with the expected value set in this
        comparator object.

        :param observed:
            Value against which to make the comparison.
        :param subset:
            If this is a non-scalar value, e.g. dict, this will allow for dictionary
            subsets to be compared against what is available while accepting other
            values not specified here to be included in the observed value.
        :return:
            Comparator object specifying the result of the comparison with
            supporting data for assertion and other display.
        """
        try:
            result = self._compare(observed, subset)
        except Exception as error:
            return Comparison(
                operation=self.operation_name(),
                success=False,
                expected=self.value,
                observed=observed,
                error=error,
            )

        if isinstance(result, Comparison):
            return result

        return Comparison(
            operation=self.operation_name(),
            success=result,
            expected=self.value,
            observed=observed,
        )

    @classmethod
    def _from_yaml(cls, loader: yaml.Loader, node: yaml.Node) -> "Comparator":
        """Internal yaml node parsing. Defaults to a scalar value."""
        value = loader.construct_scalar(node)
        return cls(value)

    @classmethod
    def parse_yaml(cls, loader: yaml.Loader, node: yaml.Node) -> "Comparator":
        """Yaml alternative constructor that builds the comparator from a yaml node."""
        return cls._from_yaml(loader, node)

    @classmethod
    def register(cls):
        """Registers the comparator with the PyYaml loader."""
        yaml.add_constructor(f"!aok.{cls.operation_name()}", cls.parse_yaml)


@dataclasses.dataclass()
class Comparison:
    """Contains the results and information for an arbitrary comparison."""

    operation: str
    success: bool
    expected: typing.Any
    observed: typing.Any
    children: typing.Dict[typing.Any, "Comparison"] = dataclasses.field(
        default_factory=lambda: {},
    )
    error: typing.Optional[Exception] = None

    def to_diff_data(self) -> typing.Optional[typing.Dict[str, typing.Any]]:
        """Creates a data structure of differences for display."""
        if self.success:
            return None

        if self.children:
            return {
                key: comparison.to_diff_data()
                for key, comparison in self.children.items()
                if not comparison.success
            }

        output = {
            "OPERATION": self.operation,
            "EXPECTED": self.expected,
            "OBSERVED": self.observed,
        }
        if self.error:
            output["error"] = str(self.error)

        return output

    def to_diff_info(self) -> typing.Optional[str]:
        """Creates a formatted display message for use in assertions."""
        if self.success:
            return None

        difference = self.to_diff_data()
        try:
            return yaml.dump(difference)
        except yaml.constructor.ConstructorError:
            return pprint.pformat(difference, indent=2)

    def failed_keys(self) -> typing.Set[str]:
        """Lists failed absolute keys."""
        if self.success or not self.children:
            return set()

        outputs = []
        for key, child in self.children.items():
            if child.success:
                continue

            if not child.children:
                outputs.append(key)

            outputs += [f"{key}.{child_key}" for child_key in child.failed_keys()]

        return set(outputs)
