from dataclasses import dataclass, field

from models.junction import Junction
from models.pipe import Pipe
from models.timing_type import TimingType


@dataclass
class InpMetadata:
    junctions: list[Junction]
    pipes: list[Pipe]
    times: list[str] = field(default_factory=list)

    @property
    def junction_ids(self) -> list[str]:
        return sorted(list(map(lambda j: j.id, self.junctions)))

    @property
    def pipe_ids(self) -> list[str]:
        return sorted(list(map(lambda j: j.id, self.pipes)))

    @property
    def timing_type(self) -> TimingType:
        if len(self.times) > 1:
            return TimingType.TIME_SERIES

        else:
            return TimingType.SINGLE_PERIOD
