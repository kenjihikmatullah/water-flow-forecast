import os
import shutil
import subprocess
from typing import TextIO

import input
from constant import INITIAL_INP_FILE, NUMBER_OF_PIPES, EPANET_JAR_FILE, CATEGORY_PIPE, \
    INITIAL_ROUGHNESS, ROUGHNESS_INTERVAL_PER_VARIANT, NUMBER_OF_ROUGHNESS_VARIANTS, \
    OUTPUT_ROUGHNESS_DIR, OUTPUT_ROUGHNESS_FILE


def _open_output_file() -> TextIO:
    if os.path.exists(OUTPUT_ROUGHNESS_DIR):
        shutil.rmtree(OUTPUT_ROUGHNESS_DIR)

    os.makedirs(OUTPUT_ROUGHNESS_DIR)

    return open(OUTPUT_ROUGHNESS_DIR + OUTPUT_ROUGHNESS_FILE, 'w')


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

    # Simulate all roughness variants on each pipe
    for pipe in range(1, NUMBER_OF_PIPES + 1):
        for roughness_variant in range(0, NUMBER_OF_ROUGHNESS_VARIANTS):
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

            opparams = [str(pipe), str(roughness)]
            sep = ","
            csv_record = sep.join(opparams + input.getdata(inp_file))
            output_file.write(csv_record + '\n')

    output_file.close()
    print('Finished')
