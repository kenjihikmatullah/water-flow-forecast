from db_client.mongo_db_client import MongoDbClient
from models.junction import Junction
from models.pipe import Pipe
from models.simulation_result import SimulationResult
from models.simulation_session import SimulationSession


class MadaniMongoDbExporter:

    def __init__(self):
        self.db_client = MongoDbClient()

    def map_junction_to_dict(self, junction: Junction) -> dict:
        return {
            'id': junction.id,
            'base_demand': junction.base_demand,
            'actual_demand': junction.actual_demand,
            'emit': junction.emit,
            'pattern': junction.pattern
        }

    def map_pipe_to_dict(self, pipe: Pipe) -> dict:
        return {
            'id': pipe.id,
            'flow': pipe.flow
        }

    def map_result_to_dict(self, result: SimulationResult):
        return {
            'session_id': None,  # TODO: Generate dynamically
            'time_step': result.time_step,
            'adjusted_junction_id': result.leaking_junction_id,
            'emit': result.leaking_junction_emit,
            'junctions': list(map(self.map_junction_to_dict, result.junctions)),
            'pipes': list(map(self.map_pipe_to_dict, result.pipes))
        }

    def export(self, session_result: SimulationSession):
        documents = list(map(self.map_result_to_dict, session_result.cases))
        self.db_client.insert('simulation_results', documents)
