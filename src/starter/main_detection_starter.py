from detection.ed_leak_detection_v2 import EdLeakDetectionV2
from importer.madani.madani_maria_db_importer import MadaniMariaDbImporter
from repository.leak_localization_repository import LeakLocalizationRepository
from result.madani.madani_session_result import MadaniSessionResult

if __name__ == "__main__":
    session_result_per_time: dict[str, MadaniSessionResult] = {}
    for i in range(7):
        time = f"0{i+1}:00:00"
        importer = MadaniMariaDbImporter(table=f"andalus_results_time_{i+1}")

        session_result_per_time[time] = importer.do_import()

    EdLeakDetectionV2(session_result_per_time).execute()

    LeakLocalizationRepository().export_db_to_csv()

