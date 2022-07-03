import os
import shutil
import subprocess
from typing import TextIO

from properties import constant
from utils import emit_util, inp_util
from properties.constant import NUMBER_OF_PIPES, EPANET_JAR_FILE, CATEGORY_EMITTERS, \
    OUTPUT_EMIT_DIR, OUTPUT_EMIT_FILE, JUNCTION_IDS
from utils.out_util import get_flows, get_pressures, get_heads, get_demands




def simulate():
    output_file = _open_output_file()

    try:
        _write_header(output_file)

        # Write first row: no leak
        write_row(output_file, constant.INITIAL_INP_FILE, '-', '-')



        print('Finished')

    finally:
        output_file.close()
