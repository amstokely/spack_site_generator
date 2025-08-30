from pathlib import Path
from typing import List, Dict, Any, Optional

from spack_site_generator.utils.autodict import AutoDict
from spack_site_generator.utils.spack_yaml import to_yaml
from spack_site_generator.site.abstract_site_config import AbstractSiteConfig


class Packages(AbstractSiteConfig):
    """
    Represents the package configuration for a Spack site.

    This class allows managing compiler definitions, external package configurations,
    and provider mappings in Spack's package configuration system.

    Attributes:
        config (AutoDict): A dictionary-like structure that stores package configurations.
    """

    def __init__(self) -> None:
        """
        Initialize the package configuration with an empty structure.
        """
        self.config: AutoDict = AutoDict()

    def add_provider(
        self,
        *,
        provider_name: str,
        library_name: str,
        library_version: str,
        buildable: bool,
    ) -> None:
        """
        Add a provider mapping to the package configuration.

        This method defines a provider (e.g., MPI, BLAS, LAPACK) that
        maps to a specific library and version.

        Args:
            provider_name (str): The name of the provider (e.g., "mpi").
            library_name (str): The name of the library providing the functionality.
            library_version (str): The specific version of the library.
            buildable (bool): Whether the provider can be built from source.
        """
        self.config["all"]["providers"][provider_name] = [
            f"{library_name}@{library_version}",
        ]
        self.config["all"]["providers"][provider_name].append({"override": True})
        self.config[provider_name]["buildable"] = buildable

    def add_compiler(self, *, name: str, version: str) -> None:
        """
        Add a compiler definition to the package configuration.

        Args:
            name (str): The name of the compiler (e.g., "gcc", "intel").
            version (str): The version of the compiler (e.g., "11.2.0").
        """
        self.config["all"]["compiler"] = [
            f"{name}@{version}",
            {"override": True},
        ]

    def add_package(
        self,
        *,
        name: str,
        spec: str,
        buildable: bool,
        modules: List[str],
        prefix: str,
        extra_attributes: Dict[str, str],
        override: bool,
    ) -> None:
        """
        Add an external package definition to the site configuration.

        This method registers a package under ``packages.yaml``, including its
        spec string, installation prefix, module dependencies, and optional
        extra attributes. It is primarily used to describe external packages
        (e.g., system compilers, MPI libraries) that Spack should not build
        from source. If ``override`` is True, any existing definition for the
        package will be replaced.

        Args:
            name (str): Logical package name (e.g., "openmpi").
            spec (str): Spack spec string with version and compiler (e.g.,
                "openmpi@5.0.5%gcc@11.4.0").
            buildable (bool): Whether Spack may build this package from source.
                Use False for system-installed externals.
            modules (List[str]): Module names that must be loaded to use this
                package (e.g., ["openmpi/5.0.5"]).
            prefix (str): Absolute installation path of the package.
            extra_attributes (Dict[str, str]): Additional configuration fields
                for the external package. Common keys include:
                    - "headers": Path to the package's include directory.
                    - "libs": Path to the main library file or directory.
            override (bool): If True, replace any existing package definition
                for this name in the configuration.
        """

        package_entry = self.config[name]
        package_entry["buildable"] = buildable
        if override:
            package_entry["override"] = True
        package_entry["externals"] = [{"spec": spec, "prefix": prefix}]
        if modules:
            package_entry["externals"][0]["modules"] = modules
        if extra_attributes:
            package_entry["externals"][0]["extra_attributes"] = extra_attributes

    def write(self, *, path: Path, spack_format: bool = True) -> None:
        """
        Write the package configuration to a YAML file. If the configuration is empty,
        no file will be written.

        Args:
            path (str): The file path where the configuration will be saved.
            spack_format (bool, optional): Whether to format the YAML output in Spack style.
                                           Defaults to True.
        """
        if self.config.empty():
            return
        config_dict = {"packages": self.config.to_dict()}
        with open(path, "w") as file:
            file.write(to_yaml(config_dict, spack_format=spack_format))
