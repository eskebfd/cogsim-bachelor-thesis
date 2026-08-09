import math


class EstimatedCompletionTimeAlgorithm:
    algorithm_id = "completion_time.estimated_duration"

    def calculate(self, *, required_work: float, progress_rate: float) -> int:
        return math.ceil(required_work / progress_rate)
