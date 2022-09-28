from db_client.maria_db_client import MariaDbClient
from result.madani.madani_session_result import MadaniSessionResult


class MadaniMariaDbExporter:

    def __init__(self, table='simulation_results'):
        self.db_client = MariaDbClient()
        self.__table = table

    def export(self, session_result: MadaniSessionResult):

        for result in session_result.results:
            attribute_names = "time_step, adjusted_junction_id, adjusted_junction_emit, adjusted_junction_leak"
            for pipe_id in result.pipe_ids:
                attribute_names += f', pipe_{pipe_id}_flow'

            attribute_values_question = '?, ?, ?, ?'
            for pipe in result.pipes:
                attribute_values_question += ', ?'

            attribute_values = [result.time_step, result.adjusted_junction_id, result.adjusted_junction_emit,
                                result.adjusted_junction_leak]
            for pipe in result.pipes:
                attribute_values.append(pipe.flow)

            statement = f'INSERT INTO {self.__table}({attribute_names})  VALUES ({attribute_values_question})'

            self.db_client.execute(statement, attribute_values)

        self.db_client.connection.close()
