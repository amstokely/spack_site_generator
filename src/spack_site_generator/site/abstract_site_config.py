from abc import ABC, abstractmethod


class AbstractSiteConfig(ABC):
    @abstractmethod
    def write(
            self,
            *,
            filename: str,
            spack_format: bool = True
    ) -> None:
        pass
