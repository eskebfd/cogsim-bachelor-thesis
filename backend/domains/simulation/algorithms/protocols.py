from typing import Protocol, runtime_checkable


@runtime_checkable
class SimulationAlgorithm(Protocol):
    algorithm_id: str

    def calculate(self, **kwargs):
        ...
