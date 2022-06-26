import output
import roughness
import emit
import os
import emit_util

if __name__ == "__main__":
    os.chdir('D:\\Practice\\water-flow-forecast')  # TODO: Improve elegance

    output.prepare_dir()

    # roughness.simulate()

    emit.simulate()

    # emit_util.get_proper_emit(1, 0.5)
