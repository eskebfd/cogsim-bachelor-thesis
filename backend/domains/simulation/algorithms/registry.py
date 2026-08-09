from backend.domains.simulation.algorithms.protocols import SimulationAlgorithm


class SimulationAlgorithmRegistry:
    def __init__(self) -> None:
        self._algorithms: dict[str, SimulationAlgorithm] = {}

    def register(self, algorithm: SimulationAlgorithm) -> None:
        if algorithm.algorithm_id in self._algorithms:
            raise ValueError(
                f"Simulation algorithm already registered: {algorithm.algorithm_id}"
            )
        self._algorithms[algorithm.algorithm_id] = algorithm

    def get(self, algorithm_id: str) -> SimulationAlgorithm:
        try:
            return self._algorithms[algorithm_id]
        except KeyError as exc:
            raise ValueError(f"Unknown simulation algorithm ID: {algorithm_id}") from exc

    def list_ids(self) -> list[str]:
        return list(self._algorithms)


ALGORITHM_REGISTRY = SimulationAlgorithmRegistry()


def register_algorithm(
    algorithm: SimulationAlgorithm,
    registry: SimulationAlgorithmRegistry = ALGORITHM_REGISTRY,
) -> None:
    registry.register(algorithm)


def get_algorithm(
    algorithm_id: str,
    registry: SimulationAlgorithmRegistry = ALGORITHM_REGISTRY,
) -> SimulationAlgorithm:
    return registry.get(algorithm_id)


def calculate_with_algorithm(algorithm_id: str, **kwargs):
    return get_algorithm(algorithm_id).calculate(**kwargs)
