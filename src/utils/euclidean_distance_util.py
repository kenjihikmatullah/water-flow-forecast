from models.simulation_result import SimulationResult

import numpy as np

class EuclideanDistanceUtil:

    def calculate_based_on_delta_flow(self, actual_result: SimulationResult, simulation_result: SimulationResult) -> float:
        a = np.array(list(map(lambda p: p.get_delta_flow(), simulation_result.pipes)))
        b = np.array(list(map(lambda p: p.get_delta_flow(), actual_result.pipes)))

        dist = np.linalg.norm(a - b)
        print("Euclidean distance: " + str(dist))

        return dist
