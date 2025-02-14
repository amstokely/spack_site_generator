from pathlib import Path

from spack_site_generator.site import Compilers
from spack_site_generator.site import Modules
from spack_site_generator.site import Packages
from spack_site_generator.site import Config


class Site(object):
    def __init__(self, name):
        self.name = name
        self.packages = Packages()
        self.compilers = Compilers()
        self.modules = Modules()
        self.config = Config()

    def write(self, *, path: Path) -> None:
        site_dir = Path(path) / self.name
        site_dir.mkdir(parents=True, exist_ok=True)
        self.packages.write(path=site_dir / "packages.yaml", spack_format=True)
        self.compilers.write(path=site_dir / "compilers.yaml", spack_format=True)
        self.modules.write(path=site_dir / "modules.yaml", spack_format=True)
        self.config.write(path=site_dir / "config.yaml", spack_format=True)
