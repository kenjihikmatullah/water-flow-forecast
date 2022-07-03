import os

from models.scenario import Scenario
from scenarios.madani_scenario import MadaniScenario
from utils import output
from pathlib import Path
from properties.scenario_data import its_madani_scenario_data


def setup():
    # Get current directory
    current_dir = os.path.realpath(__file__)

    # Move up to project's root directory
    root_dir = Path(current_dir).parents[2]
    os.chdir(root_dir)


if __name__ == "__main__":
    setup()
    output.prepare_dir()

    scenarios: list[Scenario] = [
        MadaniScenario(data=its_madani_scenario_data.get_data())
    ]

    for scenario in scenarios:
        scenario.run()

