from models.timing_type import TimingType
from scenario_data.madani_scenario_data import MadaniScenarioData


def get_data():
    """
    Scenario data where a leak in the early hours of the morning (3-4 AM) every week is simulated

    Sunday 3-4 AM, monday 3-4 AM, ..., saturday 3-4 AM.
    So, leak is simulated in 7 time windows

    #time-series
    """
    return MadaniScenarioData(
        output_dir='output/weekly_dawn/',
        number_of_pipes=104,
        initial_inp_file='input/its_weekly_dawn.inp',
        junction_ids=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95],
        timing_type=TimingType.TIME_SERIES,
        times=['00:00:00', '01:00:00', '02:00:00', '03:00:00', '04:00:00', '05:00:00', '06:00:00']
    )