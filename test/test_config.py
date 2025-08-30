import pytest
import yaml
from spack_site_generator.site import Config


@pytest.fixture
def config():
    """Fixture to create a fresh instance of Config for each test."""
    return Config()


def test_default_config_is_empty(config):
    """A new Config object should start with no settings."""
    assert config.config.to_dict() == {}


def test_set_build_jobs_reflects_in_config(config):
    """Setting build_jobs updates the configuration."""
    config.set_build_jobs(build_jobs=8)
    assert config.config.to_dict()["build_jobs"] == 8


def test_set_stage_paths_reflects_in_config(config):
    """Setting stage paths updates the configuration."""
    config.set_stage_paths(
        build_stage_path="/path/to/build", test_stage_path="/path/to/test"
    )

    config_dict = config.config.to_dict()
    assert config_dict["build_stage"] == "/path/to/build"
    assert config_dict["test_stage"] == "/path/to/test"


def test_set_cache_paths_reflects_in_config(config):
    """Setting cache paths updates the configuration."""
    config.set_cache_paths(
        source_cache_path="/path/to/source", misc_cache_path="/path/to/misc"
    )

    config_dict = config.config.to_dict()
    assert config_dict["source_cache"] == "/path/to/source"
    assert config_dict["misc_cache"] == "/path/to/misc"


def test_write_yaml_creates_expected_file(config, tmp_path):
    """Writing configuration produces a YAML file with the expected structure."""
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

    # Behavior: top-level "config" section with expected settings
    assert "config" in data
    assert data["config"]["build_jobs"] == 8
    assert data["config"]["source_cache"] == "/path/to/source"
    assert data["config"]["misc_cache"] == "/path/to/misc"
    assert data["config"]["build_stage"] == "/path/to/build"
    assert data["config"]["test_stage"] == "/path/to/test"
