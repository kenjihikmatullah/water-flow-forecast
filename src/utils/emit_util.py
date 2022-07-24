from utils import inp_util, out_util
from models.simulator import Simulator
import subprocess

INP_EMITTERS_COEFFICIENT_COLUMN_INDEX = 1

EMIT_CLIMB_STEP = 0.005

def get_proper_emit(initial_inp_file: str, output_dir: str, adjusted_junction_id: int,
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
            target_file_path=f'{output_dir}temp-hill-climbing/j-index-{adjusted_junction_id}-ec{emit}.inp',
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