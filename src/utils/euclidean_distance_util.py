from result.madani.madani_result import MadaniResult

import numpy as np

class EuclideanDistanceUtil:

    def calculateBetweenMadaniResult(self, result_a: MadaniResult, result_b: MadaniResult) -> float:
        a = np.array(list(map(lambda p: p.flow, result_a.pipes)))
        b = np.array(list(map(lambda p: p.flow, result_b.pipes)))

        dist = np.linalg.norm(a - b)
        print("Euclidean distance: " + str(dist))

        return dist
