from dataclasses import dataclass, field

from models.junction import Junction
from models.simulation_result import SimulationResult


@dataclass
class SimulationSession:
    session_id: str = None
    results: list[SimulationResult] = field(default_factory=list)

    # TODO: Add FK to version of real data from sensors which this simulation is based on

    def get_junction_result_when_no_leak(self, junction_id, time_step) -> Junction | None:
        """
        Get actual demand of a junction at certain time step
        """
        for result in self.results:
            if result.leaking_junction_id is None and result.time_step == time_step:
                for junction in result.junctions:
                    if junction.id == junction_id:
                        return junction

        return None
