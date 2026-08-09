from backend.domains.simulation.recommendations import (
    _priority,
    build_profile_recommendation_views,
)


def _step(
    step_id: str,
    *,
    description: str,
    step_type: str,
    planned: float = 10,
    actual: float = 10,
) -> dict:
    return {
        "step_id": step_id,
        "display_name": f"Step {step_id[-1]} – {description}",
        "description": description,
        "step_type": step_type,
        "goms_operations": [step_type],
        "planned_duration_seconds": planned,
        "actual_duration_seconds": actual,
    }


def _timeline_row(
    step: dict,
    *,
    profile_id: str = "generic",
    attention: float = 85,
    reading_speed: float = 90,
    cognitive_load: float = 35,
    error_risk: float = 25,
    events: list[dict] | None = None,
) -> dict:
    return {
        "profile": profile_id,
        "current_task_step": {
            "step_id": step["step_id"],
            "step_index": int(step["step_id"][-1]) - 1,
            "description": step["description"],
            "name": step["description"],
            "step_type": step["step_type"],
            "goms_operations": step["goms_operations"],
        },
        "attention": attention,
        "reading_speed": reading_speed,
        "cognitive_load": cognitive_load,
        "error_risk": error_risk,
        "fatigue": 25,
        "events": events or [],
    }


def _recommendations(
    *,
    profile_id: str = "generic",
    profile_label: str = "Generic",
    steps: list[dict],
    timeline: list[dict],
) -> tuple[list[str], list[str], list[dict], list[dict]]:
    return build_profile_recommendation_views(
        profile_id=profile_id,
        profile_label=profile_label,
        timeline=timeline,
        task_step_durations=steps,
        metrics={
            "completion_efficiency": 75,
            "task_success_score": 80,
        },
    )


def test_generic_small_deviations_do_not_create_fake_recommendations():
    step = _step("s1", description="Angebot öffnen", step_type="click")
    problems, recommendations, cards, findings = _recommendations(
        steps=[step],
        timeline=[_timeline_row(step)],
    )

    assert problems == []
    assert recommendations == []
    assert cards == []
    assert findings
    assert findings[0]["title"] == "Kein dringender Anpassungsbedarf"


def test_adhd_attention_event_creates_attention_recommendation():
    step = _step(
        "s1",
        description="Hotelinformationen vergleichen",
        step_type="compare",
        planned=10,
        actual=18,
    )

    _, _, cards, _ = _recommendations(
        profile_id="adhd",
        profile_label="ADHS",
        steps=[step],
        timeline=[
            _timeline_row(
                step,
                profile_id="adhd",
                attention=42,
                events=[{"event_type": "very_low_attention"}],
            )
        ],
    )

    assert [card["source_rule_ids"][0] for card in cards] == ["attention_drop"]
    assert cards[0]["affected_step"] == "Step 1 – Hotelinformationen vergleichen"
    assert cards[0]["structured_recommendation"]["rule_id"] == "attention_drop"
    assert cards[0]["structured_recommendation"]["triggering_event_ids"] == [
        "very_low_attention"
    ]
    assert "error_risk" in cards[0]["structured_recommendation"][
        "triggering_metric_ids"
    ]
    assert cards[0]["interpretation_context"]["interpretation_role"] == (
        "language_generation_only"
    )


def test_adhd_without_attention_evidence_gets_no_attention_recommendation():
    step = _step(
        "s1",
        description="Hotel auswählen",
        step_type="compare",
        planned=10,
        actual=12,
    )

    _, _, cards, findings = _recommendations(
        profile_id="adhd",
        profile_label="ADHS",
        steps=[step],
        timeline=[_timeline_row(step, profile_id="adhd", attention=85)],
    )

    assert all("attention_drop" not in card["source_rule_ids"] for card in cards)
    assert findings


def test_dyslexia_reading_step_creates_text_recommendation():
    step = _step(
        "s1",
        description="Lange Hotelbeschreibung lesen",
        step_type="read",
        planned=12,
        actual=22,
    )

    _, _, cards, _ = _recommendations(
        profile_id="dyslexie",
        profile_label="Dyslexie",
        steps=[step],
        timeline=[
            _timeline_row(
                step,
                profile_id="dyslexie",
                reading_speed=58,
                cognitive_load=68,
            )
        ],
    )

    assert cards[0]["source_rule_ids"] == ["reading_step_delay"]
    assert "Textinformationen" in cards[0]["title"]
    assert cards[0]["structured_recommendation"]["deterministic"] is True
    assert cards[0]["structured_recommendation"]["affected_ui_component"] == (
        "Text- oder Informationsbereich"
    )


def test_dyslexia_navigation_delay_does_not_create_text_recommendation():
    step = _step(
        "s1",
        description="Filter öffnen",
        step_type="click",
        planned=8,
        actual=15,
    )

    _, _, cards, _ = _recommendations(
        profile_id="dyslexie",
        profile_label="Dyslexie",
        steps=[step],
        timeline=[_timeline_row(step, profile_id="dyslexie", reading_speed=58)],
    )

    assert all(card["source_rule_ids"] != ["reading_step_delay"] for card in cards)


def test_low_error_reading_step_does_not_create_form_recommendation():
    step = _step(
        "s1",
        description="Informationen lesen",
        step_type="read",
        planned=10,
        actual=18,
    )

    _, _, cards, _ = _recommendations(
        steps=[step],
        timeline=[_timeline_row(step, reading_speed=55, error_risk=30)],
    )

    assert all(card["source_rule_ids"] != ["error_risk"] for card in cards)
    assert all(
        "Pflichtangaben klar markieren" not in card.get("suggested_actions", [])
        for card in cards
    )


def test_unattributed_large_delay_gets_low_confidence_fallback():
    step = _step(
        "s1",
        description="Seite prüfen",
        step_type="inspect",
        planned=10,
        actual=18,
    )

    _, _, cards, _ = _recommendations(
        steps=[step],
        timeline=[_timeline_row(step)],
    )

    assert cards[0]["source_rule_ids"] == ["unattributed_delay"]
    assert cards[0]["confidence"] == "niedrig"


def test_repeated_same_problem_is_deduplicated_per_step():
    step = _step(
        "s1",
        description="Hotelbeschreibung lesen",
        step_type="read",
        planned=10,
        actual=20,
    )

    _, _, cards, _ = _recommendations(
        profile_id="dyslexie",
        profile_label="Dyslexie",
        steps=[step, step],
        timeline=[
            _timeline_row(step, profile_id="dyslexie", reading_speed=50),
            _timeline_row(step, profile_id="dyslexie", reading_speed=52),
        ],
    )

    text_cards = [
        card for card in cards if card["source_rule_ids"] == ["reading_step_delay"]
    ]
    assert len(text_cards) == 1


def test_recommendations_are_not_artificially_limited_to_four_cards():
    steps = [
        _step(
            f"s{index}",
            description=f"Schritt {index} prüfen",
            step_type="inspect",
            planned=10,
            actual=20,
        )
        for index in range(1, 7)
    ]

    _, _, cards, _ = _recommendations(
        steps=steps,
        timeline=[_timeline_row(step) for step in steps],
    )

    assert len(cards) == 6


def test_recommendation_priority_high_for_blocking_events():
    assert _priority(
        event_count=1,
        relative_delay=0.1,
        event_types={"task_aborted"},
    ) == "hoch"
    assert _priority(
        event_count=1,
        relative_delay=0.1,
        event_types={"rework_event"},
    ) == "hoch"


def test_recommendation_priority_medium_for_single_non_blocking_event():
    assert _priority(
        event_count=1,
        relative_delay=0.1,
        event_types={"very_low_attention"},
    ) == "mittel"


def test_recommendation_priority_low_without_event_or_relevant_delay():
    assert _priority(
        event_count=0,
        relative_delay=0.1,
        event_types=set(),
    ) == "niedrig"
