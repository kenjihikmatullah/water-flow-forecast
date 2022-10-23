from result.madani.madani_result import MadaniResult

import numpy as np

class EuclideanDistanceUtil:

    def calculateBetweenMadaniResult(self, result_a: MadaniResult, result_b: MadaniResult) -> float:
        a = np.array(list(map(lambda p: p.flow, result_a.pipes)))
        b = np.array(list(map(lambda p: p.flow, result_b.pipes)))

        dist = np.linalg.norm(a - b)
        print("Euclidean distance: " + str(dist))

        return dist

    def calculate_based_on_delta_flow(self, result_a: MadaniResult, result_b: MadaniResult) -> float:
        a = np.array(list(map(lambda p: p.get_delta_flow(), result_a.pipes)))
        b = np.array(list(map(lambda p: p.get_delta_flow(), result_b.pipes)))

        dist = np.linalg.norm(a - b)
        print("Euclidean distance: " + str(dist))

        return dist
