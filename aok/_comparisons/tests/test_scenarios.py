import pathlib

import yaml
from pytest import mark

import aok

directory = pathlib.Path(__file__).parent.joinpath("scenarios").absolute()

scenario_paths = [p.name for p in directory.iterdir() if p.name.endswith(".yaml")]


@mark.parametrize("filename", scenario_paths)
def test_scenario(filename: str):
    """Test the expected scenario against the executed aok validation."""
    path = directory.joinpath(filename)
    scenario = yaml.full_load(path.read_text())
    comparator: aok.Okay = scenario["comparator"]
    result = comparator.compare(
        scenario["observed"],
        subset=scenario.get("subset", False),
    )

    expectations = scenario["expected"]
    assert result.success == expectations["success"], result.to_diff_info()
    assert result.failed_keys() == set(expectations.get("failed_keys", []))
