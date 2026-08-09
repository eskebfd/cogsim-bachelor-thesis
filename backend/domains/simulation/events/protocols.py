from typing import Protocol, runtime_checkable

from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.schemas.types import ResultMetrics, UserState


@runtime_checkable
class SimulationEventDefinition(Protocol):
    event_type: str

    def condition(
        self,
        *,
        user_state: UserState,
        metrics: ResultMetrics,
        config: SimulationConfig,
        context: dict,
    ) -> dict:
        ...

    def effect(
        self,
        *,
        task_step: dict,
        config: SimulationConfig,
    ) -> dict[str, float | int]:
        ...
