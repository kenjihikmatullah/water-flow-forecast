import os
import shutil
import subprocess
from typing import TextIO

from constant import INITIAL_INP_FILE, NUMBER_OF_PIPES, NUMBER_OF_JUNCTIONS, EPANET_JAR_FILE, CATEGORY_PIPE, \
    INITIAL_ROUGHNESS, ROUGHNESS_INTERVAL_PER_VARIANT, NUMBER_OF_ROUGHNESS_VARIANTS, \
    OUTPUT_ROUGHNESS_DIR, OUTPUT_ROUGHNESS_FILE
from simulation import get_flows, get_pressures, get_heads, get_demands


def _open_output_file() -> TextIO:
    if os.path.exists(OUTPUT_ROUGHNESS_DIR):
        shutil.rmtree(OUTPUT_ROUGHNESS_DIR)

    os.makedirs(OUTPUT_ROUGHNESS_DIR)

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


def _generate_inp_file(pipe: int, roughness_variant: int, roughness: int):
    target_inp_file = f'{OUTPUT_ROUGHNESS_DIR}tmp-PP-{pipe}-r-{roughness_variant}.inp'
    idname = pipe
    pos = 5

    try:
        fileobj = open(INITIAL_INP_FILE, 'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        print('Input file open error')
    try:
        fileout = open(target_inp_file, 'w')
    except:
        print('Output file open error ')

    incategory = False
    nl = len(lines)
    for i in range(0, nl):
        sss = lines[i].split(' ')
        ss = list(filter(lambda x: x != '', sss))

        if (incategory):
            if (len(ss) == 1):
                incategory = False
            else:
                if ((ss[0] == idname) or (idname == '*' and ss[0][0] != ';')):
                    ss[pos] = roughness
                    sep = "    "
                    lines[i] = sep.join(ss)

        if (ss[0].find(CATEGORY_PIPE) > -1):
            incategory = True
        fileout.write(lines[i])

    fileout.close()
    print(f'Created: {target_inp_file}')
    return target_inp_file


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
                    roughness_variant=roughness_variant,
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
