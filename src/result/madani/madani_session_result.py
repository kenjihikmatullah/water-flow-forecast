from dataclasses import dataclass, field

from result.madani.madani_result import MadaniResult


@dataclass
class MadaniSessionResult:
    results: list[MadaniResult] = field(default_factory=list)

    # TODO: Add FK to version of real data from sensors which this simulation is based on
