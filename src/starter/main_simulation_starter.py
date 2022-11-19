import os
from pathlib import Path

from properties.cases import its_andalus_001_case
from scenarios.andalus_scenario import AndalusScenario
from scenarios.scenario import Scenario


def setup():
    # Get current directory
    current_dir = os.path.realpath(__file__)

    # Move up to project's root directory
    root_dir = Path(current_dir).parents[2]
    os.chdir(root_dir)


if __name__ == "__main__":
    setup()

    # metadata = InpMetadataCreatorImpl().create('input/its_weekly_dawn.inp')
    # MariaDbClient().create_table(metadata.pipe_ids)

    scenarios: list[Scenario] = [
        # MadaniScenario(data=its_002_madani_case.get_data()),
        AndalusScenario(data=its_andalus_001_case.get_data()),
    ]

    for scenario in scenarios:
        scenario.run()
