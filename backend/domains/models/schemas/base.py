from typing import Literal

IntensityLevel = Literal[
    "low",
    "medium",
    "high",
]

RiskLevel = Literal[
    "low",
    "medium",
    "high",
]

ConfidenceLevel = Literal[
    "low",
    "medium",
    "high",
]

ImpactDirection = Literal[
    "positive",
    "neutral",
    "negative",
]


DeviceType = Literal[
    "Laptop",
    "Smartphone",
    "Tablet",
    "Desktop",
]

ScenarioScope = Literal[
    "einzelne_interaktion",
    "mehrstufiger_prozess",
    "formularprozess",
    "navigationsaufgabe",
    "informationssuche",
    "vergleichsaufgabe",
    "unbekannt",
]

MetricType = Literal[
    "time",
    "count",
    "score",
    "probability",
    "state",
    "category",
]

AggregationType = Literal[
    "sum",
    "average",
    "minimum",
    "maximum",
    "last_value",
    "distribution",
    "none",
]

MetricSource = Literal[
    "task_model",
    "user_model",
    "environment_model",
    "computed_parameters",
    "simulation",
]

PriorityLevel = Literal[
    "low",
    "medium",
    "high",
]
