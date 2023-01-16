import numpy as np

from models.simulation_result import SimulationResult


class CorrCoefUtil:

    def calculate(self, actual_result: SimulationResult, simulation_result: SimulationResult) -> float:
        actual = list(map(lambda p: p.get_delta_flow(), actual_result.pipes))
        simulation = list(map(lambda p: p.get_delta_flow(), simulation_result.pipes))

        matrix = np.corrcoef(actual, simulation)
        coefficient = abs(matrix[0][1])
        print('Coefficient: ' + str(coefficient))

        return coefficient
