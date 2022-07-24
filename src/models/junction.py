from dataclasses import dataclass


@dataclass
class Junction:
    id: str

    base_demand: float = 0

    actual_demand: float = 0
    """
    base demand combined with leak and demand multiply,
    based on simulation.
    
    Later on, this will be compared with actual demand
    based on data from sensors in the area.
    """

    emit: float = 0
    """emitter coefficient, represents leakage rate"""

    pattern: str = None
