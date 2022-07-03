from abc import abstractmethod


class Scenario:

    def _on_arrange(self):
        """
        Do arrangement before simulation
        e.g. create output folder
        """
        pass

    @abstractmethod
    def _on_simulate(self):
        """
        Do simulation to get output
        e.g. simulate leak by setting emitter coefficient on each junction to get WDS state when leak occurs
        """
        pass

    def _on_clean_up(self):
        """
        Do clean-up after simulation
        e.g. clear temporary files generated during simulation
        """
        pass

    def run(self):
        self._on_arrange()
        self._on_simulate()
        self._on_clean_up()
