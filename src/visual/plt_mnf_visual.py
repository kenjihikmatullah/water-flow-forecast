import subprocess

from models.simulator import Simulator
import matplotlib.pyplot as plt

from scenario_data.andalus_scenario_data import AndalusScenarioData
from utils import out_util


class PltMnfVisual:
    def __init__(self, data: AndalusScenarioData):
        self.data = data

    def visualize(self):
        pipe_id_map_to_flows: dict[str, list[float]] = {}

        for time_step in self.data.time_steps:
            """Simulate on each time step"""

            # Simulate no leak
            subprocess.call(["java", "-cp", Simulator.JAR_FILE, "org.addition.epanet.EPATool",
                             self.data.initial_inp_file])

            pipes_when_no_leak = out_util.get_pipes(inp_file=self.data.initial_inp_file, time_step=time_step)
            for p in pipes_when_no_leak:
                p.base_flow = p.flow

            pipes_when_no_leak.sort(key=lambda p: int(p.id))
            for pipe in pipes_when_no_leak:
                if pipe.id in pipe_id_map_to_flows.keys():
                    pipe_id_map_to_flows.get(pipe.id).append(pipe.base_flow)

                else:
                    pipe_id_map_to_flows[pipe.id] = [pipe.base_flow]


        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for pipe_id in pipe_id_map_to_flows.keys():
            # if pipe_id != '13':
            #     continue

            plt.plot(days, pipe_id_map_to_flows.get(pipe_id))
            plt.title(f'MNF of Pipe {pipe_id}')
            plt.xlabel('Day')
            plt.ylabel('Flow (LPS)')
            plt.savefig(f'C:\\Users\\kenji\\OneDrive - Institut Teknologi Sepuluh Nopember\\Thesis\\Progress\\22_oct\\mnf_pipe_{pipe_id}.png')
            plt.show()
