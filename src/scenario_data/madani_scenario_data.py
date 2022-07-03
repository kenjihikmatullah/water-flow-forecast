from dataclasses import dataclass


@dataclass
class MadaniScenarioData:
    output_dir: str
    number_of_pipes: int
    initial_inp_file: str
    junction_ids: list[int]
