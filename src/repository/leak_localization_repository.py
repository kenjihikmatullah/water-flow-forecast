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
        statement = f'INSERT INTO leak_localization(session_id, actual_leaking, time_step_of_prediction, prediction) VALUES (?, ?, ?, ?)'

        self.db_client.execute(statement, [record.session_id, record.actual_leaking, record.time_step_of_prediction, record.prediction])
        self.db_client.connection.close()

    def export_db_to_csv(self):
        statement = """
            SELECT actual_leaking
                , MAX(CASE WHEN time_step_of_prediction = 'SUNDAY' THEN prediction END) AS sunday_prediction
                , MAX(CASE WHEN time_step_of_prediction = 'MONDAY' THEN prediction END) AS monday_prediction
                , MAX(CASE WHEN time_step_of_prediction = 'TUESDAY' THEN prediction END) AS tuesday_prediction
                , MAX(CASE WHEN time_step_of_prediction = 'WEDNESDAY' THEN prediction END) AS wednesdey_prediction
                , MAX(CASE WHEN time_step_of_prediction = 'THURSDAY' THEN prediction END) AS thursday_prediction
                , MAX(CASE WHEN time_step_of_prediction = 'FRIDAY' THEN prediction END) AS friday_prediction
                , MAX(CASE WHEN time_step_of_prediction = 'SATURDAY' THEN prediction END) AS saturday_prediction
            FROM leak_localization
            GROUP BY actual_leaking
        """

        self.db_client.execute(statement, [])
        print("Extracting result from DB...")

        results = self.db_client.cursor.fetchall()

        COLUMN_ACTUAL_LEAKING = 0

        for i in range(0, len(results)):
            count = 0
            for j in range(1, 8):
                if results[i][j] == results[i][COLUMN_ACTUAL_LEAKING]:
                    count += 1

            percentage = round(count / 7, 2)
            results[i] = results[i] + (count, percentage)

        print(results)
        column_names = [i[0] for i in self.db_client.cursor.description] + ['correct_count', 'correct_percentage']
        fp = open('leak_localization_confidence_level.csv', 'w')
        file = csv.writer(fp, lineterminator='\n')
        file.writerow(column_names)
        file.writerows(results)
        fp.close()

        self.db_client.connection.close()
