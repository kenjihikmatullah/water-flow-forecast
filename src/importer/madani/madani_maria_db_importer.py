from db_client.maria_db_client import MariaDbClient
from models.junction import Junction
from models.pipe import Pipe
from result.madani.madani_result import MadaniResult
from result.madani.madani_session_result import MadaniSessionResult


class MadaniMariaDbImporter:

    def __init__(self, table='simulation_results'):
        self.db_client = MariaDbClient()
        self.__table = table

    def do_import(self) -> MadaniSessionResult:
        statement = "SELECT * FROM " + self.__table
        print("Importing from DB...")
        self.db_client.execute(statement, [])

        print("Extracting result from DB...")
        columns = self.db_client.cursor.description
        fetchall = self.db_client.cursor.fetchall()
        rows = [{columns[index][0]: column for index, column in enumerate(value)} for value in fetchall]

        # for row in rows:
        #     for attr in row:
        #         print(row)

        session_result: MadaniSessionResult = MadaniSessionResult()

        for row in rows:
            print("Converting row to POJO...")

            if row['time_step'] == '03:00':
                break

            # time_step: str = ''
            # adjusted_junction_id: str | None = None
            # adjusted_junction_emit: float | None = None
            # adjusted_junction_leak: float | None = None
            junctions: list[Junction] = []
            pipes: list[Pipe] = []

            time_step = row['time_step']
            adjusted_junction_id = row['adjusted_junction_id']
            adjusted_junction_emit = row['adjusted_junction_emit']
            adjusted_junction_leak = row['adjusted_junction_leak']

            for attr_key in row:
                if str(attr_key).startswith('pipe_') and str(attr_key).endswith('_flow'):
                    underscore_separated = str(attr_key).split('_')
                    pipe_id = underscore_separated[1]
                    pipes.append(
                        Pipe(
                            id=pipe_id,
                            delta_flow=row[attr_key]
                        )
                    )

            session_result.results.append(
                MadaniResult(
                    custom_inp_file='',
                    time_step=time_step,
                    adjusted_junction_id=adjusted_junction_id,
                    adjusted_junction_emit=adjusted_junction_emit,
                    adjusted_junction_leak=adjusted_junction_leak,
                    junctions=junctions,
                    pipes=pipes
                )
            )

        return session_result
