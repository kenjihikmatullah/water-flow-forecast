import os
import shutil
import subprocess
from typing import TextIO

import constant
import input
from constant import OUTPUT_ROUGHNESS_DIR, OUTPUT_ROUGHNESS_FILE

rough_positions = []
for pos in range(1, 59):
    rough_positions.append(str(pos))


def _prepare_dir():
    if os.path.exists(OUTPUT_ROUGHNESS_DIR):
        shutil.rmtree(OUTPUT_ROUGHNESS_DIR)

    os.makedirs(OUTPUT_ROUGHNESS_DIR)


def _open_file() -> TextIO:
    _prepare_dir()
    return open(OUTPUT_ROUGHNESS_DIR + OUTPUT_ROUGHNESS_FILE, 'w')


def _change_inner(inputfile, outputfile, category, idname, pos, val):
    try:
        fileobj = open(inputfile, 'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        print('Input file open error')
    try:
        fileout = open(outputfile, 'w')
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
                    ss[pos] = val
                    sep = "    "
                    lines[i] = sep.join(ss)

        if (ss[0].find(category) > -1):
            incategory = True
        fileout.write(lines[i])

    fileout.close()


def _change(pp, rp, r):
    infilename = constant.INPUT_FILE
    finaloutputfile = constant.OUTPUT_ROUGHNESS_DIR + 'tmp-PP-' + pp + '-r-' + str(r) + '.inp'
    _change_inner(infilename, finaloutputfile, 'PIPES', pp, 5, rp + ' ')
    print(f'Created: {finaloutputfile}')
    return finaloutputfile


def simulate():
    database_file = _open_file()

    for r in range(0, constant.STEP_COUNT + 1):
        for pp in rough_positions:
            rp = str(constant.INITIAL_ROUGHNESS + constant.STEP * r)
            finaloutputfile = _change(pp, rp, r)

            subprocess.call(["java", "-cp", constant.EPANET_JAR_FILE, "org.addition.epanet.EPATool",
                             finaloutputfile])

            opparams = [pp, rp]
            sep = ","
            csv_record = sep.join(opparams + input.getdata(finaloutputfile))
            database_file.write(csv_record + '\n')

    database_file.close()
    print('Finished')
