from pathlib import Path
from typing import Optional, Dict, Any

from spack_site_generator.utils.autodict import AutoDict
from spack_site_generator.utils.spack_yaml import to_yaml
from spack_site_generator.site.abstract_site_config import AbstractSiteConfig


class Compilers(
    AbstractSiteConfig):
    """
    Represents a Spack site configuration for compilers.

    This class allows managing a list of compiler configurations, ensuring they
    are properly structured and formatted for Spack.

    Attributes:
        config (AutoDict): A dictionary-like structure that stores compiler configurations.
    """

    def __init__(self):
        """
        Initialize the compiler configuration with a base structure.

        The default configuration includes an override flag to ensure that
        compiler definitions take precedence in Spack.
        """
        self.config = AutoDict()
        self.config["compilers"] = [{"override": True}]

    def add_compiler(
        self,
        *,
        spec: str,
        paths: Dict[str, str],
        operating_system: str,
        target: str,
        flags: Dict[str, Any],
        modules: Optional[list[str]],
        environment: Optional[Dict[str, Any]],
        extra_rpaths: Optional[list[str]],
    ) -> None:
        """
        Add a new compiler entry to the configuration.

        Args:
            spec (str): The compiler specification (e.g., "gcc@11.2.0").
            paths (Dict[str, str]): A dictionary specifying compiler paths, typically:
                - "cc" (C compiler)
                - "cxx" (C++ compiler)
                - "f77" (Fortran 77 compiler)
                - "fc" (Fortran compiler)
            operating_system (str): The OS associated with this compiler.
            target (str): The target architecture for the compiler.
            flags (Dict[str, Any]): A dictionary containing compiler flags (e.g., CFLAGS, CXXFLAGS).
            modules (Optional[list[str]]): A list of modules that should be loaded before using the compiler.
            environment (Optional[Dict[str, Any]]): Environment variables for the compiler.
            extra_rpaths (Optional[list[str]]): Additional library paths to be added to the RPATH.
        """
        self.config["compilers"].append(
            {
                "compiler": {
                    "spec": spec,
                    "paths": paths,
                    "flags": flags,
                    "operating_system": operating_system,
                    "target": target,
                    "modules": modules,
                    "environment": environment,
                    "extra_rpaths": extra_rpaths,
                }
            }
        )

    def write(self, *, path: Path, spack_format: Optional[bool] = True) -> None:
        """
        Write the compiler configuration to a YAML file. If the configuration is empty,
        no file will be written.

        Args:
            path (str): The file path where the configuration will be saved.
            spack_format (Optional[bool]): Whether to format the YAML output in Spack style.
                                           Defaults to True.
        """
        if self.config.empty():
            return
        with open(path, "w") as f:
            f.write(to_yaml(self.config.to_dict(), spack_format=spack_format))
