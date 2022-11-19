from models.simulation_result import SimulationResult
from models.simulation_session import SimulationSession


class LeakLocator:

    def __init__(self, madani_session_result: SimulationSession, andalus_result: SimulationResult):
        self._madani_session_result = madani_session_result
        self._andalus_result = andalus_result

    def execute(self):
        pass
