from dataclasses import dataclass

from scenario_data.scenario_data import ScenarioData


@dataclass
class MadaniScenarioData(ScenarioData):

    default_demand_based_on_sensors = 0.5
    """
    Real demand (not simulation) of junction in LPS 
    
    Later on, this value should be described
    - specifically for each junction
    - real-time based on data from sensors in the area
    """
