from abc import ABC, abstractmethod
from pathlib import Path


class AbstractSiteConfig(ABC):
    @abstractmethod
    def write(self, *, path: Path, spack_format: bool = True) -> None:
        pass
