from models.simulation_result import SimulationResult

import numpy as np

class EuclideanDistanceUtil:

    def calculateBetweenMadaniResult(self, result_a: SimulationResult, result_b: SimulationResult) -> float:
        a = np.array(list(map(lambda p: p.flow, result_a.pipes)))
        b = np.array(list(map(lambda p: p.flow, result_b.pipes)))

        dist = np.linalg.norm(a - b)
        print("Euclidean distance: " + str(dist))

        return dist

    def calculate_based_on_delta_flow(self, simulation_case: SimulationResult, actual_case: SimulationResult) -> float:
        a = np.array(list(map(lambda p: p.get_delta_flow(), simulation_case.pipes)))
        b = np.array(list(map(lambda p: p.get_delta_flow(), actual_case.pipes)))

        dist = np.linalg.norm(a - b)
        print("Euclidean distance: " + str(dist))

        return dist
