from dataclasses import dataclass


@dataclass
class Junction:
    id: str
    elevation: float = 0
    demand: float = 0
    pattern: str = None
