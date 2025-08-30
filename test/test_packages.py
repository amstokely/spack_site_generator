import pytest
import yaml
from spack_site_generator.utils.autodict import AutoDict
from spack_site_generator.site import Packages


@pytest.fixture
def packages():
    """Fixture to create a fresh instance of Packages for each test."""
    return Packages()


def test_initialization(packages):
    """Test that the Packages class initializes correctly."""
    assert isinstance(packages.config, AutoDict)
    assert packages.config.to_dict() == {}


def test_add_provider(packages):
    """Test that a provider entry is correctly added."""
    packages.add_provider(
        provider_name="mpi",
        library_name="openmpi",
        library_version="4.1.1",
        buildable=True,
    )

    providers = packages.config["all"]["providers"]
    assert "mpi" in providers
    assert providers["mpi"] == ["openmpi@4.1.1", {"override": True}]
    assert packages.config["mpi"]["buildable"] is True


def test_add_compiler(packages):
    """Test that a compiler entry is correctly added."""
    packages.add_compiler(name="gcc", version="11.2.0")

    assert "compiler" in packages.config["all"]
    assert packages.config["all"]["compiler"] == ["gcc@11.2.0", {"override": True}]


import pytest


@pytest.mark.parametrize("override", [False, True])
def test_add_package(packages, override):
    """Test that a package entry is correctly added with and without override."""
    packages.add_package(
        name="hdf5",
        spec="hdf5@1.12.0",
        buildable=False,
        modules=["hdf5/1.12.0"],
        prefix="/usr/local/hdf5",
        extra_attributes={
            "headers": "/usr/local/include",
            "libs": "/usr/local/lib/libhdf5.so",
        },
        override=override,
    )

    assert "hdf5" in packages.config
    assert packages.config["hdf5"]["externals"] == [
        {
            "spec": "hdf5@1.12.0",
            "prefix": "/usr/local/hdf5",
            "modules": ["hdf5/1.12.0"],
            "extra_attributes": {
                "headers": "/usr/local/include",
                "libs": "/usr/local/lib/libhdf5.so",
            },
        }
    ]
    assert packages.config["hdf5"]["buildable"] is False

    # Only assert the override flag when it is set
    if override:
        assert packages.config["hdf5"]["override"] is True
    else:
        assert "override" not in packages.config["hdf5"]


def test_write_yaml(packages, tmp_path):
    """Test that the YAML file is written correctly."""
    packages.add_provider(
        provider_name="mpi",
        library_name="openmpi",
        library_version="4.1.1",
        buildable=True,
    )
    packages.add_compiler(name="gcc", version="11.2.0")
    packages.add_package(
        name="hdf5",
        spec="hdf5@1.12.0",
        buildable=False,
        modules=["hdf5/1.12.0"],
        prefix="/usr/local/hdf5",
        extra_attributes={
            "headers": "/usr/local/include",
            "libs": "/usr/local/lib/libhdf5.so",
        },
        override=False,
    )

    output_file = tmp_path / "packages.yaml"
    packages.write(path=output_file, spack_format=False)

    with open(output_file, "r") as f:
        data = yaml.safe_load(f)

    assert "packages" in data
    assert "mpi" in data["packages"]
    assert "hdf5" in data["packages"]
    assert "compiler" in data["packages"]["all"]
    assert "externals" in data["packages"]["hdf5"]
    assert "modules" in data["packages"]["hdf5"]["externals"][0]
    assert "extra_attributes" in data["packages"]["hdf5"]["externals"][0]
