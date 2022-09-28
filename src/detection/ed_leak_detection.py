import json

from detection.leak_detection import LeakDetection
from models.ed_rank import EdRank
from utils.euclidean_distance_util import EuclideanDistanceUtil


class EdLeakDetection(LeakDetection):
    """
    Detect leak by calculating euclidean distance (alias ed) between simulation results
    of madani and andalus scenario
    """

    ed_util = EuclideanDistanceUtil()

    def execute(self):
        ranking: list[EdRank] = []

        for madani_result in self._madani_session_result.results:
            if madani_result.time_step != self._andalus_result.time_step:
                continue

            print('Calculating euclidean distance...')
            score = self.ed_util.calculateBetweenMadaniResult(madani_result, self._andalus_result)

            ranking.append(
                EdRank(madani_result, self._andalus_result, score)
            )

        ranking.sort(key=lambda r: r.score)

        print(list(
            map(
                lambda r: r.toJSON(),
                ranking
            )
        )[:5])
