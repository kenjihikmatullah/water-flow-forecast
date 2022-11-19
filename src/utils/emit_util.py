import subprocess

from models.emit_to_simulate_leak_result import EmitToSimulateLeakResult
from models.simulator import Simulator
from utils import out_util, inp_util
from utils.inp_util import INP_EMITTERS_COEFFICIENT_COLUMN_INDEX

EMIT_CLIMB_STEP = 0.005


class EmitUtil:

    def get_proper_emit(self, initial_inp_file: str, output_dir: str, adjusted_junction_id: int,
                        expected_actual_demand: float, base_demand: int = 0, time_step: str = '00:00:00'):
        """
        get proper emit to achieve expected actual demand
        on adjusted junction

        this method use hill climbing approach

        @:param expected_actual_demand: in LPS
        """

        emit = 0
        prev_actual_demand = 0
        while True:
            emit += EMIT_CLIMB_STEP

            # Set emit
            inp_file = inp_util.generate_custom_inp_file(
                initial_inp_file=initial_inp_file,
                target_file_path=f'{output_dir}temp_hill_climbing/{time_step.replace(":", "_")}_set_junction_{adjusted_junction_id}_emit_{emit}.inp',
                customized_category=Simulator.CATEGORY_EMITTERS,
                customized_component_id=str(adjusted_junction_id),
                customized_column_index=INP_EMITTERS_COEFFICIENT_COLUMN_INDEX,
                custom_value=str(emit)
            )

            # Simulate
            subprocess.call(["java", "-cp", Simulator.JAR_FILE, "org.addition.epanet.EPATool",
                             inp_file])

            actual_demand_str = out_util.get_actual_demand(
                inp_file=inp_file,
                junction_id=adjusted_junction_id,
                time_step=time_step
            )
            actual_demand = float(actual_demand_str.replace('\n', ''))

            print("[Hill Climbing] junction_id={}, base_demand={}, time_step={}, emit={}, then actual demand={}".format(
                adjusted_junction_id, base_demand, time_step, emit, actual_demand))

            # Check whether desired actual demand is achieved
            if actual_demand > expected_actual_demand:
                current_diff = actual_demand - expected_actual_demand
                prev_diff = expected_actual_demand - prev_actual_demand

                if prev_diff < current_diff:
                    print('[Hill Climbing] selected emit=' + str(emit - EMIT_CLIMB_STEP))
                    return emit - EMIT_CLIMB_STEP
                else:
                    print('[Hill Climbing] selected emit=' + str(emit))
                    return emit

            else:
                prev_actual_demand = actual_demand

    def get_emit_to_simulate_certain_leak(self, initial_inp_file: str, output_dir: str, adjusted_junction_id: int,
                                          expected_leak: float, demand_when_no_leak: float,
                                          time_step: str = '00:00:00') -> EmitToSimulateLeakResult:
        """
        get proper emit to simulate certain leak on certain junction

        this method use hill climbing approach
        :param expected_leak: in LPS
        :param demand_when_no_leak: in LPS
        :return:
        """

        current_emit = 0
        prev_leak = 0
        while True:
            current_emit += EMIT_CLIMB_STEP

            # Set emit
            inp_file = inp_util.generate_custom_inp_file(
                initial_inp_file=initial_inp_file,
                target_file_path=f'{output_dir}temp_hill_climbing/{time_step.replace(":", "_")}_set_junction_{adjusted_junction_id}_emit_{current_emit}.inp',
                customized_category=Simulator.CATEGORY_EMITTERS,
                customized_component_id=str(adjusted_junction_id),
                customized_column_index=INP_EMITTERS_COEFFICIENT_COLUMN_INDEX,
                custom_value=str(current_emit)
            )

            # Simulate
            subprocess.call(["java", "-cp", Simulator.JAR_FILE, "org.addition.epanet.EPATool",
                             inp_file])

            actual_demand_str = out_util.get_actual_demand(
                inp_file=inp_file,
                junction_id=adjusted_junction_id,
                time_step=time_step
            )
            actual_demand = float(actual_demand_str.replace('\n', ''))
            leak = actual_demand - demand_when_no_leak

            print(
                "[Hill Climbing] junction_id={}, demand_when_no_leak={}, time_step={}, emit={}, then actual demand_when_leak={}".format(
                    adjusted_junction_id, demand_when_no_leak, time_step, current_emit, actual_demand))

            # Check whether expected leak to simulate is achieved
            if leak > expected_leak:
                current_diff = leak - expected_leak
                prev_diff = expected_leak - prev_leak

                selected_emit = 0
                leak_of_selected_emit = 0

                if prev_diff < current_diff:
                    selected_emit = current_emit - EMIT_CLIMB_STEP
                    leak_of_selected_emit = prev_leak

                else:
                    selected_emit = current_emit
                    leak_of_selected_emit = leak

                print(
                    f"[Hill Climbing] selected emit={str(selected_emit)}, leak of selected emit={str(leak_of_selected_emit)}")

                return EmitToSimulateLeakResult(
                    emit=selected_emit,
                    actual_leak=leak_of_selected_emit
                )

            else:
                prev_leak = leak
