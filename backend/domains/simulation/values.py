from collections.abc import Sequence
import math
from typing import Any


def clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    """
    Begrenzt einen numerischen Wert auf einen definierten Wertebereich.
    Standardmäßig wird auf die Skala von 0 bis 100 begrenzt.
    """
    return max(minimum, min(maximum, float(value)))


def attribute_value(model: dict, attribute: str, default: float = 0.0) -> float:
    """
    Liest den numerischen Wert eines Modellattributs aus.

    Unterstützt sowohl Attribute als einfache Zahlen als auch
    Attribute im Schemaformat {"value": ...}. Ungültige Werte
    werden durch den Default-Wert ersetzt.
    """
    raw_value: Any = model.get(attribute, default)

    if isinstance(raw_value, dict):
        raw_value = raw_value.get("value", default)

    try:
        return clamp(float(raw_value))
    except (TypeError, ValueError):
        return clamp(default)


def parameter_value(model: dict, parameter: str, default: float = 0.0) -> float:
    """
    Liest einen berechneten Parameter aus einem Parameter-Dictionary.
    Verwendet dieselbe Logik wie attribute_value().
    """
    return attribute_value(model, parameter, default)


def rounded(value: float) -> float:
    """
    Begrenzt einen Wert auf den gültigen Bereich und rundet
    ihn auf zwei Nachkommastellen.
    """
    return round(clamp(value), 2)


def equal_weights(factor_count: int) -> tuple[float, ...]:
    """
    Erzeugt gleich verteilte Gewichtungen für eine beliebige
    Anzahl von Einflussfaktoren.
    """
    if factor_count <= 0:
        raise ValueError("factor_count must be greater than zero")

    weight = 1 / factor_count
    return tuple(weight for _ in range(factor_count))


def validated_weights(
    weights: Sequence[float] | None,
    factor_count: int,
) -> tuple[float, ...]:
    """
    Validiert Gewichtungen für lineare Modelle.

    Falls keine Gewichtungen angegeben sind, werden automatisch
    gleich verteilte Gewichte verwendet.
    """
    resolved = tuple(weights) if weights is not None else equal_weights(factor_count)


    if len(resolved) != factor_count:
        raise ValueError(f"Expected {factor_count} weights, received {len(resolved)}")


    if any(weight < 0 for weight in resolved):
        raise ValueError("Model weights must not be negative")


    if not math.isclose(sum(resolved), 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError("Model weights must sum to 1")

    return resolved


def weighted_sum(
    factors: Sequence[float],
    weights: Sequence[float] | None = None,
) -> float:
    """
    Berechnet die gewichtete Summe mehrerer Einflussfaktoren.

    Diese Funktion bildet die Grundlage aller linearen Modelle
    innerhalb der Simulation.
    """
    resolved_weights = validated_weights(weights, len(factors))

    return rounded(
        sum(weight * factor for weight, factor in zip(resolved_weights, factors))
    )
