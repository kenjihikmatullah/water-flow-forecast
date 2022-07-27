from db_client.mongo_db_client import MongoDbClient
from models.junction import Junction
from models.pipe import Pipe
from result.madani.madani_result import MadaniResult
from result.madani.madani_session_result import MadaniSessionResult


class MadaniDbExporter:

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

    def map_result_to_dict(self, result: MadaniResult):
        return {
            'time_step': result.time_step,
            'adjusted_junction_id': result.adjusted_junction_id,
            'emit': result.emit,
            'junctions': list(map(self.map_junction_to_dict, result.junctions)),
            'pipes': list(map(self.map_pipe_to_dict, result.pipes))
        }

    def export(self, session_result: MadaniSessionResult):
        documents = list(map(self.map_result_to_dict, session_result.results))
        self.db_client.insert('simulation_results', documents)
