from exporter.madani.madani_csv_exporter import MadaniCsvExporter
from result.madani.madani_result import MadaniResult
from result.madani.madani_session_result import MadaniSessionResult
from scenarios.scenario import Scenario
import subprocess
from typing import TextIO

from scenario_data.madani_scenario_data import MadaniScenarioData
from utils import emit_util, inp_util, out_util
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
        self.__exporter = MadaniCsvExporter(self.__data)
        self.__exporter.write_header()
        self.__session_result = MadaniSessionResult()

    def _on_simulate(self):
        for time_step in self.__data.time_steps:
            """Simulate on each time step"""

            # Simulate no leak
            subprocess.call(["java", "-cp", Simulator.JAR_FILE, "org.addition.epanet.EPATool",
                             self.__data.initial_inp_file])
            self.__session_result.results.append(
                MadaniResult(
                    custom_inp_file=self.__data.initial_inp_file,
                    time_step=time_step,
                    adjusted_junction_id=None,
                    emit=None,
                    junctions=out_util.get_junctions(inp_file=self.__data.initial_inp_file, time_step=time_step),
                    pipes=out_util.get_pipes(inp_file=self.__data.initial_inp_file, time_step=time_step)
                )
            )

            # Simulate leak
            for junction_id in self.__data.junction_ids:
                if junction_id == '3':
                    return
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

                # Put result
                self.__session_result.results.append(
                    MadaniResult(
                        custom_inp_file=inp_file,
                        time_step=time_step,
                        adjusted_junction_id=junction_id,
                        emit=emit,
                        junctions=out_util.get_junctions(inp_file=inp_file, time_step=time_step),
                        pipes=out_util.get_pipes(inp_file=inp_file, time_step=time_step)
                    )
                )

    def _on_post_simulate(self):
        self.__exporter.write_body(self.__session_result)
        self.__exporter.close()
