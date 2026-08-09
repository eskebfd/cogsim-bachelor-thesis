from numbers import Real
from typing import Any


class ModelAttributeError(ValueError):
    pass


def numeric_attribute_value(
    model: dict,
    attribute: str,
    *,
    default: float | None = None,
) -> float:
    raw_value: Any = model.get(attribute)

    if isinstance(raw_value, dict):
        raw_value = raw_value.get("value")
    elif hasattr(raw_value, "value"):
        raw_value = raw_value.value

    if isinstance(raw_value, Real) and not isinstance(raw_value, bool):
        return max(0.0, min(100.0, float(raw_value)))

    if default is not None:
        return max(0.0, min(100.0, float(default)))

    raise ModelAttributeError(
        f"Required numeric attribute '{attribute}' is missing or has no numeric value."
    )
