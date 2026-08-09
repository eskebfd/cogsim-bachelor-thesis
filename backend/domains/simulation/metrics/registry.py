from backend.domains.simulation.metrics.protocols import SimulationMetric


class SimulationMetricRegistry:
    def __init__(self) -> None:
        self._metrics: dict[str, SimulationMetric] = {}
        self._aliases: dict[str, str] = {}

    def register(self, metric: SimulationMetric) -> None:
        if metric.metric_id in self._metrics:
            raise ValueError(f"Simulation metric already registered: {metric.metric_id}")
        self._metrics[metric.metric_id] = metric

    def get(self, metric_id: str) -> SimulationMetric:
        metric_id = self._aliases.get(metric_id, metric_id)
        try:
            return self._metrics[metric_id]
        except KeyError as exc:
            raise ValueError(f"Unknown simulation metric ID: {metric_id}") from exc

    def list_ids(self) -> list[str]:
        return list(self._metrics)

    def register_alias(self, legacy_metric_id: str, canonical_metric_id: str) -> None:
        if legacy_metric_id in self._metrics:
            raise ValueError(f"Simulation metric already registered: {legacy_metric_id}")
        if canonical_metric_id not in self._metrics:
            raise ValueError(f"Unknown canonical simulation metric ID: {canonical_metric_id}")
        self._aliases[legacy_metric_id] = canonical_metric_id


METRIC_REGISTRY = SimulationMetricRegistry()


def register_metric(
    metric: SimulationMetric,
    registry: SimulationMetricRegistry = METRIC_REGISTRY,
) -> None:
    registry.register(metric)


def get_metric(
    metric_id: str,
    registry: SimulationMetricRegistry = METRIC_REGISTRY,
) -> SimulationMetric:
    return registry.get(metric_id)


def calculate_metric(metric_id: str, **kwargs):
    return get_metric(metric_id).calculate(**kwargs)
