from detection.ed_leak_detection import EdLeakDetection
from importer.madani.madani_maria_db_importer import MadaniMariaDbImporter

if __name__ == "__main__":

    madani_session_result = MadaniMariaDbImporter(table='simulation_results').do_import()
    andalus_session_result = MadaniMariaDbImporter(table='andalus_results').do_import()

    EdLeakDetection(madani_session_result, andalus_session_result.results[5]).execute()
