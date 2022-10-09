from db_client.maria_db_client import MariaDbClient
from result.madani.madani_result import MadaniResult
from result.madani.madani_session_result import MadaniSessionResult


class MadaniPerTimeMariaDbExporter:

    def __init__(self):
        self.db_client = MariaDbClient()

    def export(self, session_result: MadaniSessionResult):
        for result in session_result.results:
            if result.time_step == '01:00:00':
                self.insert_row(result, 'andalus_results_time_1')

            elif result.time_step == '02:00:00':
                self.insert_row(result, 'andalus_results_time_2')

            elif result.time_step == '03:00:00':
                self.insert_row(result, 'andalus_results_time_3')

            elif result.time_step == '04:00:00':
                self.insert_row(result, 'andalus_results_time_4')

            elif result.time_step == '05:00:00':
                self.insert_row(result, 'andalus_results_time_5')

            elif result.time_step == '06:00:00':
                self.insert_row(result, 'andalus_results_time_6')

            elif result.time_step == '07:00:00':
                self.insert_row(result, 'andalus_results_time_7')

    def insert_row(self, result: MadaniResult, table: str):
        attribute_names = "time_step, adjusted_junction_id, adjusted_junction_emit, adjusted_junction_leak"
        for pipe_id in result.pipe_ids:
            attribute_names += f', pipe_{pipe_id}_flow'

        attribute_values_question = '?, ?, ?, ?'
        for pipe in result.pipes:
            attribute_values_question += ', ?'

        attribute_values = [result.time_step, result.adjusted_junction_id, result.adjusted_junction_emit,
                            result.adjusted_junction_leak]
        for pipe in result.pipes:
            attribute_values.append(pipe.delta_flow)

        statement = f'INSERT INTO {table}({attribute_names})  VALUES ({attribute_values_question})'

        self.db_client.execute(statement, attribute_values)