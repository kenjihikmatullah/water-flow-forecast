from scenarios.scenario import Scenario
import os
import shutil
import subprocess
from typing import TextIO

from scenario_data.madani_scenario_data import MadaniScenarioData
from utils import emit_util, inp_util
from utils.out_util import get_flows, get_pressures, get_heads, get_demands
from models.simulator import Simulator


class MadaniScenario(Scenario):
    """
    Simulate leak by setting some attributes:
    - emitter coeff. of each junction.
    - demand pattern

    This scenario aims to get WDS state when a leak occurs.
    """

    INP_EMITTERS_COEFFICIENT_COLUMN_INDEX = 1

    output_file: TextIO

    def __init__(self, data: MadaniScenarioData):
        self.__data = data

    def __open_output_file(self):
        if os.path.exists(self.__data.output_dir):
            shutil.rmtree(self.__data.output_dir)

        os.makedirs(self.__data.output_dir)
        os.makedirs(self.__data.output_dir + 'temp/')
        os.makedirs(self.__data.output_dir + 'temp-hill-climbing/')

        self.output_file = open(self.__data.output_dir + "water_flow_forecast.csv", 'w')

    def __write_header(self):
        header: list[str] = ['Time', 'Adjusted Junction', 'Emitter Coeff.']

        for pipe_id in self.__data.pipe_ids:
            header.append(f'P{pipe_id} Flow (LPS)')

        header.append('...what is this?')

        for junction_id in self.__data.junction_ids:
            header.append(f'J{junction_id} Pressure (m)')

        for junction_id in self.__data.junction_ids:
            header.append(f'J{junction_id} Head (m)')

        for junction_id in self.__data.junction_ids:
            header.append(f'J{junction_id} Demand (LPS)')

        self.output_file.write(",".join(header) + '\n')

    def __generate_inp_file(self, junction_id: int, emit: int):
        return inp_util.generate_custom_inp_file(
            initial_inp_file=self.__data.initial_inp_file,
            target_file_path=f'{self.__data.output_dir}temp/J{junction_id}-ec{emit}.inp',
            customized_category=Simulator.CATEGORY_EMITTERS,
            customized_component_id=str(junction_id),
            customized_column_index=MadaniScenario.INP_EMITTERS_COEFFICIENT_COLUMN_INDEX,
            custom_value=str(emit)
        )

    def __write_row(self, inp_file: str, adjusted_junction_label: str, emit_label: str):
        # Simulate
        subprocess.call(["java", "-cp", Simulator.JAR_FILE, "org.addition.epanet.EPATool",
                         inp_file])

        # Times, used if scenario is based on time-series
        times = self.__data.times
        if len(times) == 0:
            times = ['00:00:00']

        # Write down the result for every time period
        for time in times:
            csv_record = ",".join([
                time,
                adjusted_junction_label,
                emit_label,
                *get_flows(inp_file, time=time),
                *get_pressures(inp_file, time=time),
                *get_heads(inp_file, time=time),
                *get_demands(inp_file, time=time)
            ])
            self.output_file.write(csv_record + '\n')

    def _on_arrange(self):
        self.__open_output_file()
        self.__write_header()
        self.__write_row(
            inp_file=self.__data.initial_inp_file,
            adjusted_junction_label='-',
            emit_label='-'
        )

    def _on_simulate(self):
        # Simulate all emitter coefficient variants on each pipe
        for junction_id in self.__data.junction_ids:
            # Get proper emit
            emit = emit_util.get_proper_emit(
                initial_inp_file=self.__data.initial_inp_file,
                output_dir=self.__data.output_dir,
                adjusted_junction_id=junction_id,
                expected_actual_demand=0.5
            )

            # Set up simulation
            inp_file = self.__generate_inp_file(
                junction_id=junction_id,
                emit=emit
            )

            # Write row
            self.__write_row(
                inp_file=inp_file,
                adjusted_junction_label=str(junction_id),
                emit_label=str(emit)
            )

    def _on_clean_up(self):
        self.output_file.close()
