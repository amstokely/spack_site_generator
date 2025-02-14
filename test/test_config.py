import pytest
import yaml
from spack_site_generator.utils.autodict import AutoDict
from spack_site_generator.site import Config


@pytest.fixture
def config():
    """Fixture to create a fresh instance of Config for each test."""
    return Config()


def test_initialization(config):
    """Test that the Config class initializes correctly."""
    assert isinstance(config.config, AutoDict)
    assert config.config.to_dict() == {}


def test_set_build_jobs(config):
    """Test that the build_jobs setting is correctly set."""
    config.set_build_jobs(build_jobs=8)
    assert config.config["build_jobs"] == 8


def test_set_stage_paths(config):
    """Test that stage paths are correctly set."""
    config.set_stage_paths(
        build_stage_path="/path/to/build", test_stage_path="/path/to/test"
    )

    assert config.config["build_stage"] == "/path/to/build"
    assert config.config["test_stage"] == "/path/to/test"


def test_set_cache_paths(config):
    """Test that cache paths are correctly set."""
    config.set_cache_paths(
        source_cache_path="/path/to/source", misc_cache_path="/path/to/misc"
    )

    assert config.config["source_cache"] == "/path/to/source"
    assert config.config["misc_cache"] == "/path/to/misc"


def test_write_yaml(config, tmp_path):
    """Test that the YAML file is written correctly."""
    config.set_build_jobs(build_jobs=8)
    config.set_cache_paths(
        source_cache_path="/path/to/source", misc_cache_path="/path/to/misc"
    )
    config.set_stage_paths(
        build_stage_path="/path/to/build", test_stage_path="/path/to/test"
    )

    output_file = tmp_path / "config.yaml"
    config.write(path=output_file, spack_format=False)

    with open(output_file, "r") as f:
        data = yaml.safe_load(f)

    assert "config" in data
    assert data["config"]["build_jobs"] == 8
    assert data["config"]["source_cache"] == "/path/to/source"
    assert data["config"]["misc_cache"] == "/path/to/misc"
    assert data["config"]["build_stage"] == "/path/to/build"
    assert data["config"]["test_stage"] == "/path/to/test"
