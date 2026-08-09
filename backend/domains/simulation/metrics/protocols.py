from typing import Protocol, runtime_checkable


@runtime_checkable
class SimulationMetric(Protocol):
    metric_id: str

    def calculate(self, **kwargs):
        ...
