from result.madani.madani_result import MadaniResult
from result.madani.madani_session_result import MadaniSessionResult


class LeakDetection:

    def __init__(self, madani_session_result: MadaniSessionResult, andalus_result: MadaniResult):
        self._madani_session_result = madani_session_result
        self._andalus_result = andalus_result

    def execute(self):
        pass
