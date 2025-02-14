import pytest
import yaml
from spack_site_generator.site import Compilers

@pytest.fixture
def compilers():
    """Fixture to create a fresh instance of Compilers for each test."""
    return Compilers()

def test_initialization(compilers):
    """Test that the Compilers class initializes with an override entry."""
    assert "compilers" in compilers.config
    assert compilers.config["compilers"] == [{"override": True}]

def test_add_compiler(compilers):
    """Test that a compiler entry is correctly added."""
    compiler_entry = {
        "spec": "gcc@11.2.0",
        "paths": {"cc": "/usr/bin/gcc", "cxx": "/usr/bin/g++", "fc": "/usr/bin/gfortran"},
        "flags": {"cflags": "-O2", "cxxflags": "-O2"},
        "operating_system": "ubuntu20.04",
        "target": "x86_64",
        "modules": ["gcc/11.2.0"],
        "environment": {"set": {"OMP_NUM_THREADS": "4"}},
        "extra_rpaths": ["/usr/local/lib"]
    }

    compilers.add_compiler(**compiler_entry)

    assert len(compilers.config["compilers"]) == 2  # Override entry + added compiler
    assert compilers.config["compilers"][1]["compiler"] == compiler_entry

def test_write_yaml(compilers, tmp_path):
    """Test that the YAML file is written correctly."""
    compiler_entry = {
        "spec": "gcc@11.2.0",
        "paths": {"cc": "/usr/bin/gcc", "cxx": "/usr/bin/g++", "fc": "/usr/bin/gfortran"},
        "flags": {"cflags": "-O2", "cxxflags": "-O2"},
        "operating_system": "ubuntu20.04",
        "target": "x86_64",
        "modules": ["gcc/11.2.0"],
        "environment": {"set": {"OMP_NUM_THREADS": "4"}},
        "extra_rpaths": ["/usr/local/lib"]
    }

    compilers.add_compiler(**compiler_entry)

    output_file = tmp_path / "compilers.yaml"
    compilers.write(filename=str(output_file), spack_format=False)

    with open(output_file, "r") as f:
        data = yaml.safe_load(f)

    assert "compilers" in data
    assert len(data["compilers"]) == 2
    assert data["compilers"][1]["compiler"] == compiler_entry

