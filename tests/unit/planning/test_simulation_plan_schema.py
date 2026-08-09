import pytest
from pydantic import ValidationError

from backend.domains.planning.schemas.simulation_plan import (
    ComputationModelInstance,
    SimulationPlanSchema,
)


def minimal_plan_payload() -> dict:
    return {
        "selected_user_profiles": [
            {
                "profile_id": "generic",
                "label": "Generisch",
                "is_baseline": True,
            }
        ],
        "evaluation_metrics": [
            {
                "metric_id": "completion_efficiency",
                "name": "Bearbeitungseffizienz",
                "description": "Bewertet die Effizienz des Aufgabenabschlusses.",
                "metric_type": "score",
                "source": "predefined",
            }
        ],
        "simulation_settings": {
            "time_step_seconds": 1,
            "max_duration_seconds": 300,
        },
    }


def test_minimal_simulation_plan_can_be_validated():
    plan = SimulationPlanSchema.model_validate(minimal_plan_payload())

    assert plan.selected_user_profiles[0].is_baseline is True
    assert plan.simulation_settings.max_duration_seconds == 300
    assert plan.required_attributes == []
    assert plan.computation_models == []


def test_simulation_plan_supports_multiple_user_profiles():
    payload = minimal_plan_payload()
    payload["selected_user_profiles"].append(
        {
            "profile_id": "adhd",
            "label": "ADHS",
            "is_baseline": False,
        }
    )

    plan = SimulationPlanSchema.model_validate(payload)

    assert [profile.profile_id for profile in plan.selected_user_profiles] == [
        "generic",
        "adhd",
    ]


def test_simulation_plan_supports_custom_metrics():
    payload = minimal_plan_payload()
    payload["evaluation_metrics"].append(
        {
            "metric_id": "notification_recovery_time",
            "name": "Erholungszeit nach Benachrichtigung",
            "description": "Misst die Zeit bis zur erneuten Aufgabenbearbeitung.",
            "metric_type": "time",
            "source": "custom",
            "analysis_question": "Wie schnell wird die Aufgabe fortgesetzt?",
        }
    )

    plan = SimulationPlanSchema.model_validate(payload)

    assert plan.evaluation_metrics[1].source == "custom"
    assert plan.evaluation_metrics[1].analysis_question is not None


@pytest.mark.parametrize("model_type", ["weighted_sum", "ratio"])
def test_supported_computation_model_types(model_type: str):
    model = ComputationModelInstance.model_validate(
        {
            "model_id": f"test_{model_type}",
            "name": "Testmodell",
            "model_type": model_type,
            "inputs": ["input_a", "input_b"],
            "output": "result",
            "weights": {"input_a": 0.5, "input_b": 0.5},
        }
    )

    assert model.model_type == model_type


def test_invalid_computation_model_type_is_rejected():
    with pytest.raises(ValidationError):
        ComputationModelInstance.model_validate(
            {
                "model_id": "invalid_model",
                "name": "Ungültiges Modell",
                "model_type": "neural_network",
                "inputs": ["input_a"],
                "output": "result",
            }
        )
