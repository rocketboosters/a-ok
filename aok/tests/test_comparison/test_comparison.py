import pathlib

import pytest
import yaml

import aok

path = pathlib.Path(__file__).parent.joinpath("scenario.yaml")


def test_comparison_subset():
    """Should assert failure on comparison."""
    scenario = yaml.full_load(path.read_text())

    okay: aok.Okay = scenario["expected"]
    with pytest.raises(AssertionError):
        okay.assert_subset(scenario["observed"])


def test_comparison_exact():
    """Should assert failure on comparison."""
    scenario = yaml.full_load(path.read_text())

    okay: aok.Okay = scenario["expected"]
    with pytest.raises(AssertionError):
        okay.assert_all(scenario["observed"])
