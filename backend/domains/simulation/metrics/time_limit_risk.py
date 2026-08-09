class TimeLimitRiskMetric:
    metric_id = "time_limit_risk"

    def calculate(
        self,
        *,
        completion_time: float,
        time_limit_seconds: float | None,
    ) -> float:
        if not time_limit_seconds or time_limit_seconds <= 0:
            return 0.0
        return round(
            min(
                100.0,
                max(0.0, completion_time - time_limit_seconds)
                / time_limit_seconds
                * 100,
            ),
            2,
        )
