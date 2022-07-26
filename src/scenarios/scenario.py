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

    def _on_post_simulate(self):
        """
        Do something after simulation
        e.g. write the result to DB
        """
        pass

    def run(self):
        self._on_arrange()
        self._on_simulate()
        self._on_post_simulate()
