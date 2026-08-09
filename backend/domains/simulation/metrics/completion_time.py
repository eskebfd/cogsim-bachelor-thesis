class CompletionTimeMetric:
    metric_id = "completion_time"

    def calculate(self, *, timeline: list[dict]) -> float:
        return timeline[-1]["timestamp_seconds"] if timeline else 0
