import csv

from db_client.maria_db_client import MariaDbClient
from models.leak_localization_record import LeakLocalizationRecord


class LeakLocalizationRepository:

    DATABASE_NAME = 'leak_detection'
    TABLE_NAME = 'leak_localization'

    def __init__(self):
        self.db_client = MariaDbClient()

    def create_table(self):
        statement = """
            CREATE TABLE `leak_localization` (
                `localization_session_id` VARCHAR(32) NOT NULL,
                `simulation_session_id` VARCHAR(32) NOT NULL,                
                `actual_leaking` VARCHAR(32) NOT NULL COMMENT 'ID of actual leaking junction',
                `time_step_of_prediction` VARCHAR(32) NOT NULL COMMENT 'Time step which prediction is based on',
                `prediction` VARCHAR(32) NOT NULL COMMENT 'ID of predicted leaking junction'
            )
            COMMENT='Leak localization data comparing actual and predicted leaking junction'
            COLLATE='utf8mb4_general_ci'
        """

        self.db_client.execute(statement)
        self.db_client.connection.close()

    def store(self, record: LeakLocalizationRecord):
        statement = f'INSERT INTO leak_localization(localization_session_id, simulation_session_id, actual_leaking, time_step_of_prediction, prediction, method) VALUES (?, ?, ?, ?, ?, ?)'

        self.db_client.execute(statement, [record.localization_session_id, record.simulation_session_id, record.actual_leaking, record.time_step_of_prediction, record.prediction, record.method])

    def export_db_to_csv(self, localization_session_id: str, filename: str):
        statement = """
            SELECT actual_leaking
                , MAX(CASE WHEN time_step_of_prediction = 'SUNDAY' THEN prediction END) AS sunday_prediction
                , MAX(CASE WHEN time_step_of_prediction = 'MONDAY' THEN prediction END) AS monday_prediction
                , MAX(CASE WHEN time_step_of_prediction = 'TUESDAY' THEN prediction END) AS tuesday_prediction
                , MAX(CASE WHEN time_step_of_prediction = 'WEDNESDAY' THEN prediction END) AS wednesday_prediction
                , MAX(CASE WHEN time_step_of_prediction = 'THURSDAY' THEN prediction END) AS thursday_prediction
                , MAX(CASE WHEN time_step_of_prediction = 'FRIDAY' THEN prediction END) AS friday_prediction
                , MAX(CASE WHEN time_step_of_prediction = 'SATURDAY' THEN prediction END) AS saturday_prediction
            FROM leak_localization
            WHERE localization_session_id = ?
            GROUP BY actual_leaking
        """

        self.db_client.execute(statement, [localization_session_id])
        print("Extracting result from DB...")

        results = self.db_client.cursor.fetchall()

        COLUMN_ACTUAL_LEAKING = 0

        percentage_total = 0

        # Iterate through location cases
        for i in range(0, len(results)):
            count = 0

            # Iterate through all time step tables
            for j in range(1, 8):
                if results[i][j] == results[i][COLUMN_ACTUAL_LEAKING]:
                    count += 1

            percentage = round(count / 7, 2)
            percentage_total += percentage
            results[i] = results[i] + (count, percentage)

        average_percentage = percentage_total / len(results)
        print(results)
        column_names = [i[0] for i in self.db_client.cursor.description] + ['correct_count', 'correct_percentage']
        fp = open(filename, 'w')
        file = csv.writer(fp, lineterminator='\n')
        file.writerow(column_names)
        file.writerows(results)
        file.writerow([average_percentage])
        fp.close()

        self.db_client.connection.close()
