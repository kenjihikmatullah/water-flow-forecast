class LeakLocalizationRecord:
    def __init__(self, actual_leaking: str, time_step_of_prediction: str, prediction: str):
        self.actual_leaking = actual_leaking
        self.time_step_of_prediction = time_step_of_prediction
        self.prediction = prediction
