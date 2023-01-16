class LeakLocalizationRecord:
    def __init__(self, localization_session_id: str, simulation_session_id: str, actual_leaking: str, time_step_of_prediction: str, prediction: str, method: str):
        self.localization_session_id = localization_session_id
        self.simulation_session_id = simulation_session_id
        self.actual_leaking = actual_leaking
        self.time_step_of_prediction = time_step_of_prediction
        self.prediction = prediction
        self.method = method
