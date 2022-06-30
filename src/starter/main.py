import output
import roughness
import emit
import os
import emit_util
from pathlib import Path

def setup():
    # Get current directory
    current_dir = os.path.realpath(__file__)

    # Move up to project's root directory
    root_dir = Path(current_dir).parents[2]
    os.chdir(root_dir)


if __name__ == "__main__":
    setup()
    output.prepare_dir()

    # roughness.simulate()

    # emit.simulate()

    emit_util.get_proper_emit(1, 0.5)
