from dataclasses import dataclass


@dataclass
class Pipe:
    id: str
    flow: float | None = None
    base_flow: float | None = None  # Flow when no leak

    delta_flow: float | None = None

    def get_delta_flow(self):
        if self.delta_flow is not None:
            return self.delta_flow

        if self.flow is None or self.base_flow is None:
            return None

        return self.flow - self.base_flow
