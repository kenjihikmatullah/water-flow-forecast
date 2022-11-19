from dataclasses import dataclass

from models.junction import Junction
from models.pipe import Pipe


@dataclass
class SimulationResult:
    custom_inp_file: str

    time_step: str
    leaking_junction_id: str | None
    leaking_junction_emit: float | None
    leaking_junction_leak: float | None

    junctions: list[Junction]
    pipes: list[Pipe]

    @property
    def pipe_ids(self):
        return list(map(lambda x: x.id, self.pipes))
