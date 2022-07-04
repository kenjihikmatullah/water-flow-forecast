from models.inp_metadata import InpMetadata
from models.junction import Junction
from models.timing_type import TimingType
from simulators.epanet_simulator import EpanetSimulator
from utils.InpMetadataCreator import InpMetadataCreator


# TODO: Make this injected
class InpMetadataCreatorImpl(InpMetadataCreator):

    def create(self, path: str) -> InpMetadata:
        file = open(path, 'r')
        lines = file.readlines()

        return InpMetadata(
            junctions=self.__get_junctions(lines),
            pipe_ids=self.__get_pipe_ids(),
            timing_type=self.__get_timing_type(),
            times=self.__get_times()
        )

    @staticmethod
    def __get_objects(cls, lines: list[str], category: str):
        attributes: list[str] = []
        objects: list[dict[str, str]] = []

        in_category = False
        for i in range(0, len(lines)):
            columns = lines[i].split(' ')
            columns = list(filter(lambda x: x != '', columns))

            if in_category:
                if len(columns) == 1:
                    break

                else:
                    if columns[0].startswith(';'):
                        for column in columns:
                            attributes.append(column.replace(';', ''))

                    else:
                        for i in range(len(columns)):
                            objects.append()

            elif columns[0].find(category) > -1:
                in_category = True

        return objects

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
                        elevation=float(columns[1] if 1 < len(columns) else 0),
                        demand=float(columns[2] if 2 < len(columns) else 0),
                        pattern=columns[3] if 3 < len(columns) else None
                    )
                    junctions.append(junction)
            else:
                if len(columns) == 0:
                    continue

                if columns[0].find(EpanetSimulator.CATEGORY_JUNCTIONS) > -1:
                    in_category = True

        print(junctions)
        return junctions

    @classmethod
    def __get_pipe_ids(cls) -> list[str]:
        return []  # TODO

    @classmethod
    def __get_timing_type(cls) -> TimingType:
        return TimingType.TIME_SERIES  # TODO

    @classmethod
    def __get_times(cls) -> list[str]:
        return []  # TODO
