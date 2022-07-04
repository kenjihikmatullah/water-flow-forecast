LINKS_OUT_EXTENSION = '.links.out'
NODES_OUT_EXTENSION = '.nodes.out'

SEPARATOR = '\t'
NUMBER_OF_HEADER_ROWS = 2

LINKS_OUT_FLOW_COLUMN_INDEX = 5
NODES_OUT_PRESSURE_COLUMN_INDEX = 4
NODES_OUT_HEAD_COLUMN_INDEX = 5
NODES_OUT_DEMAND_COLUMN_INDEX = 6

def _extract_result(inp_file: str, extension: str, column_index: int, component_id: int) -> str:
    try:
        result_file = open(f'{inp_file}{extension}', 'r')
        lines = result_file.readlines()

    except OSError as e:
        raise OSError(e, f'Failed to open {inp_file}{extension}')

    finally:
        result_file.close()

    for i in range(0, len(lines) - NUMBER_OF_HEADER_ROWS):
        line = lines[i + NUMBER_OF_HEADER_ROWS].split('\t')

        if line[0] == str(component_id):
            return line[column_index]


def _extract_results(inp_file: str, extension: str, column_index: int, time: str = '00:00:00') -> list[str]:
    results = []

    try:
        result_file = open(f'{inp_file}{extension}', 'r')
        lines = result_file.readlines()

    except OSError as e:
        raise OSError(e, f'Failed to open {inp_file}{extension}')

    finally:
        result_file.close()

    for i in range(0, len(lines) - NUMBER_OF_HEADER_ROWS):
        line = lines[i + NUMBER_OF_HEADER_ROWS].split('\t')

        if extension == NODES_OUT_EXTENSION and line[0] == '71':
            continue

        if line[1] != time:
            continue

        results.append(line[column_index].replace('\n', ''))

    return results


def get_flows(inp_file: str, time: str = '00:00:00'):
    return _extract_results(
        inp_file=inp_file,
        extension=LINKS_OUT_EXTENSION,
        column_index=LINKS_OUT_FLOW_COLUMN_INDEX
    )


def get_pressures(inp_file: str, time: str = '00:00:00'):
    return _extract_results(
        inp_file=inp_file,
        extension=NODES_OUT_EXTENSION,
        column_index=NODES_OUT_PRESSURE_COLUMN_INDEX
    )


def get_heads(inp_file: str, time: str = '00:00:00'):
    return _extract_results(
        inp_file=inp_file,
        extension=NODES_OUT_EXTENSION,
        column_index=NODES_OUT_PRESSURE_COLUMN_INDEX
    )


def get_demands(inp_file: str, time: str = '00:00:00'):
    return _extract_results(
        inp_file=inp_file,
        extension=NODES_OUT_EXTENSION,
        column_index=NODES_OUT_DEMAND_COLUMN_INDEX
    )

def get_demand(inp_file: str, component_id: int):
    return _extract_result(
        inp_file=inp_file,
        extension=NODES_OUT_EXTENSION,
        column_index=NODES_OUT_DEMAND_COLUMN_INDEX,
        component_id=component_id
    )
