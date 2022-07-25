from scenarios.scenario import Scenario
import os
import shutil
import subprocess
from typing import TextIO

from scenario_data.madani_scenario_data import MadaniScenarioData
from utils import emit_util, inp_util
from utils.out_util import get_flows, get_actual_demands
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
        os.makedirs(self.__data.output_dir + 'temp_hill_climbing/')

        self.output_file = open(self.__data.output_dir + "water_flow_forecast.csv", 'w')

    def __write_header(self):
        header: list[str] = ['time_step', 'adjusted_junction_id', 'emit']

        for junction_id in self.__data.junction_ids:
            header.append(f'junction_{junction_id}_actual_demand')

        for pipe_id in self.__data.pipe_ids:
            header.append(f'pipe_{pipe_id}_flow')

        self.output_file.write(",".join(header) + '\n')

    def __generate_inp_file(self, junction_id: int, emit: int, time_step: str):
        return inp_util.generate_custom_inp_file(
            initial_inp_file=self.__data.initial_inp_file,
            target_file_path=f'{self.__data.output_dir}temp/{time_step.replace(":", "_")}_set_junction_{junction_id}_emit_{emit}.inp',
            customized_category=Simulator.CATEGORY_EMITTERS,
            customized_component_id=str(junction_id),
            customized_column_index=MadaniScenario.INP_EMITTERS_COEFFICIENT_COLUMN_INDEX,
            custom_value=str(emit)
        )

    def _on_arrange(self):
        self.__open_output_file()
        self.__write_header()

    def _on_simulate(self):
        for time_step in self.__data.time_steps:
            """Simulate on each time step"""

            # Simulate no leak
            csv_record = ",".join([
                time_step,
                '',
                '',
                *get_actual_demands(self.__data.initial_inp_file, time_step=time_step),
                *get_flows(self.__data.initial_inp_file, time_step=time_step)
            ])
            self.output_file.write(csv_record + '\n')

            # Simulate leak
            for junction_id in self.__data.junction_ids:
                """Simulate leak on each pipe by setting emitter coefficient"""

                # Get proper emit to reproduce actual demand of ... LPS
                # (based on scenario data)
                emit = emit_util.get_proper_emit(
                    initial_inp_file=self.__data.initial_inp_file,
                    output_dir=self.__data.output_dir,
                    adjusted_junction_id=junction_id,
                    time_step=time_step,
                    expected_actual_demand=self.__data.default_demand_based_on_sensors
                )

                # Set up simulation
                inp_file = self.__generate_inp_file(
                    junction_id=junction_id,
                    emit=emit,
                    time_step=time_step
                )

                # Simulate
                subprocess.call(["java", "-cp", Simulator.JAR_FILE, "org.addition.epanet.EPATool",
                                 inp_file])

                # Write row
                csv_record = ",".join([
                    time_step,
                    str(junction_id),
                    str(emit),
                    *get_actual_demands(inp_file, time_step=time_step),
                    *get_flows(inp_file, time_step=time_step)
                ])
                self.output_file.write(csv_record + '\n')

    def _on_clean_up(self):
        self.output_file.close()
