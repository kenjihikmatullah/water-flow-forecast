class LeakLocalizationRecord:
    def __init__(self, session_id: str, actual_leaking: str, time_step_of_prediction: str, prediction: str):
        self.session_id = session_id
        self.actual_leaking = actual_leaking
        self.time_step_of_prediction = time_step_of_prediction
        self.prediction = prediction
