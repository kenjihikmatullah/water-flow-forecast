from models.inp_metadata import InpMetadata
from models.junction import Junction
from models.pipe import Pipe
from models.epanet_constants import EpanetConstants
from models.inp_metadata import InpMetadata


class InpMetadataCreator:

    def create(self, path: str) -> InpMetadata:
        file = open(path, 'r')
        lines = file.readlines()

        return InpMetadata(
            junctions=self.__get_junctions(lines),
            pipes=self.__get_pipes(lines),
            time_steps=self.__get_time_steps(lines)
        )

    @classmethod
    def __get_junctions(cls, lines: list[str]) -> list[Junction]:
        junctions: list[Junction] = []

        in_category = False
        for i in range(0, len(lines)):
            columns = lines[i].split()

            if in_category:
                if len(columns) == 0:
                    break

                if columns[0].startswith(';'):
                    continue

                else:
                    if ';' in columns:
                        columns.remove(';')

                    junction = Junction(
                        id=columns[0],
                        base_demand=float(columns[2] if 2 < len(columns) else 0),
                        pattern=columns[3] if 3 < len(columns) else None
                    )
                    junctions.append(junction)
            else:
                if len(columns) == 0:
                    continue

                if columns[0].find(EpanetConstants.CATEGORY_JUNCTIONS) > -1:
                    in_category = True

        return junctions

    @classmethod
    def __get_pipes(cls, lines: list[str]) -> list[Pipe]:
        pipes: list[Pipe] = []

        in_category = False
        for i in range(0, len(lines)):
            columns = lines[i].split()

            if in_category:
                if len(columns) == 0:
                    break

                if columns[0].startswith(';'):
                    continue

                else:
                    if ';' in columns:
                        columns.remove(';')

                    pipe = Pipe(
                        id=columns[0],
                    )
                    pipes.append(pipe)
            else:
                if len(columns) == 0:
                    continue

                if columns[0].find(EpanetConstants.CATEGORY_PIPES) > -1:
                    in_category = True

        return pipes

    @classmethod
    def __get_time_steps(cls, lines: list[str]) -> list[str]:
        duration = 0
        pattern_timestep = 0
        pattern_start = 0

        in_category = False
        for i in range(0, len(lines)):
            columns = lines[i].strip().split()

            if in_category:
                if len(columns) == 0:
                    break

                if columns[0] == 'Duration':
                    duration = int(columns[1].split(':')[0])
                    continue

                if columns[0] == 'Pattern':
                    if columns[1] == 'Timestep':
                        pattern_timestep = int(columns[2].split(':')[0])

                    elif columns[1] == 'Start':
                        pattern_start = int(columns[2].split(':')[0])

            else:
                if len(columns) == 0:
                    continue

                if columns[0].find(EpanetConstants.CATEGORY_TIMES) > -1:
                    in_category = True

        times: list[str] = []

        current = pattern_start
        for i in range(duration):
            current += pattern_timestep

            time = ''

            if current < 10:
                time = '0' + str(current)
            else:
                time = str(current)

            time = time + ':00:00'
            times.append(time)

        return times
