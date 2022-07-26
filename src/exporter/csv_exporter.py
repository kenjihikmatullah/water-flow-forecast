class CsvExporter:

    def _initialize(self, path: str):
        """
        :param path: path of csv file which data is exported to
        """
        self.path = path
        self.__open_output_file()

    def __open_output_file(self):
        # TODO: Programmatically create directory which doesn't exist
        self.output_file = open(self.path, 'w')

    def _write_row(self, row: list[str]):
        self.output_file.write(",".join(row) + '\n')

    def close(self):
        self.output_file.close()
