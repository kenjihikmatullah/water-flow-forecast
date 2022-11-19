from dataclasses import dataclass

from models.inp_metadata import InpMetadata
from utils.inp_metadata_creator import InpMetadataCreator


@dataclass
class ScenarioData:
    initial_inp_file: str
    output_dir: str

    initial_inp_metadata: InpMetadata = None

    def __post_init__(self):
        self.initial_inp_metadata = InpMetadataCreator().create(self.initial_inp_file)

    @property
    def junction_ids(self):
        return self.initial_inp_metadata.junction_ids

    @property
    def pipe_ids(self):
        return self.initial_inp_metadata.pipe_ids

    @property
    def time_steps(self):
        return self.initial_inp_metadata.time_steps
