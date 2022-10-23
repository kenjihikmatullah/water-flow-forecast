import os
from pathlib import Path

from properties.cases import its_andalus_001_case
from visual.plt_mnf_visual import PltMnfVisual

if __name__ == "__main__":
    # Get current directory
    current_dir = os.path.realpath(__file__)

    # Move up to project's root directory
    root_dir = Path(current_dir).parents[2]
    os.chdir(root_dir)

    data = its_andalus_001_case.get_data()
    PltMnfVisual(data).visualize()
