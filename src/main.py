import output
import roughness
import emit
import os

if __name__ == "__main__":
    os.chdir('D:\\Practice\\water-flow-forecast')  # TODO: Improve elegance

    output.prepare_dir()

    # roughness.simulate()

    emit.simulate()
