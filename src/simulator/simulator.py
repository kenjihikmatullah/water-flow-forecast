import subprocess
from typing import TextIO

from models.epanet_constants import EpanetConstants
from repository.simulation_result_repository import SimulationResultRepository
from models.simulation_result import SimulationResult
from models.simulation_session import SimulationSession
from models.scenario_data import ScenarioData
from utils import inp_util, out_util
from utils.emit_util import EmitUtil
from utils.inp_util import INP_EMITTERS_COEFFICIENT_COLUMN_INDEX


class Simulator:
    """
    Simulate leak by setting some attributes:
    - emitter coeff. of each junction.
    - demand pattern

    This scenario aims to get WDS state (pipe flow) when a leak with consistent volume happens at a junction all week
    """

    output_file: TextIO

    def __init__(self, data: ScenarioData):
        self.__data = data
        self.repository = SimulationResultRepository()

    def __generate_inp_file(self, junction_id: int, emit: int, time_step: str):
        return inp_util.generate_custom_inp_file(
            initial_inp_file=self.__data.initial_inp_file,
            target_file_path=f'{self.__data.output_dir}temp/{time_step.replace(":", "_")}_set_junction_{junction_id}_emit_{emit}.inp',
            customized_category=EpanetConstants.CATEGORY_EMITTERS,
            customized_component_id=str(junction_id),
            customized_column_index=INP_EMITTERS_COEFFICIENT_COLUMN_INDEX,
            custom_value=str(emit)
        )

    def run(self):
        self._on_arrange()
        self._on_simulate()
        self._on_post_simulate()

    def _on_arrange(self):
        self.__session_result = SimulationSession()
        self.__session_result.session_id = '2022-11-19 08:30:00'

    def _on_simulate(self):
        for time_step in self.__data.time_steps:
            """Simulate on each time step"""

            # Simulate no leak
            subprocess.call(["java", "-cp", EpanetConstants.JAR_FILE, "org.addition.epanet.EPATool",
                             self.__data.initial_inp_file])

            pipes_when_no_leak = out_util.get_pipes(inp_file=self.__data.initial_inp_file, time_step=time_step)
            for p in pipes_when_no_leak:
                p.base_flow = p.flow

            result_when_no_leak = SimulationResult(
                custom_inp_file=self.__data.initial_inp_file,
                time_step=time_step,
                leaking_junction_id=None,
                leaking_junction_emit=None,
                leaking_junction_leak=None,
                junctions=out_util.get_junctions(inp_file=self.__data.initial_inp_file, time_step=time_step),
                pipes=pipes_when_no_leak
            )
            self.__session_result.results.append(result_when_no_leak)

            for junction_id in self.__data.junction_ids:
                """Simulate leak on each pipe by setting emitter coefficient"""

                # if time_step == '02:00:00':
                #     break
                #
                # if int(junction_id) > 2:
                #     break

                junction_when_no_leak = self.__session_result.get_junction_result_when_no_leak(junction_id, '01:00:00')
                demand_when_no_leak = junction_when_no_leak.actual_demand

                emit_to_simulate_leak_result = EmitUtil().get_emit_to_simulate_certain_leak(
                    initial_inp_file=self.__data.initial_inp_file,
                    output_dir=self.__data.output_dir,
                    adjusted_junction_id=junction_id,
                    expected_leak=self.__data.default_leak_to_simulate,
                    demand_when_no_leak=demand_when_no_leak,
                    time_step=time_step
                )
                emit = emit_to_simulate_leak_result.emit
                actual_leak = emit_to_simulate_leak_result.actual_leak

                # Set up simulation
                inp_file = self.__generate_inp_file(
                    junction_id=junction_id,
                    emit=emit,
                    time_step=time_step
                )

                # Simulate
                subprocess.call(["java", "-cp", EpanetConstants.JAR_FILE, "org.addition.epanet.EPATool",
                                 inp_file])

                # Get result
                result_junctions = out_util.get_junctions(inp_file=inp_file, time_step=time_step)
                result_pipes = out_util.get_pipes(inp_file=inp_file, time_step=time_step)
                for pipe in result_pipes:
                    for p in pipes_when_no_leak:
                        if pipe.id == p.id:
                            pipe.base_flow = p.flow
                            break

                # Put result
                self.__session_result.results.append(
                    SimulationResult(
                        custom_inp_file=inp_file,
                        time_step=time_step,
                        leaking_junction_id=junction_id,
                        leaking_junction_emit=emit,
                        leaking_junction_leak=actual_leak,
                        junctions=result_junctions,
                        pipes=result_pipes
                    )
                )

    def _on_post_simulate(self):
        # for exporter in self.__exporters:
        #     exporter.export(self.__session_result)

        self.repository.store(self.__session_result)
