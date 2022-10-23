import json

from result.madani.madani_result import MadaniResult


class EdRank:

    def __init__(self, result_to_compare: MadaniResult, result: MadaniResult, score: float):
        self.result_to_compare = result_to_compare
        self.result = result
        self.score = score

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)