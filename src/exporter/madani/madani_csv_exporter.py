from exporter.csv_exporter import CsvExporter
import os
import shutil

from result.madani.madani_session_result import MadaniSessionResult
from scenario_data.madani_scenario_data import MadaniScenarioData


class MadaniCsvExporter(CsvExporter):

    def __init__(self, data: MadaniScenarioData):
        self.__data = data

    def export(self, session_result: MadaniSessionResult):
        self.__initialize()
        self.__write_header()
        self.__write_body(session_result)
        self.close()

    def __initialize(self):
        if os.path.exists(self.__data.output_dir):
            shutil.rmtree(self.__data.output_dir)

        os.makedirs(self.__data.output_dir)
        os.makedirs(self.__data.output_dir + 'temp/')
        os.makedirs(self.__data.output_dir + 'temp_hill_climbing/')

        self._initialize(self.__data.output_dir + "water_flow_forecast.csv")

    def __write_header(self):
        header: list[str] = ['time_step', 'adjusted_junction_id', 'emit']

        for junction_id in self.__data.junction_ids:
            header.append(f'junction_{junction_id}_actual_demand')

        for pipe_id in self.__data.pipe_ids:
            header.append(f'pipe_{pipe_id}_flow')

        self._write_row(header)

    def __write_body(self, session_result: MadaniSessionResult):
        for result in session_result.results:
            row = [
                result.time_step,
                result.adjusted_junction_id or '',
                str(result.emit),
                *map(lambda j: str(j.actual_demand), result.junctions),
                *map(lambda j: str(j.flow), result.pipes)
            ]
            self._write_row(row)
