import os
from pathlib import Path

from properties.cases import its_andalus_001_case
from repository.simulation_result_repository import SimulationResultRepository
from simulator.simulator import Simulator


def setup():
    # Get current directory
    current_dir = os.path.realpath(__file__)

    # Move up to project's root directory
    root_dir = Path(current_dir).parents[2]
    os.chdir(root_dir)


if __name__ == "__main__":
    setup()

    scenario = Simulator(data=its_andalus_001_case.get_data())
    scenario.run()
