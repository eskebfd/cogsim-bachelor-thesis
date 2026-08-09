from backend.domains.simulation.events.protocols import SimulationEventDefinition


class SimulationEventRegistry:
    def __init__(self) -> None:
        self._events: dict[str, SimulationEventDefinition] = {}

    def register(self, event: SimulationEventDefinition) -> None:
        if event.event_type in self._events:
            raise ValueError(f"Simulation event already registered: {event.event_type}")
        self._events[event.event_type] = event

    def get(self, event_type: str) -> SimulationEventDefinition:
        try:
            return self._events[event_type]
        except KeyError as exc:
            raise ValueError(f"Unknown simulation event type: {event_type}") from exc

    def list_events(self) -> list[SimulationEventDefinition]:
        return list(self._events.values())

    def list_types(self) -> list[str]:
        return list(self._events)


EVENT_REGISTRY = SimulationEventRegistry()


def register_event(
    event: SimulationEventDefinition,
    registry: SimulationEventRegistry = EVENT_REGISTRY,
) -> None:
    registry.register(event)


def get_event(
    event_type: str,
    registry: SimulationEventRegistry = EVENT_REGISTRY,
) -> SimulationEventDefinition:
    return registry.get(event_type)
