from locator.ed_leak_locator import EdLeakLocator
from repository.leak_localization_repository import LeakLocalizationRepository
from repository.simulation_result_repository import SimulationResultRepository
from models.simulation_session import SimulationSession

if __name__ == "__main__":
    session_result_per_time: dict[str, SimulationSession] = {}

    for i in range(1, 8):
        time = f"0{i}:00:00"
        session_result_per_time[time] = SimulationResultRepository().get_simulation_cases(session_id='2022-11-19 08:30:00', time_step=time)

    EdLeakLocator(
        simulation_session_result_per_time=session_result_per_time,
        actual_session_result_per_time=session_result_per_time
    ).execute()

    LeakLocalizationRepository().export_db_to_csv()

