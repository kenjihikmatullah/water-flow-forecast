import matplotlib.pyplot as plt

from db_client.maria_db_client import MariaDbClient


class HasilSimulasi1:

    def __init__(self):
        self.db_client = MariaDbClient()

    def fetch(self):
        statement = """
            SELECT *
            FROM simulation_results sr
            JOIN simulation_pipe_flow spf ON spf.result_id = sr.id
            WHERE spf.pipe_id = ? AND sr.time_step = ?
        """

        self.db_client.execute(statement, ['1', '01:00:00'])
        print("Extracting result from DB...")

        return self.db_client.cursor.fetchall()

    def visualize(self):
        data = self.fetch()

        cases = ['Normal']
        for d in data:
            if d[3] is not None:
                cases.append('J' + d[3])

        flows = list(map(lambda row: row[8], data))

        plt.plot(cases, flows)
        plt.title('Arus Pipa 1 di Berbagai Kasus')
        plt.xlabel('Kasus')
        plt.ylabel('Arus Air (LPS)')
        plt.savefig(
            f'C:\\Users\\kenji\\OneDrive - Institut Teknologi Sepuluh Nopember\\Thesis\\Buku TA\\pipe_1_flow.png')
        plt.show()