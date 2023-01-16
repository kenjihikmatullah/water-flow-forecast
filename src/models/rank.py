import json

from models.simulation_result import SimulationResult


class Rank:

    def __init__(self, actual_result: SimulationResult, simulation_result: SimulationResult, score: float):
        self.actual_result = actual_result
        self.simulation_result = simulation_result
        self.score = score

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
