from dataclasses import dataclass

from models.inp_metadata import InpMetadata
from scenario_data.scenario_data import ScenarioData
from utils.impl.inp_metadata_creator_impl import InpMetadataCreatorImpl


@dataclass
class MadaniScenarioData(ScenarioData):

    default_demand_based_on_sensors = 0.5
    """
    Real demand (not simulation) of junction in LPS 
    
    Later on, this value should be described
    - specifically for each junction
    - real-time based on data from sensors in the area
    """
