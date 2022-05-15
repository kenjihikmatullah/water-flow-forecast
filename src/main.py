import output
import roughness

if __name__ == "__main__":
    output.prepare_dir()

    roughness.simulate()

    # TODO: Simulate emitter coefficient
