from scenario_data.madani_scenario_data import MadaniScenarioData


def get_data():
    """
    Leak in single period (snapshot) is simulated
    """
    return MadaniScenarioData(
        initial_inp_file='input/its_water_distribution.inp',
        output_dir='output/emit/'
    )
