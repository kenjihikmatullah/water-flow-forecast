import mariadb


class MariaDbClient:
    __DATABASE_NAME = 'leak_detection'
    __TABLE_NAME = 'simulation_results'

    def __init__(self):
        try:
            self.connection = mariadb.connect(
                user="root",
                password="",
                host="localhost",
                port=3306,
                database="leak_detection"
            )
            self.__cursor = self.connection.cursor()

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB: {e}")

    def execute(self, statement, data):
        try:
            self.__cursor.execute(statement, data)

            # self.__cursor.execute("INSERT INTO table_test(name) VALUES(?)", ["amir"])
            self.connection.commit()

        except mariadb.Error as e:
            print(f"Error executing SQL statement: {e}")

    def create_database(self):
        statement = 'CREATE DATABASE `leak_detection`'
        self.__cursor.execute(statement)

    def create_table(self, pipe_ids: list[str]):
        pipe_flow_columns = ""
        for i, pipe_id in enumerate(pipe_ids):
            pipe_flow_columns += f"`pipe_{pipe_id}_flow` FLOAT NOT NULL"
            if i < len(pipe_ids) - 1:
                pipe_flow_columns += ','

        statement = """
            CREATE TABLE `simulation_results` (
                `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                `time_step` VARCHAR(32) NOT NULL,
                `adjusted_junction_id` VARCHAR(32) NULL,
                `adjusted_junction_emit` FLOAT NULL,
                `adjusted_junction_leak` FLOAT NULL COMMENT 'actual demand - (base demand * demand multiplier)',
                """ + pipe_flow_columns
        statement += """,
                PRIMARY KEY (`id`)
            )
            COMMENT='All junction demands and pipe flows are in LPS'
            COLLATE='utf8mb4_general_ci'
        """

        self.__cursor.execute(statement)
