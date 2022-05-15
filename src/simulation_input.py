from constant import INITIAL_INP_FILE


def change_property_value(lines: list[str], category: str, component_id: str, column_index: int, new_value: str):
    in_category = False

    for i in range(0, len(lines)):
        columns = lines[i].split(' ')
        columns = list(filter(lambda x: x != '', columns))

        if in_category:
            if len(columns) == 1:
                break

            else:
                if columns[0] == component_id:
                    columns[column_index] = new_value
                    separator = "    "
                    lines[i] = separator.join(columns)
                    break

        elif columns[0].find(category) > -1:
            in_category = True


def generate_custom_inp_file(target_file_path: str, customized_category: str, customized_component_id: str,
                             customized_column_index: int, custom_value: str):
    initial_inp_file = open(INITIAL_INP_FILE, 'r')
    target_inp_file = open(target_file_path, 'w')

    try:
        lines = initial_inp_file.readlines()

        change_property_value(
            lines=lines,
            category=customized_category,
            component_id=customized_component_id,
            column_index=customized_column_index,
            new_value=custom_value
        )

        for line in lines:
            target_inp_file.write(line)

        print(f'Created: {target_file_path}')

    finally:
        initial_inp_file.close()
        target_inp_file.close()

    return target_file_path
