from abc import ABC, abstractmethod

from pathlib import Path


class AbstractSiteConfig(ABC):
    """
    Abstract base class for all site configuration components.

    This class defines the interface that all site configuration
    sections (e.g., Packages, Compilers, Modules, Config) must follow.
    At a minimum, subclasses are required to implement ``write``,
    which outputs the configuration to a YAML file.
    """

    @abstractmethod
    def write(self, *, path: Path, spack_format: bool = True) -> None:
        """
        Write the configuration to disk.

        Args:
            path (Path): Path to the output YAML file.
            spack_format (bool): If True, format the file according to
                Spack's expected YAML schema.

        Note:
            Must be implemented by all subclasses of AbstractSiteConfig.
        """
        pass
