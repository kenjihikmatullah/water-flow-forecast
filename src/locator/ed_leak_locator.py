from models.ed_rank import EdRank
from models.leak_localization_record import LeakLocalizationRecord
from repository.leak_localization_repository import LeakLocalizationRepository
from models.simulation_result import SimulationResult
from models.simulation_session import SimulationSession
from utils.euclidean_distance_util import EuclideanDistanceUtil


class EdLeakLocator:

    def __init__(
            self,
            simulation_session_result_per_time: dict[str, SimulationSession],
            actual_session_result_per_time: dict[str, SimulationSession]
    ):
        self.simulation_session_result_per_time = simulation_session_result_per_time
        self.actual_session_result_per_time = actual_session_result_per_time
        self.ed_util = EuclideanDistanceUtil()
        self.repository = LeakLocalizationRepository()

    def execute(self):
        num_correct = 0
        num_total = 0

        for key in self.simulation_session_result_per_time.keys():
            for simulation_result in self.simulation_session_result_per_time.get(key).results:

                actual_leaking_junction_id = simulation_result.leaking_junction_id
                predicted_leaking_junction_id = self.detect_leak(simulation_result,
                                                                 session_id=self.simulation_session_result_per_time.get(
                                                                     key).session_id)

                if actual_leaking_junction_id is not None:
                    print('ID of Actual Leaking Junction: ' + actual_leaking_junction_id)
                    print('ID of Predicted Leaking Junction: ' + predicted_leaking_junction_id)

                    num_total += 1
                    if actual_leaking_junction_id == predicted_leaking_junction_id:
                        num_correct += 1

        # print(f'Correct {num_correct}/{num_total} = {num_correct / num_total * 100}%')

    def detect_leak(self, simulation_result: SimulationResult, session_id: str) -> str:
        guess_of_leaking_junction_id = []

        print(self.actual_session_result_per_time)

        for key in self.actual_session_result_per_time.keys():
            ranking: list[EdRank] = []

            for actual_result in self.actual_session_result_per_time.get(key).results:
                if actual_result.leaking_junction_id is None:
                    continue

                score = self.ed_util.calculate_based_on_delta_flow(actual_case=actual_result,
                                                                   simulation_case=simulation_result)

                ranking.append(
                    EdRank(actual_case=actual_result, simulation_case=simulation_result, score=score)
                )

            ranking.sort(key=lambda r: r.score)

            if len(ranking) == 0:
                return ''

            prediction = ranking[0].simulation_case.leaking_junction_id
            guess_of_leaking_junction_id.append(prediction)

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
                session_id=session_id,
                actual_leaking=simulation_result.leaking_junction_id,
                time_step_of_prediction=simulation_result.time_step,
                prediction=prediction
            )

            self.repository.store(record)

        return max(set(guess_of_leaking_junction_id), key=guess_of_leaking_junction_id.count)
