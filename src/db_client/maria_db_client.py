import mariadb


class MariaDbClient:
    __DATABASE_NAME = 'leak_detection'

    def __init__(self):
        try:
            self.connection = mariadb.connect(
                user="root",
                password="",
                host="localhost",
                port=3306,
                database="leak_detection"
            )
            self.cursor = self.connection.cursor()

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB: {e}")

    def execute(self, statement, data):
        try:
            self.cursor.execute(statement, data)

            # self.__cursor.execute("INSERT INTO table_test(name) VALUES(?)", ["amir"])
            self.connection.commit()

        except mariadb.Error as e:
            print(f"Error executing SQL statement: {e}")

    def create_database(self):
        statement = 'CREATE DATABASE `leak_detection`'
        self.cursor.execute(statement)
