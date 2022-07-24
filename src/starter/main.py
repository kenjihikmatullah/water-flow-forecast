import os

from scenarios.scenario import Scenario
from scenarios.madani_scenario import MadaniScenario
from pathlib import Path
from properties.cases import its_001_madani_case, its_002_madani_case


def setup():
    # Get current directory
    current_dir = os.path.realpath(__file__)

    # Move up to project's root directory
    root_dir = Path(current_dir).parents[2]
    os.chdir(root_dir)


if __name__ == "__main__":
    setup()

    scenarios: list[Scenario] = [
        MadaniScenario(data=its_002_madani_case.get_data()),
    ]

    for scenario in scenarios:
        scenario.run()
