from pathlib import Path

from spack_site_generator.site import Compilers
from spack_site_generator.site import Modules
from spack_site_generator.site import Packages
from spack_site_generator.site import Config


class Site(object):
    """
    Represents a Spack site configuration.

    A Site encapsulates all the configuration components needed to describe
    a computing environment (packages, compilers, modules, and global
    settings). Once defined, the site can be written to disk as a set of
    YAML files in the format Spack expects (``packages.yaml``,
    ``compilers.yaml``, ``modules.yaml``, and ``config.yaml``).

    Attributes:
        name (str): Name of the site, used as the directory name for the
            generated configuration files.
        packages (Packages): Collection of package definitions, including
            externals, providers, and buildability flags.
        compilers (Compilers): Collection of compiler definitions and paths.
        modules (Modules): Module system configuration (Lmod or Tcl).
        config (Config): Global configuration options (e.g., build jobs).
    """

    def __init__(self, name):
        self.name = name
        self.packages = Packages()
        self.compilers = Compilers()
        self.modules = Modules()
        self.config = Config()

    def write(self, *, path: Path) -> None:
        """
        Write the site configuration to disk in Spack YAML format.

        This method generates a directory named after the site (``self.name``)
        under the given ``path`` and writes the component configuration files:
        ``packages.yaml``, ``compilers.yaml``, ``modules.yaml``, and
        ``config.yaml``.

        Args:
            path (Path): Base path where the site directory will be created.
                The site directory itself is named after ``self.name``.
        """
        site_dir = Path(path) / self.name
        site_dir.mkdir(parents=True, exist_ok=True)
        self.packages.write(path=site_dir / "packages.yaml", spack_format=True)
        self.compilers.write(path=site_dir / "compilers.yaml", spack_format=True)
        self.modules.write(path=site_dir / "modules.yaml", spack_format=True)
        self.config.write(path=site_dir / "config.yaml", spack_format=True)
