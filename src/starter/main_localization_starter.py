from locator.corr_coef_leak_locator import CorrCoefLeakLocator
from locator.ed_leak_locator import EdLeakLocator
from repository.leak_localization_repository import LeakLocalizationRepository
from repository.simulation_result_repository import SimulationResultRepository
from models.simulation_session import SimulationSession


def add_noise(session_per_time: dict[str, SimulationSession], percentage: int):
    for key in session_per_time.keys():
        results = session_per_time.get(key).results
        for result in results:
            for pipe in result.pipes:
                noise = percentage/100 * pipe.flow

                pipe.flow = pipe.flow + noise
                pipe.delta_flow = pipe.delta_flow + noise

if __name__ == "__main__":
    for n in [5, -5, 10, -10, 30, -30]:
        simulation_session_per_time: dict[str, SimulationSession] = {}
        actual_session_per_time: dict[str, SimulationSession] = {}

        for i in range(1, 8):
            time = f"0{i}:00:00"
            simulation_session_per_time[time] = SimulationResultRepository().get_simulation_results(
                session_id='20-NOV-2022', time_step=time)
            actual_session_per_time[time] = SimulationResultRepository().get_simulation_results(
                session_id='20-NOV-2022', time_step=time)

        add_noise(actual_session_per_time, n)
        localization_session_id = f'21-NOV-2022_EUCL_DIST_NOISY_{n}_PERCENT'

        EdLeakLocator(
            actual_session_result_per_time=actual_session_per_time,
            simulation_session_result_per_time=simulation_session_per_time,
            localization_session_id=localization_session_id
        ).execute()

        LeakLocalizationRepository().export_db_to_csv(
            localization_session_id=localization_session_id,
            filename=f'{localization_session_id}.csv'
        )

