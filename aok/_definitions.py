import dataclasses
import typing

import yaml

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

    def to_diff_info(
        self,
    ) -> typing.Optional[typing.Union[str, typing.Dict[str, typing.Any]]]:
        """Creates a formatted display message for use in assertions."""
        if self.success:
            return None

        if self.children:
            return {
                key: comparison.to_diff_info()
                for key, comparison in self.children.items()
                if not comparison.success
            }

        return "{operation}({expected}, {observed}){error}".format(
            operation=self.operation,
            expected=self.expected,
            observed=self.observed,
            error=f" [ERROR] {self.error}" if self.error else "",
        )

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
