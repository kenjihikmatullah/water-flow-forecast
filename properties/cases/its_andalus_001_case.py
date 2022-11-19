from models.scenario_data import ScenarioData


def get_data():
    """
    Leak in the early hours of the morning (3-4 AM) every week is simulated

    Sunday 3-4 AM, monday 3-4 AM, ..., saturday 3-4 AM.
    So, leak is simulated in 7 time windows

    #time-series
    """
    return ScenarioData(
        initial_inp_file='input/its_weekly_dawn.inp',
        output_dir='output/weekly_dawn_andalus/'
    )