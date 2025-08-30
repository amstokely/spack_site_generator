"""
Module for managing and generating a Spack `config.yaml` file.

This module provides the `Config` class, which allows users to define and
customize Spack's configuration settings, including build jobs, stage paths,
and cache paths. The configuration can then be written to a `config.yaml` file.

Classes:
    Config: Handles the configuration of Spack's `config.yaml` file.
"""

from pathlib import Path

from spack_site_generator.utils.autodict import AutoDict
from spack_site_generator.site.abstract_site_config import AbstractSiteConfig
from spack_site_generator.utils import to_yaml


class Config(AbstractSiteConfig):
    """
    A class for managing Spack's `config.yaml` file.

    This class provides methods to define Spack's configuration settings,
    including build jobs, stage paths, and cache paths. The final configuration
    can be exported as a YAML file.

    Attributes:
        config (AutoDict): A dictionary-like structure storing configuration settings.

    Methods:
        set_build_jobs(build_jobs: int) -> None:
            Set the number of parallel build jobs.

        set_stage_paths(build_stage_path: str, test_stage_path: str) -> None:
            Set paths for build and test staging areas.

        set_cache_paths(source_cache_path: str, misc_cache_path: str) -> None:
            Set paths for source cache and miscellaneous cache.

        write(path: Path, spack_format: bool = True) -> None:
            Write the configuration to a `config.yaml` file.
    """

    def __init__(self):
        """
        Initialize an empty configuration using an AutoDict.
        """
        self.config: AutoDict = AutoDict()

    def set_build_jobs(self, *, build_jobs: int) -> None:
        """
        Set the number of parallel build jobs.

        Args:
            build_jobs (int): The number of build jobs to configure.
        """
        self.config["build_jobs"] = build_jobs

    def set_stage_paths(self, *, build_stage_path: str, test_stage_path: str) -> None:
        """
        Define stage paths for Spack.

        Args:
            build_stage_path (str): Path to the build stage directory.
            test_stage_path (str): Path to the test stage directory.
        """
        if build_stage_path:
            self.config["build_stage"] = build_stage_path
        if test_stage_path:
            self.config["test_stage"] = test_stage_path

    def set_cache_paths(self, *, source_cache_path: str, misc_cache_path: str) -> None:
        """
        Define cache paths for Spack.

        Args:
            source_cache_path (str): Path to the source cache directory.
            misc_cache_path (str): Path to the miscellaneous cache directory.
        """
        if source_cache_path:
            self.config["source_cache"] = source_cache_path
        if misc_cache_path:
            self.config["misc_cache"] = misc_cache_path

    def write(self, *, path: Path, spack_format: bool = True) -> None:
        """
        Write the configuration to a `config.yaml` file.

        If the configuration is empty, the method does nothing.

        Args:
            path (Path): The file path where the configuration will be written.
            spack_format (bool, optional): Whether to format the YAML output
                                           in Spack's style. Defaults to True.
        """
        if self.config.empty():
            return
        config_dict = {"config": self.config.to_dict()}
        with open(path, "w") as f:
            f.write(to_yaml(config_dict, spack_format=spack_format))
