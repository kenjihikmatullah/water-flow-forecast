from dataclasses import dataclass

from scenario_data.scenario_data import ScenarioData


@dataclass
class AndalusScenarioData(ScenarioData):
    default_leak_to_simulate = 0.5
    """
    Leak to simulate on each junction for all time steps in LPS
    
    Later on, this value should be described according to business needs, field conditions, and historical data
    """
