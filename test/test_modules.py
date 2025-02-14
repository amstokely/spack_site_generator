import pytest
import yaml
from spack_site_generator.utils.autodict import AutoDict
from spack_site_generator.site import Modules


@pytest.fixture
def modules():
    """Fixture to create a fresh instance of Modules for each test."""
    return Modules()


def test_initialization(modules):
    """Test that the Modules class initializes correctly."""
    assert isinstance(modules.config, AutoDict)
    assert modules.config.to_dict() == {"default": {"enable": []}}


def test_add_module_type(modules):
    """Test that a module type entry is correctly added."""
    modules.add_module_type(
        module_type="tcl",
        autoload="all",
        hash_length=7,
        hide_implicits=True,
        include=["hdf5", "netcdf"],
        exclude=["openmpi"],
    )

    assert "tcl" in modules.config["default"]
    assert "enable" in modules.config["default"]
    assert "tcl" in modules.config["default"]["enable"]
    assert modules.config["default"]["tcl"]["all"]["autoload"] == "all"
    assert modules.config["default"]["tcl"]["hash_length"] == 7
    assert modules.config["default"]["tcl"]["hide_implicits"] is True
    assert modules.config["default"]["tcl"]["include"] == ["hdf5", "netcdf"]
    assert modules.config["default"]["tcl"]["exclude"] == ["openmpi"]


def test_write_yaml(modules, tmp_path):
    """Test that the YAML file is written correctly."""
    modules.add_module_type(
        module_type="lmod",
        autoload="direct",
        hash_length=5,
        hide_implicits=False,
        include=["hdf5"],
        exclude=["mpich"],
    )

    output_file = tmp_path / "modules.yaml"
    modules.write(path=output_file, spack_format=False)

    with open(output_file, "r") as f:
        data = yaml.safe_load(f)

    assert "modules" in data
    assert "lmod" in data["modules"]["default"]
    assert data["modules"]["default"]["enable"] == ["lmod", {"override": True}]
    assert data["modules"]["default"]["lmod"]["all"]["autoload"] == "direct"
    assert data["modules"]["default"]["lmod"]["hash_length"] == 5
    assert data["modules"]["default"]["lmod"]["hide_implicits"] is False
    assert data["modules"]["default"]["lmod"]["include"] == ["hdf5"]
    assert data["modules"]["default"]["lmod"]["exclude"] == ["mpich"]
