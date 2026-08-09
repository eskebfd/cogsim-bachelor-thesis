from collections.abc import Sequence


def normalize_weights(
    weights: Sequence[float] | None,
    factor_count: int | None = None,
    decimals: int = 4,
) -> list[float]:
    """
    Normalisiert Gewichtungen für lineare Modelle.

    Negative oder ungültige Werte werden verworfen. Falls keine gültigen
    Gewichtungen vorhanden sind, werden gleich verteilte Gewichte erzeugt.
    Die Summe der zurückgegebenen Gewichte beträgt exakt 1.
    """

    try:
        source = list(weights or [])
    except TypeError:
        source = []


    count = factor_count or len(source) or 3

    if count <= 0:
        raise ValueError("factor_count must be greater than zero")

    values = []


    for value in source[:count]:
        try:
            values.append(max(0.0, float(value)))
        except (TypeError, ValueError):
            values.append(0.0)


    values.extend(0.0 for _ in range(count - len(values)))

    total = sum(values)


    if total <= 0:
        values = [1 / count for _ in range(count)]
    else:
        values = [value / total for value in values]


    normalized = [round(value, decimals) for value in values[:-1]]


    final_weight = round(1.0 - sum(normalized), decimals)


    if final_weight < 0:
        normalized = [round(value, 8) for value in values[:-1]]
        final_weight = round(1.0 - sum(normalized), 8)

    normalized.append(final_weight)


    normalized[-1] += 1.0 - sum(normalized)

    return normalized
