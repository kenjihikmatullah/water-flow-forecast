from models.ed_rank import EdRank
from models.leak_localization_record import LeakLocalizationRecord
from repository.leak_localization_repository import LeakLocalizationRepository
from result.madani.madani_result import MadaniResult
from result.madani.madani_session_result import MadaniSessionResult
from utils.euclidean_distance_util import EuclideanDistanceUtil


class EdLeakDetectionV2:

    def __init__(self, session_result_per_time: dict[str, MadaniSessionResult]):
        self.session_result_per_time = session_result_per_time
        self.ed_util = EuclideanDistanceUtil()

    def execute(self):
        num_correct = 0
        num_total = 0

        for key in self.session_result_per_time.keys():

            for result in self.session_result_per_time.get(key).results:
                if str(result.adjusted_junction_id) not in ['1', '2', '3', '4']:
                    continue

                actual_leaking_junction_id = result.adjusted_junction_id
                predicted_leaking_junction_id = self.detect_leak(result)

                if actual_leaking_junction_id is not None:
                    print('ID of Actual Leaking Junction: ' + actual_leaking_junction_id)
                    print('ID of Predicted Leaking Junction: ' + predicted_leaking_junction_id)

                    num_total += 1
                    if actual_leaking_junction_id == predicted_leaking_junction_id:
                        num_correct += 1

        print(f'Correct {num_correct}/{num_total} = {num_correct / num_total * 100}%')

    def detect_leak(self, result: MadaniResult) -> str:
        guess_of_leaky_junction_id = []

        for key in self.session_result_per_time.keys():
            ranking: list[EdRank] = []

            for result_to_compare in self.session_result_per_time.get(key).results:
                if result_to_compare.adjusted_junction_id is None:
                    continue

                score = self.ed_util.calculate_based_on_delta_flow(result, result_to_compare)

                ranking.append(
                    EdRank(result=result, result_to_compare=result_to_compare, score=score)
                )

            ranking.sort(key=lambda r: r.score)

            # print(list(
            #     map(
            #         lambda r: r.toJSON(),
            #         ranking
            #     )
            # )[:3])
            # print('rank: ' + str(list(
            #     map(
            #         lambda r: r.result_to_compare.adjusted_junction_id,
            #         ranking
            #     )
            # )[:3]))

            prediction = ranking[0].result_to_compare.adjusted_junction_id
            guess_of_leaky_junction_id.append(prediction)


            time_step_mapping = {
                '01:00:00': 'MONDAY',
                '02:00:00': 'TUESDAY',
                '03:00:00': 'WEDNESDAY',
                '04:00:00': 'THURSDAY',
                '05:00:00': 'FRIDAY',
                '06:00:00': 'SATURDAY',
                '07:00:00': 'SUNDAY',
            }

            LeakLocalizationRepository().store(
                LeakLocalizationRecord(
                    actual_leaking=result.adjusted_junction_id,
                    time_step_of_prediction=time_step_mapping.get(result.time_step),
                    prediction=prediction
                )
            )

        # print('all guess of leaky junction id' + str(guess_of_leaky_junction_id))

        return max(set(guess_of_leaky_junction_id), key=guess_of_leaky_junction_id.count)
