import pytest
from pathlib import Path
from spack_site_generator.site import Site


def test_site_write_creates_expected_files(tmp_path: Path):
    """Site.write should create the expected YAML files in the site directory."""
    site = Site(name="testsite")

    # Add a minimal package so write() produces output
    site.packages.add_package(
        name="dummy",
        spec="dummy@1.0",
        buildable=False,
        modules=[],
        prefix="/opt/dummy",
        extra_attributes={},
        override=False,
    )
    site.config.set_build_jobs(build_jobs=4)

    # Write the site configuration into a temporary directory
    site.write(path=tmp_path)

    site_dir = tmp_path / "testsite"
    expected_files = [
        site_dir / "packages.yaml",
        site_dir / "compilers.yaml",
        site_dir / "modules.yaml",
        site_dir / "config.yaml",
    ]

    # Behavior: site directory exists
    assert site_dir.exists() and site_dir.is_dir()

    # Behavior: all expected files are created
    for f in expected_files:
        assert f.exists() and f.is_file()
