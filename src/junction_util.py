def print_junction_ids():
    junction_ids = []

    inp_file = open('input/its_water_distribution.inp', 'r')
    lines = inp_file.readlines()
    in_category = False
    for i in range(0, len(lines)):
        columns = lines[i].split(' ')
        columns = list(filter(lambda x: x != '', columns))

        if in_category:
            if len(columns) == 1:
                break

            else:
                if columns[0] != ';ID':
                    junction_ids.append(int(columns[0]))

        elif columns[0].find('JUNCTIONS') > -1:
            in_category = True

    print(junction_ids)
