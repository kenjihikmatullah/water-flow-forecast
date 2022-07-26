from dataclasses import dataclass


@dataclass
class Pipe:
    id: str
    flow: float | None = None
