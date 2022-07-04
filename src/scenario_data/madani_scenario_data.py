from dataclasses import dataclass, field

from models.timing_type import TimingType


@dataclass
class MadaniScenarioData:
    output_dir: str
    number_of_pipes: int
    initial_inp_file: str
    junction_ids: list[int]

    timing_type: TimingType = TimingType.SINGLE_PERIOD
    times: list[str] = field(default_factory=list)
