import os
import shutil
import subprocess
from typing import TextIO

import simulation_input
from constant import NUMBER_OF_PIPES, NUMBER_OF_JUNCTIONS, EPANET_JAR_FILE, CATEGORY_EMITTERS, \
    INITIAL_EMIT, EMIT_INTERVAL_PER_VARIANT, NUMBER_OF_EMIT_VARIANTS, \
    OUTPUT_EMIT_DIR, OUTPUT_EMIT_FILE
from simulation_output import get_flows, get_pressures, get_heads, get_demands

INP_EMITTERS_COEFFICIENT_COLUMN_INDEX = 1


def _open_output_file() -> TextIO:
    if os.path.exists(OUTPUT_EMIT_DIR):
        shutil.rmtree(OUTPUT_EMIT_DIR)

    os.makedirs(OUTPUT_EMIT_DIR)
    os.makedirs(OUTPUT_EMIT_DIR + 'temp/')

    return open(OUTPUT_EMIT_DIR + OUTPUT_EMIT_FILE, 'w')


def _write_header(output_file):
    header: list[str] = ['Adjusted Junction', 'Emitter Coeff.']

    for pipe in range(1, NUMBER_OF_PIPES + 1):
        header.append(f'P{pipe} Flow (LPS)')

    for junction in range(1, NUMBER_OF_JUNCTIONS + 1):
        header.append(f'J{junction} Pressure (m)')

    for junction in range(1, NUMBER_OF_JUNCTIONS + 1):
        header.append(f'J{junction} Head (m)')

    for junction in range(1, NUMBER_OF_JUNCTIONS + 1):
        header.append(f'J{junction} Demand (LPS)')

    output_file.write(",".join(header) + '\n')


def _generate_inp_file(junction_id: int, emit: int):
    return simulation_input.generate_custom_inp_file(
        target_file_path=f'{OUTPUT_EMIT_DIR}temp/J{junction_id}-ec{emit}.inp',
        customized_category=CATEGORY_EMITTERS,
        customized_component_id=str(junction_id),
        customized_column_index=INP_EMITTERS_COEFFICIENT_COLUMN_INDEX,
        custom_value=str(emit)
    )


def simulate():
    output_file = _open_output_file()

    try:
        _write_header(output_file)

        # Simulate all emitter coefficient variants on each pipe
        for junction_id in range(1, NUMBER_OF_JUNCTIONS + 1):
            for emit_variant in range(0, NUMBER_OF_EMIT_VARIANTS + 1):
                # Count emitter coefficient
                emit = INITIAL_EMIT + EMIT_INTERVAL_PER_VARIANT * emit_variant

                # Generate inp file
                inp_file = _generate_inp_file(
                    junction_id=junction_id,
                    emit=emit
                )

                # Run simulation
                subprocess.call(["java", "-cp", EPANET_JAR_FILE, "org.addition.epanet.EPATool",
                                 inp_file])

                # Write down the result
                csv_record = ",".join([
                    str(junction_id),
                    str(emit),
                    *get_flows(inp_file),
                    *get_pressures(inp_file),
                    *get_heads(inp_file),
                    *get_demands(inp_file)
                ])
                output_file.write(csv_record + '\n')

        print('Finished')

    finally:
        output_file.close()
