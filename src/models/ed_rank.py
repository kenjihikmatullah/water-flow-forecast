import json

from result.madani.madani_result import MadaniResult


class EdRank:

    def __init__(self, simulation_case: MadaniResult, actual_case: MadaniResult, score: float):
        self.simulation_case = simulation_case
        self.actual_case = actual_case
        self.score = score

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)