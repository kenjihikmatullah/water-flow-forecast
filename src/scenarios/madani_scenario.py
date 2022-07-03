from models.scenario import Scenario
import os
import shutil
import subprocess
from typing import TextIO

from properties import constant
from utils import emit_util, inp_util
from properties.constant import NUMBER_OF_PIPES, EPANET_JAR_FILE, CATEGORY_EMITTERS, \
    OUTPUT_EMIT_DIR, OUTPUT_EMIT_FILE, JUNCTION_IDS
from utils.out_util import get_flows, get_pressures, get_heads, get_demands


class MadaniScenario(Scenario):
    """
    Simulate leak by setting emitter coeff. to each junction.
    This scenario aims to get WDS state when a leak occurs.
    """

    INP_EMITTERS_COEFFICIENT_COLUMN_INDEX = 1

    output_file: TextIO

    def _open_output_file(self):
        if os.path.exists(OUTPUT_EMIT_DIR):
            shutil.rmtree(OUTPUT_EMIT_DIR)

        os.makedirs(OUTPUT_EMIT_DIR)
        os.makedirs(OUTPUT_EMIT_DIR + 'temp/')
        os.makedirs(OUTPUT_EMIT_DIR + 'temp-hill-climbing/')

        self.output_file = open(OUTPUT_EMIT_DIR + OUTPUT_EMIT_FILE, 'w')

    def _write_header(self):
        header: list[str] = ['Adjusted Junction', 'Emitter Coeff.']

        for pipe in range(1, NUMBER_OF_PIPES + 1):
            header.append(f'P{pipe} Flow (LPS)')

        header.append('...what is this?')

        for junction in JUNCTION_IDS:
            header.append(f'J{junction} Pressure (m)')

        for junction in JUNCTION_IDS:
            header.append(f'J{junction} Head (m)')

        for junction in JUNCTION_IDS:
            header.append(f'J{junction} Demand (LPS)')

        self.output_file.write(",".join(header) + '\n')

    def generate_inp_file(junction_id: int, emit: int):
        return inp_util.generate_custom_inp_file(
            target_file_path=f'{OUTPUT_EMIT_DIR}temp/J{junction_id}-ec{emit}.inp',
            customized_category=CATEGORY_EMITTERS,
            customized_component_id=str(junction_id),
            customized_column_index=MadaniScenario.INP_EMITTERS_COEFFICIENT_COLUMN_INDEX,
            custom_value=str(emit)
        )

    def write_row(self, inp_file: str, adjusted_junction_label: str, emit_label: str):
        # Simulate
        subprocess.call(["java", "-cp", EPANET_JAR_FILE, "org.addition.epanet.EPATool",
                         inp_file])

        # Write down the result
        csv_record = ",".join([
            adjusted_junction_label,
            emit_label,
            *get_flows(inp_file),
            *get_pressures(inp_file),
            *get_heads(inp_file),
            *get_demands(inp_file)
        ])
        self.output_file.write(csv_record + '\n')

    def _on_arrange(self):
        self._open_output_file()
        self._write_header()
        self.write_row(constant.INITIAL_INP_FILE, '-', '-')

    def _on_simulate(self):
            # Simulate all emitter coefficient variants on each pipe
            for junction_id in JUNCTION_IDS:
                # Get proper emit
                emit = emit_util.get_proper_emit(
                    adjusted_junction_id=junction_id,
                    expected_actual_demand=0.5
                )

                # Set up simulation
                inp_file = self.generate_inp_file(
                    junction_id=junction_id,
                    emit=emit
                )

                # Write row
                self.write_row(inp_file, str(junction_id), str(emit))

    def _on_clean_up(self):
        self.output_file.close()
