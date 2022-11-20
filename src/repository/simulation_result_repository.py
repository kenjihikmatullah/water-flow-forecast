from itertools import groupby
from operator import itemgetter

from db_client.maria_db_client import MariaDbClient
from models.pipe import Pipe
from models.simulation_result import SimulationResult
from models.simulation_session import SimulationSession


class SimulationResultRepository:

    def __init__(self):
        self.db_client = MariaDbClient()

    def create_cases_table(self):
        statement = """
            CREATE TABLE `simulation_results` (
                `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                `session_id` VARCHAR(32) NOT NULL,
                `time_step` VARCHAR(32) NOT NULL,
                `leaking_junction_id` VARCHAR(32) NULL,
                `leaking_junction_emit` FLOAT NULL,
                `leaking_junction_leak` FLOAT NULL COMMENT 'actual demand - (base demand * demand multiplier)',
                
                PRIMARY KEY (id)
            )
        """
        self.db_client.execute(statement, [])
        self.db_client.cursor.close()

    def create_delta_flow_table(self):
        statement = """
            CREATE TABLE `simulation_pipe_flow` (
                `result_id` INT UNSIGNED NOT NULL,
                `pipe_id` VARCHAR(32) NOT NULL,
                `pipe_flow` FLOAT NOT NULL,
                `pipe_delta_flow` FLOAT NOT NULL,
                
                FOREIGN KEY (result_id) REFERENCES simulation_results(id)
            )
        """
        self.db_client.execute(statement, [])
        self.db_client.cursor.close()

    def get_simulation_results(self, session_id: str, time_step: str) -> SimulationSession:
        statement = """
            SELECT *
            FROM simulation_results sr
            JOIN simulation_pipe_flow spf ON spf.result_id = sr.id
            WHERE sr.session_id = ?
            AND sr.time_step = ?
            ORDER BY result_id, CAST(pipe_id AS UNSIGNED)
        """

        self.db_client.execute(statement, [session_id, time_step])
        print("Extracting result from DB...")

        results = self.db_client.cursor.fetchall()
        print(results)
        columns = self.db_client.cursor.description
        rows = [{columns[index][0]: column for index, column in enumerate(value)} for value in results]

        print("Converting row to POJO...")
        session_result = SimulationSession()
        session_result.session_id = session_id

        for key, value in groupby(rows, key=itemgetter('result_id')):
            pipes: list[Pipe] = []

            values = list(value)
            val = values[0]

            time_step = val['time_step']
            leaking_junction_id = val['leaking_junction_id']
            leaking_junction_emit = val['leaking_junction_emit']
            leaking_junction_leak = val['leaking_junction_leak']

            for df_row in values:
                pipes.append(
                    Pipe(
                        id=df_row['pipe_id'],
                        flow=df_row['pipe_flow'],
                        delta_flow=df_row['pipe_delta_flow']
                    )
                )

            session_result.results.append(
                SimulationResult(
                    custom_inp_file='',
                    time_step=time_step,
                    leaking_junction_id=leaking_junction_id,
                    leaking_junction_emit=leaking_junction_emit,
                    leaking_junction_leak=leaking_junction_leak,
                    junctions=[],
                    pipes=pipes
                )
            )

        return session_result

    def store(self, session_result: SimulationSession):
        for case in session_result.results:
            statement = """
                INSERT INTO `simulation_results` (session_id, time_step, leaking_junction_id, leaking_junction_emit, leaking_junction_leak) 
                VALUES (?, ?, ?, ?, ?)
            """
            self.db_client.execute(statement, [session_result.session_id, case.time_step, case.leaking_junction_id, case.leaking_junction_emit, case.leaking_junction_leak])
            result_id = self.db_client.cursor.lastrowid

            for pipe in case.pipes:
                statement_df = """
                    INSERT INTO `simulation_pipe_flow` (result_id, pipe_id, pipe_flow, pipe_delta_flow) VALUES (?, ?, ?, ?)
                """
                self.db_client.execute(statement_df, [result_id, pipe.id, pipe.flow, pipe.get_delta_flow()])
