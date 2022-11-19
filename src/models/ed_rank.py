import json

from models.simulation_result import SimulationResult


class EdRank:

    def __init__(self, simulation_case: SimulationResult, actual_case: SimulationResult, score: float):
        self.simulation_case = simulation_case
        self.actual_case = actual_case
        self.score = score

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
