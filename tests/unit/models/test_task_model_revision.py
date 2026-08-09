from backend.domains.models.services.task_model_revision import (
    derive_task_attribute_values,
    merge_task_model_revision,
)
from backend.domains.models.services import generation as generation_service
from backend.workflow.nodes import model_nodes


def attribute(value: int) -> dict:
    return {
        "value": value,
        "scale_min_description": "niedrig",
        "scale_max_description": "hoch",
        "explanation": "Testwert",
        "confidence": "high",
    }


def step(
    name: str,
    *,
    step_id: str = "step_1",
    step_type: str = "read",
    duration: float = 10,
) -> dict:
    return {
        "step_id": step_id,
        "name": name,
        "goal": f"{name} erledigen",
        "step_type": step_type,
        "description": f"{name} durchführen",
        "goms_operations": ["perceive", "think"],
        "operation_time_estimates": [
            {
                "operation": "perceive",
                "estimated_duration_seconds": duration / 2,
                "cognitive_requirement": "wahrnehmen",
            },
            {
                "operation": "think",
                "estimated_duration_seconds": duration / 2,
                "cognitive_requirement": "verarbeiten",
            },
        ],
        "cognitive_requirements": ["verstehen"],
        "estimated_duration_seconds": duration,
    }


def task_model(names: list[str]) -> dict:
    steps = [
        step(
            name,
            step_id=f"step_{index}",
            step_type="input" if name in {"D", "E"} else "read",
            duration=20 if name in {"D", "E"} else 10,
        )
        for index, name in enumerate(names, start=1)
    ]
    return {
        "task_name": "Testaufgabe",
        "task_goal": "Testziel",
        "task_complexity": attribute(30),
        "number_of_steps": attribute(len(steps)),
        "reading_demand": attribute(30),
        "input_demand": attribute(20),
        "memory_demand": attribute(20),
        "decision_demand": attribute(20),
        "error_criticality": attribute(10),
        "steps": steps,
        "assumptions": [],
    }


def test_task_revision_adds_one_step_and_updates_step_count():
    current = task_model(["A", "B", "C"])
    revised = task_model(["A", "B", "C", "D"])

    result = merge_task_model_revision(current, revised)

    assert [step["name"] for step in result["steps"]] == ["A", "B", "C", "D"]
    added_step = result["steps"][3]
    assert added_step["goms_operations"]
    assert added_step["operation_time_estimates"]
    assert added_step["estimated_duration_seconds"] > 0
    assert result["number_of_steps"]["value"] == 4


def test_task_revision_adds_steps_cumulatively():
    first = merge_task_model_revision(
        task_model(["A", "B", "C"]),
        task_model(["A", "B", "C", "D"]),
    )
    second = merge_task_model_revision(
        first,
        task_model(["A", "B", "C", "E"]),
    )

    assert [step["name"] for step in second["steps"]] == [
        "A",
        "B",
        "C",
        "E",
        "D",
    ]
    assert "D" in [step["name"] for step in second["steps"]]
    assert second["number_of_steps"]["value"] == 5


def test_task_revision_updates_dependent_task_attributes():
    current = task_model(["A", "B", "C"])
    revised = task_model(["A", "B", "C", "D"])
    revised["steps"][3]["step_type"] = "input"
    revised["steps"][3]["description"] = (
        "Pflichtfelder ausfüllen und kritische Eingaben prüfen"
    )
    revised["steps"][3]["cognitive_requirements"] = [
        "eingeben",
        "prüfen",
        "erinnern",
    ]

    before = derive_task_attribute_values(current)
    result = merge_task_model_revision(current, revised)

    assert result["number_of_steps"]["value"] == 4
    assert result["task_complexity"]["value"] != before["task_complexity"]
    assert result["input_demand"]["value"] >= before["input_demand"]
    for attribute_id in (
        "task_complexity",
        "reading_demand",
        "input_demand",
        "memory_demand",
        "decision_demand",
        "error_criticality",
    ):
        assert 0 <= result[attribute_id]["value"] <= 100


def test_task_revision_keeps_attribute_updates_bounded_after_added_step():
    current = task_model(["Suche eingeben", "Ergebnisse lesen", "Hotel auswählen"])
    revised = task_model(
        [
            "Suche eingeben",
            "Ergebnisse lesen",
            "Filter auswählen",
            "Hotel auswählen",
        ]
    )
    revised["steps"][2]["description"] = (
        "Mehrere Filter auswählen, Optionen vergleichen und Pflichtangaben prüfen"
    )
    revised["steps"][2]["cognitive_requirements"] = [
        "Auswahl treffen",
        "Informationen vergleichen",
        "Eingaben prüfen",
    ]

    result = merge_task_model_revision(current, revised)

    assert result["number_of_steps"]["value"] == 4
    for attribute_id in (
        "task_complexity",
        "reading_demand",
        "input_demand",
        "memory_demand",
        "decision_demand",
        "error_criticality",
    ):
        assert result[attribute_id]["value"] < 100


def test_task_revision_preserves_existing_attribute_floor_when_step_is_added():
    current = task_model(["Suche eingeben", "Ergebnisse lesen", "Hotel auswählen"])
    current["task_complexity"] = attribute(55)
    current["orthographic_irregularity"] = attribute(10)
    revised = task_model(
        [
            "Suche eingeben",
            "Ergebnisse lesen",
            "Filter auswählen",
            "Hotel auswählen",
        ]
    )

    result = merge_task_model_revision(current, revised)

    assert result["number_of_steps"]["value"] == 4
    assert result["task_complexity"]["value"] >= 55
    assert result["orthographic_irregularity"]["value"] >= 10


def test_task_revision_does_not_duplicate_existing_step():
    current = task_model(["A", "B", "C"])
    revised = task_model(["A", "B", "C", "C"])

    result = merge_task_model_revision(current, revised)

    assert [step["name"] for step in result["steps"]] == ["A", "B", "C"]


def test_task_revision_can_update_existing_reading_step_without_adding_step():
    current = task_model(["Produktdetails lesen", "Buchung prüfen"])
    revised = task_model(["Produktdetails lesen", "Buchung prüfen"])
    revised["steps"][0]["description"] = (
        "Sechs Seiten Produktdetails sorgfältig lesen und verstehen"
    )
    revised["steps"][0]["goms_operations"] = ["read", "read", "think", "verify"]
    revised["steps"][0]["operation_time_estimates"] = [
        {
            "operation": "read",
            "estimated_duration_seconds": 45,
            "cognitive_requirement": "Produktdetails lesen",
        },
        {
            "operation": "read",
            "estimated_duration_seconds": 45,
            "cognitive_requirement": "weitere Produktdetails lesen",
        },
        {
            "operation": "think",
            "estimated_duration_seconds": 20,
            "cognitive_requirement": "Informationen einordnen",
        },
        {
            "operation": "verify",
            "estimated_duration_seconds": 10,
            "cognitive_requirement": "Verständnis prüfen",
        },
    ]
    revised["steps"][0]["estimated_duration_seconds"] = 120

    before = derive_task_attribute_values(current)
    result = merge_task_model_revision(current, revised)

    assert [step["name"] for step in result["steps"]] == [
        "Produktdetails lesen",
        "Buchung prüfen",
    ]
    assert result["number_of_steps"]["value"] == 2
    assert result["steps"][0]["estimated_duration_seconds"] == 120
    assert result["steps"][0]["goms_operations"] == [
        "read",
        "read",
        "think",
        "verify",
    ]
    assert result["reading_demand"]["value"] > before["reading_demand"]


class GeneratedTaskModel:
    def __init__(self, data: dict):
        self.data = data

    def model_dump(self) -> dict:
        return self.data


def test_review_node_uses_current_task_model_and_invalidates_downstream(monkeypatch):
    current = task_model(["A", "B", "C"])
    captured = {}

    def fake_generate_task_model(**kwargs):
        captured.update(kwargs)
        return GeneratedTaskModel(task_model(["A", "B", "C", "D"]))

    monkeypatch.setattr(
        generation_service,
        "generate_task_model",
        fake_generate_task_model,
    )

    result = model_nodes.construct_task_model(
        {
            "current_stage": "review_base_task",
            "scenario_context": {"description": "Test scenario"},
            "dimensions": {},
            "revision_instruction": "Ergänze D.",
            "task_model": current,
            "computed_parameters": {"old": True},
            "simulation_model": {"old": True},
            "results": {"old": True},
            "simulation_results": {"old": True},
        }
    )

    assert captured["current_task_model"] == current
    assert [step["name"] for step in result["task_model"]["steps"]] == [
        "A",
        "B",
        "C",
        "D",
    ]
    assert result["computed_parameters"] == {}
    assert result["simulation_model"] == {}
    assert result["simulation_results"] == {}
    assert result["results"] == {}
