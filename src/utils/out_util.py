from typing.io import TextIO

LINKS_OUT_EXTENSION = '.links.out'
NODES_OUT_EXTENSION = '.nodes.out'

SEPARATOR = '\t'
NUMBER_OF_HEADER_ROWS = 2

COMPONENT_ID_COLUMN_INDEX = 0
TIME_STEP_COLUMN_INDEX = 1

LINKS_OUT_FLOW_COLUMN_INDEX = 5
NODES_OUT_PRESSURE_COLUMN_INDEX = 4
NODES_OUT_HEAD_COLUMN_INDEX = 5
NODES_OUT_ACTUAL_DEMAND_COLUMN_INDEX = 6


def _extract_result(inp_file: str, extension: str, column_index: int, component_id: int, time_step: str) -> str:
    result_file: TextIO | None = None

    try:
        result_file = open(f'{inp_file}{extension}', 'r')
        lines = result_file.readlines()

    except OSError as e:
        raise OSError(e, f'Failed to open {inp_file}{extension}')

    finally:
        if result_file is not None:
            result_file.close()

    for i in range(0, len(lines) - NUMBER_OF_HEADER_ROWS):
        line = lines[i + NUMBER_OF_HEADER_ROWS].split('\t')

        if line[COMPONENT_ID_COLUMN_INDEX] == str(component_id) and line[TIME_STEP_COLUMN_INDEX] == time_step:
            return line[column_index]


def _extract_results(inp_file: str, extension: str, column_index: int, time_step: str = '00:00:00') -> list[str]:
    result_file: TextIO | None = None
    results = []

    try:
        result_file = open(f'{inp_file}{extension}', 'r')
        lines = result_file.readlines()

    except OSError as e:
        raise OSError(e, f'Failed to open {inp_file}{extension}')

    finally:
        if result_file is not None:
            result_file.close()

    for i in range(0, len(lines) - NUMBER_OF_HEADER_ROWS):
        line = lines[i + NUMBER_OF_HEADER_ROWS].split('\t')

        if extension == NODES_OUT_EXTENSION and line[0] == '71':
            continue

        if line[1] != time_step:
            continue

        results.append(line[column_index].replace('\n', ''))

    return results


def get_flows(inp_file: str, time_step: str = '00:00:00'):
    """
    Get flow of each pipe on certain time step
    """
    return _extract_results(
        inp_file=inp_file,
        extension=LINKS_OUT_EXTENSION,
        column_index=LINKS_OUT_FLOW_COLUMN_INDEX,
        time_step=time_step
    )


def get_actual_demands(inp_file: str, time_step: str = '00:00:00'):
    """
    Get actual demand of each junction on certain time step
    """
    return _extract_results(
        inp_file=inp_file,
        extension=NODES_OUT_EXTENSION,
        column_index=NODES_OUT_ACTUAL_DEMAND_COLUMN_INDEX,
        time_step=time_step
    )


def get_actual_demand(inp_file: str, junction_id: int, time_step: str = '00:00:00'):
    """
    Get actual demand of certain junction on certain time step
    """
    return _extract_result(
        inp_file=inp_file,
        extension=NODES_OUT_EXTENSION,
        column_index=NODES_OUT_ACTUAL_DEMAND_COLUMN_INDEX,
        component_id=junction_id,
        time_step=time_step
    )
