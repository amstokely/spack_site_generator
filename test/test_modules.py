import pytest
import yaml
from spack_site_generator.site import Modules


@pytest.fixture
def modules():
    """Fixture to create a fresh instance of Modules for each test."""
    return Modules()


def test_default_config_is_empty(modules):
    """A new Modules object starts with no enabled module types."""
    config_dict = modules.config.to_dict()
    assert "default" in config_dict
    assert config_dict["default"].get("enable", []) == []


def test_add_module_type_reflects_in_enable_list(modules):
    """Adding a module type makes it appear in the 'enable' list."""
    modules.add_module_type(
        module_type="tcl",
        autoload="all",
        hash_length=7,
        hide_implicits=True,
        include=["hdf5", "netcdf"],
        exclude=["openmpi"],
    )

    config_dict = modules.config.to_dict()

    # Behavior: "tcl" is listed as enabled
    assert "tcl" in config_dict["default"]["enable"]

    # Behavior: expected options are captured for the module type
    tcl_config = config_dict["default"]["tcl"]
    assert tcl_config["all"]["autoload"] == "all"
    assert tcl_config["hash_length"] == 7
    assert tcl_config["hide_implicits"] is True
    assert tcl_config["include"] == ["hdf5", "netcdf"]
    assert tcl_config["exclude"] == ["openmpi"]


def test_write_yaml_creates_expected_file(modules, tmp_path):
    """Writing configuration produces a YAML file with the expected structure."""
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

    # Reload the YAML to check behavior at file level
    with open(output_file, "r") as f:
        data = yaml.safe_load(f)

    # Behavior: "modules" key exists with "default" section
    assert "modules" in data
    assert "default" in data["modules"]

    # Behavior: "lmod" is enabled and has the expected options
    assert "lmod" in data["modules"]["default"]["enable"]
    lmod_config = data["modules"]["default"]["lmod"]
    assert lmod_config["all"]["autoload"] == "direct"
    assert lmod_config["hash_length"] == 5
    assert lmod_config["hide_implicits"] is False
    assert lmod_config["include"] == ["hdf5"]
    assert lmod_config["exclude"] == ["mpich"]


def test_write_yaml_without_modules_creates_empty_file(modules, tmp_path):
    """Writing immediately without adding modules should produce an empty config."""
    output_file = tmp_path / "modules.yaml"
    modules.write(path=output_file, spack_format=False)

    with open(output_file, "r") as f:
        data = yaml.safe_load(f)

    # Behavior: "modules" key exists with default section, but nothing enabled
    assert "modules" in data
    assert "default" in data["modules"]
    assert data["modules"]["default"].get("enable", []) == []
