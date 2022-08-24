from dataclasses import dataclass

from models.junction import Junction
from models.pipe import Pipe


@dataclass
class MadaniResult:
    custom_inp_file: str

    time_step: str
    adjusted_junction_id: str | None
    adjusted_junction_emit: float | None
    adjusted_junction_leak: float | None

    junctions: list[Junction]
    pipes: list[Pipe]

    @property
    def pipe_ids(self):
        return list(map(lambda x: x.id, self.pipes))
