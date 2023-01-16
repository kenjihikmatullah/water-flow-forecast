from models.leak_localization_record import LeakLocalizationRecord
from models.rank import Rank
from models.simulation_result import SimulationResult
from models.simulation_session import SimulationSession
from repository.leak_localization_repository import LeakLocalizationRepository
from utils.corr_coef_util import CorrCoefUtil


class CorrCoefLeakLocator:
    """
    Locate leakage using correlation coefficient formula
    """

    def __init__(
            self,
            actual_session_result_per_time: dict[str, SimulationSession],
            simulation_session_result_per_time: dict[str, SimulationSession],
            localization_session_id: str
    ):
        self.actual_session_result_per_time = actual_session_result_per_time
        self.simulation_session_result_per_time = simulation_session_result_per_time
        self.localization_session_id = localization_session_id

        self.corr_coeff_util = CorrCoefUtil()
        self.repository = LeakLocalizationRepository()

    def execute(self):
        num_correct = 0
        num_total = 0

        # Iterate through all actual leak cases
        for key in self.actual_session_result_per_time.keys():
            actual_results = self.actual_session_result_per_time.get(key).results
            for actual_result in actual_results:
                actual_leaking_junction_id = actual_result.leaking_junction_id
                predicted_leaking_junction_id = self.locate(actual_result,
                                                            simulation_session_id=self.simulation_session_result_per_time.get(
                                                                key).session_id)

                if actual_leaking_junction_id is not None:
                    print('ID of Actual Leaking Junction: ' + actual_leaking_junction_id)
                    print('ID of Predicted Leaking Junction: ' + predicted_leaking_junction_id)

                    num_total += 1
                    if actual_leaking_junction_id == predicted_leaking_junction_id:
                        num_correct += 1

        # print(f'Correct {num_correct}/{num_total} = {num_correct / num_total * 100}%')

    def locate(self, actual_result: SimulationResult, simulation_session_id: str) -> str:
        """
        Locate leak based on simulation data
        """
        prediction_of_leaking_junction_id = []

        # Get prediction on each DB time step
        for key in self.simulation_session_result_per_time.keys():
            ranking: list[Rank] = []

            simulation_results = self.simulation_session_result_per_time.get(key).results
            for simulation_result in simulation_results:
                if simulation_result.leaking_junction_id is None:
                    continue

                corr_coeff = self.corr_coeff_util.calculate(
                    actual_result=actual_result,
                    simulation_result=simulation_result
                )

                ranking.append(
                    Rank(actual_result=actual_result, simulation_result=simulation_result, score=corr_coeff)
                )

            """
            In correlation coefficient formula,
            the larger the coefficient value, the more similar
            """
            ranking.sort(key=lambda r: r.score, reverse=True)

            if len(ranking) == 0:
                return ''

            prediction = ranking[0].simulation_result
            print(ranking[0].to_json())
            prediction_of_leaking_junction_id.append(prediction.leaking_junction_id)

            time_step_mapping = {
                '01:00:00': 'MONDAY',
                '02:00:00': 'TUESDAY',
                '03:00:00': 'WEDNESDAY',
                '04:00:00': 'THURSDAY',
                '05:00:00': 'FRIDAY',
                '06:00:00': 'SATURDAY',
                '07:00:00': 'SUNDAY',
            }

            record = LeakLocalizationRecord(
                localization_session_id=self.localization_session_id,
                simulation_session_id=simulation_session_id,
                actual_leaking=actual_result.leaking_junction_id,
                time_step_of_prediction=time_step_mapping.get(prediction.time_step),
                prediction=prediction.leaking_junction_id,
                method='CORRELATION_COEFFICIENT'
            )

            self.repository.store(record)

        return max(set(prediction_of_leaking_junction_id), key=prediction_of_leaking_junction_id.count)
