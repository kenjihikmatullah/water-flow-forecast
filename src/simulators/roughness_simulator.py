import os
import shutil
import subprocess
from typing import TextIO

from properties.constant import NUMBER_OF_PIPES, NUMBER_OF_JUNCTIONS, EPANET_JAR_FILE, CATEGORY_PIPES, \
    INITIAL_ROUGHNESS, ROUGHNESS_INTERVAL_PER_VARIANT, NUMBER_OF_ROUGHNESS_VARIANTS, \
    OUTPUT_ROUGHNESS_DIR, OUTPUT_ROUGHNESS_FILE
from utils.out_util import get_flows, get_pressures, get_heads, get_demands

INP_PIPE_ROUGHNESS_COLUMN_INDEX = 5


def _open_output_file() -> TextIO:
    if os.path.exists(OUTPUT_ROUGHNESS_DIR):
        shutil.rmtree(OUTPUT_ROUGHNESS_DIR)

    os.makedirs(OUTPUT_ROUGHNESS_DIR)
    os.makedirs(OUTPUT_ROUGHNESS_DIR + 'temp/')

    return open(OUTPUT_ROUGHNESS_DIR + OUTPUT_ROUGHNESS_FILE, 'w')


def _write_header(output_file):
    header: list[str] = ['Adjusted Pipe', 'Roughness']

    for pipe in range(1, NUMBER_OF_PIPES + 1):
        header.append(f'P{pipe} Flow (LPS)')

    for junction in range(1, NUMBER_OF_JUNCTIONS + 1):
        header.append(f'J{junction} Pressure (m)')

    for junction in range(1, NUMBER_OF_JUNCTIONS + 1):
        header.append(f'J{junction} Head (m)')

    for junction in range(1, NUMBER_OF_JUNCTIONS + 1):
        header.append(f'J{junction} Demand (LPS)')

    output_file.write(",".join(header) + '\n')


def _generate_inp_file(pipe: int, roughness: int):
    return simulation_input.generate_custom_inp_file(
        target_file_path=f'{OUTPUT_ROUGHNESS_DIR}temp/P{pipe}-R{roughness}.inp',
        customized_category=CATEGORY_PIPES,
        customized_component_id=str(pipe),
        customized_column_index=INP_PIPE_ROUGHNESS_COLUMN_INDEX,
        custom_value=str(roughness)
    )


def simulate():
    output_file = _open_output_file()

    try:
        _write_header(output_file)

        # Simulate all roughness variants on each pipe
        for pipe in range(1, NUMBER_OF_PIPES + 1):
            for roughness_variant in range(0, NUMBER_OF_ROUGHNESS_VARIANTS + 1):
                # Count roughness
                roughness = INITIAL_ROUGHNESS + ROUGHNESS_INTERVAL_PER_VARIANT * roughness_variant

                # Generate inp file
                inp_file = _generate_inp_file(
                    pipe=pipe,
                    roughness=roughness
                )

                # Run simulation
                subprocess.call(["java", "-cp", EPANET_JAR_FILE, "org.addition.epanet.EPATool",
                                 inp_file])

                # Write down the result
                csv_record = ",".join([
                    str(pipe),
                    str(roughness),
                    *get_flows(inp_file),
                    *get_pressures(inp_file),
                    *get_heads(inp_file),
                    *get_demands(inp_file)
                ])
                output_file.write(csv_record + '\n')

        print('Finished')

    finally:
        output_file.close()
