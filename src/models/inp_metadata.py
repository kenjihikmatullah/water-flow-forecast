from dataclasses import dataclass, field

from models.junction import Junction
from models.timing_type import TimingType


@dataclass
class InpMetadata:
    junctions: list[Junction]
    pipe_ids: list[str]
    timing_type: TimingType = TimingType.SINGLE_PERIOD
    times: list[str] = field(default_factory=list)
