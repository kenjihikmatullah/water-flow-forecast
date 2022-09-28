import json

from result.madani.madani_result import MadaniResult


class EdRank:

    def __init__(self, madani_result: MadaniResult, andalus_result: MadaniResult, score: float):
        self.madani_result = madani_result
        self.andalus_result = andalus_result
        self.score = score

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)