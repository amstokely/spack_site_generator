import pytest

from spack_site_generator.utils.spack_yaml import to_yaml


@pytest.mark.parametrize(
    "yaml_dict, expected_yaml_str",
    [
        ({"a": {"b": {"c": "d"}}}, "a:\n  b:\n    c: d"),
        ({"a": [{"b": {"c": "d"}}]}, "a:\n- b:\n    c: d"),
        ({"a": [{"b": {"c": "d"}}]}, "a:\n- b:\n    c: d"),
        (
            {"a": [{"b": {"c": ["d", {"override": True}]}}]},
            "a:\n- b:\n    c:: \n    - d",
        ),
        ({"a": [{"override": True}, {"b": "c"}]}, "a::\n- b: c"),
    ],
)
def test_to_spack_format(yaml_dict, expected_yaml_str):
    assert to_yaml(yaml_dict) == expected_yaml_str
