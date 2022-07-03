from utils import inp_util, out_util
from properties.constant import EPANET_JAR_FILE, CATEGORY_EMITTERS, OUTPUT_EMIT_DIR
import subprocess

INP_EMITTERS_COEFFICIENT_COLUMN_INDEX = 1


def get_proper_emit(adjusted_junction_id: int, expected_actual_demand: float, base_demand: int = 0):
    """
    get proper emit to achieve expected actual demand
    on adjusted junction

    this method use hill climbing approach

    @:param expected_actual_demand: in LPS
    """

    emit = 0
    prev_actual_demand = 0
    while True:
        emit += 0.01

        # Set up simulation
        inp_file = inp_util.generate_custom_inp_file(
            target_file_path=f'{OUTPUT_EMIT_DIR}temp-hill-climbing/j-index-{adjusted_junction_id}-ec{emit}.inp',
            customized_category=CATEGORY_EMITTERS,
            customized_component_id=str(adjusted_junction_id),
            customized_column_index=INP_EMITTERS_COEFFICIENT_COLUMN_INDEX,
            custom_value=str(emit)
        )

        # Simulate
        subprocess.call(["java", "-cp", EPANET_JAR_FILE, "org.addition.epanet.EPATool",
                         inp_file])

        # Check whether desired actual demand is achieved
        actual_demand_str = out_util.get_demand(
            inp_file=inp_file,
            component_id=adjusted_junction_id
        )
        actual_demand = float(actual_demand_str.replace('\n', ''))

        print("[Hill Climbing] junction_id={}, emit={}, base_demand={}, then actual demand={}".format(
            adjusted_junction_id, emit, base_demand, actual_demand))

        if actual_demand > expected_actual_demand:
            current_diff = actual_demand - expected_actual_demand
            prev_diff = expected_actual_demand - prev_actual_demand

            if prev_diff < current_diff:
                print('[Hill Climbing] selected emit=' + str(emit - 0.01))
                return emit - 0.01
            else:
                print('[Hill Climbing] selected emit=' + str(emit))
                return emit
