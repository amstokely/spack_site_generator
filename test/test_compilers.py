import pytest
import yaml
from spack_site_generator.site import Compilers


@pytest.fixture
def compilers():
    """Fixture to create a fresh instance of Compilers for each test."""
    return Compilers()


def test_default_compilers_config_starts_with_override(compilers):
    """A new Compilers object should include a default override entry."""
    config_dict = compilers.config.to_dict()
    assert "compilers" in config_dict
    # Behavior: the override entry is present at initialization
    assert config_dict["compilers"][0] == {"override": True}


def test_add_compiler_reflects_in_config(compilers):
    """Adding a compiler should append it to the compilers list."""
    compiler_entry = {
        "spec": "gcc@11.2.0",
        "paths": {
            "cc": "/usr/bin/gcc",
            "cxx": "/usr/bin/g++",
            "fc": "/usr/bin/gfortran",
        },
        "flags": {"cflags": "-O2", "cxxflags": "-O2"},
        "operating_system": "ubuntu20.04",
        "target": "x86_64",
        "modules": ["gcc/11.2.0"],
        "environment": {"set": {"OMP_NUM_THREADS": "4"}},
        "extra_rpaths": ["/usr/local/lib"],
    }

    compilers.add_compiler(**compiler_entry)

    config_dict = compilers.config.to_dict()
    assert len(config_dict["compilers"]) == 2  # override + added compiler
    assert config_dict["compilers"][1]["compiler"] == compiler_entry


def test_write_yaml_creates_expected_file(compilers, tmp_path):
    """Writing configuration should produce a YAML file with compilers listed."""
    compiler_entry = {
        "spec": "gcc@11.2.0",
        "paths": {
            "cc": "/usr/bin/gcc",
            "cxx": "/usr/bin/g++",
            "fc": "/usr/bin/gfortran",
        },
        "flags": {"cflags": "-O2", "cxxflags": "-O2"},
        "operating_system": "ubuntu20.04",
        "target": "x86_64",
        "modules": ["gcc/11.2.0"],
        "environment": {"set": {"OMP_NUM_THREADS": "4"}},
        "extra_rpaths": ["/usr/local/lib"],
    }

    compilers.add_compiler(**compiler_entry)

    output_file = tmp_path / "compilers.yaml"
    compilers.write(path=output_file, spack_format=False)

    with open(output_file, "r") as f:
        data = yaml.safe_load(f)

    # Behavior: compilers section exists and includes both override + entry
    assert "compilers" in data
    assert len(data["compilers"]) == 2
    assert data["compilers"][1]["compiler"] == compiler_entry


def test_write_yaml_without_compilers_creates_only_override(compilers, tmp_path):
    """Writing without adding compilers should produce just the override entry."""
    output_file = tmp_path / "compilers.yaml"
    compilers.write(path=output_file, spack_format=False)

    with open(output_file, "r") as f:
        data = yaml.safe_load(f)

    # Behavior: compilers list exists and contains only override
    assert "compilers" in data
    assert data["compilers"] == [{"override": True}]
