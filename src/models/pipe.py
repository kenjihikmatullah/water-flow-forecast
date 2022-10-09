from dataclasses import dataclass


@dataclass
class Pipe:
    id: str
    flow: float | None = None
    base_flow: float | None = None  # Flow when no leak

    @property
    def delta_flow(self):
        if self.flow is None or self.base_flow is None:
            return None

        return self.flow - self.base_flow
