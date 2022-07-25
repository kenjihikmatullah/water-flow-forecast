from abc import abstractmethod

from models.inp_metadata import InpMetadata


class InpMetadataCreator:

    @abstractmethod
    def create(self, path: str) -> InpMetadata:
        pass
