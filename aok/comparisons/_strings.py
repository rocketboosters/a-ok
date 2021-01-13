import fnmatch
import re
import typing

import yaml

from aok import _definitions


class Like(_definitions.Comparator):
    """Compares strings using unix-shell wildcard like regexes."""

    def _compare(
        self,
        observed: typing.Any,
        subset: bool = False,
    ) -> typing.Union[_definitions.Comparison, bool]:
        return fnmatch.fnmatch(observed, self.value)

    @classmethod
    def _from_yaml(cls, loader: yaml.Loader, node: yaml.Node) -> "Like":
        value: str = loader.construct_python_str(node)
        return cls(value)


class LikeCase(_definitions.Comparator):
    """Compares strings using unix-shell wildcard like regexes."""

    def _compare(
        self,
        observed: typing.Any,
        subset: bool = False,
    ) -> typing.Union[_definitions.Comparison, bool]:
        return fnmatch.fnmatchcase(observed, self.value)

    @classmethod
    def _from_yaml(cls, loader: yaml.Loader, node: yaml.Node) -> "LikeCase":
        value: str = loader.construct_python_str(node)
        return cls(value)


class Match(_definitions.Comparator):
    """Compares strings using the compiled regex."""

    def _compare(
        self,
        observed: typing.Any,
        subset: bool = False,
    ) -> typing.Union[_definitions.Comparison, bool]:
        """Determines if the value matches the regular expression."""
        pattern = re.compile(self.value["regex"], flags=self.value.get("flags", 0))
        return pattern.match(observed) is not None

    @classmethod
    def _from_yaml(cls, loader: yaml.Loader, node: yaml.Node) -> "Match":
        if isinstance(node, yaml.ScalarNode):
            regex = loader.construct_python_str(node)
            value = {"regex": regex}
        else:
            value = loader.construct_mapping(node, deep=True)
        return cls(value)


Like.register()
like = getattr(Like, "constructor", Like)

LikeCase.register()
like_case = getattr(LikeCase, "constructor", LikeCase)

Match.register()
match = getattr(Match, "constructor", Match)

__all__ = [
    "Like",
    "like",
    "LikeCase",
    "like_case",
    "Match",
    "match",
]
