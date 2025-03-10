from pathlib import Path
from typing import Optional

from spack_site_generator.utils.autodict import AutoDict
from spack_site_generator.utils.spack_yaml import to_yaml
from spack_site_generator.site.abstract_site_config import AbstractSiteConfig


class Modules(AbstractSiteConfig):
    """
    Represents the module configuration for a Spack site.

    This class manages the configuration of module types and their related
    settings, ensuring they are properly structured for Spack.

    Attributes:
        config (AutoDict): A dictionary-like structure to store module configurations.
    """

    def __init__(self) -> None:
        """
        Initialize the module configuration with a default structure.

        The `enable` key is initialized as an empty list to store enabled module types.
        """
        self.config: AutoDict = AutoDict()
        self.config["default"]["enable"] = []  # Ensure the `enable` key exists

    def add_module_type(
        self,
        *,
        module_type: str,
        autoload: str,
        hash_length: int,
        hide_implicits: bool,
        include: list[str],
        exclude: list[str],
    ) -> None:
        """
            Add a module type configuration.

            This method configures a specific module type and its associated settings.

            Args:
                module_type (str): The type of module to enable (e.g., "tcl", "lmod").
                autoload (str): The autoload behavior (e.g., "all", "direct").
                hash_length (int): The length of hash values for module naming.
                hide_implicits (bool): Whether implicit modules should be hidden.
                exclude (Optional[list[str]]): Packages to exclude from module generation.
                include (Optional[list[str]]): Packages to include in module generation.

        """
        self.config["default"]["enable"].append(module_type)
        self.config["default"]["enable"].append({"override": True})
        self.config["default"][module_type]["all"]["autoload"] = autoload
        self.config["default"][module_type]["hash_length"] = hash_length
        self.config["default"][module_type]["hide_implicits"] = hide_implicits
        if exclude:
            self.config["default"][module_type]["exclude"] = exclude
        if include:
            self.config["default"][module_type]["include"] = include

    def write(self, *, path: Path, spack_format: Optional[bool] = True) -> None:
        """
        Write the module configuration to a YAML file. If the configuration is empty,
        no file will be written.

        Args:
            path (str): The file path where the configuration will be saved.
            spack_format (bool, optional): Whether to format the YAML output
                                           in Spack style. Defaults to True.
        """
        if self.config.empty():
            return
        config_dict = {"modules": self.config.to_dict()}
        with open(path, "w") as f:
            f.write(to_yaml(config_dict, spack_format=spack_format))
