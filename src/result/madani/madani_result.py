from dataclasses import dataclass

from models.junction import Junction
from models.pipe import Pipe


@dataclass
class MadaniResult:
    custom_inp_file: str

    time_step: str
    adjusted_junction_id: str | None
    emit: float | None

    junctions: list[Junction]
    pipes: list[Pipe]
