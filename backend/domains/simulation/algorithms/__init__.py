from backend.domains.simulation.algorithms.attention.linear import (
    AttentionDecayAlgorithm,
    AttentionUpdateAlgorithm,
)
from backend.domains.simulation.algorithms.cognitive_load.weighted_sum import (
    CognitiveLoadAlgorithm,
)
from backend.domains.simulation.algorithms.completion_time.default import (
    EstimatedCompletionTimeAlgorithm,
)
from backend.domains.simulation.algorithms.error_risk.weighted_sum import (
    ErrorRiskAlgorithm,
)
from backend.domains.simulation.algorithms.fatigue.linear import (
    FatigueTargetAlgorithm,
    FatigueUpdateAlgorithm,
    LinearTransitionAlgorithm,
)
from backend.domains.simulation.algorithms.progress.slowdown import (
    TaskProgressSlowdownAlgorithm,
)
from backend.domains.simulation.algorithms.reading.default import (
    ReadingSpeedAlgorithm,
    ReadingSpeedUpdateAlgorithm,
)
from backend.domains.simulation.algorithms.registry import (
    ALGORITHM_REGISTRY,
    register_algorithm,
)


for _algorithm in (
    AttentionDecayAlgorithm(),
    AttentionUpdateAlgorithm(),
    FatigueTargetAlgorithm(),
    LinearTransitionAlgorithm(),
    FatigueUpdateAlgorithm(),
    ReadingSpeedAlgorithm(),
    ReadingSpeedUpdateAlgorithm(),
    TaskProgressSlowdownAlgorithm(),
    CognitiveLoadAlgorithm(),
    ErrorRiskAlgorithm(),
    EstimatedCompletionTimeAlgorithm(),
):
    register_algorithm(_algorithm)


__all__ = ["ALGORITHM_REGISTRY"]
