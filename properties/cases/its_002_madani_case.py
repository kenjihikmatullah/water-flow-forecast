from models.timing_type import TimingType
from scenario_data.madani_scenario_data import MadaniScenarioData


def get_data():
    """
    Leak in the early hours of the morning (3-4 AM) every week is simulated

    Sunday 3-4 AM, monday 3-4 AM, ..., saturday 3-4 AM.
    So, leak is simulated in 7 time windows

    #time-series
    """
    return MadaniScenarioData(
        initial_inp_file='input/its_weekly_dawn.inp',
        output_dir='output/weekly_dawn/'
    )