from backend.domains.evaluation.registries.metrics import (
    get_predefined_evaluation_metrics,
)
from backend.domains.simulation.config import DEFAULT_SIMULATION_CONFIG
from backend.domains.simulation.events.metric_relations import (
    METRIC_EVENT_RELATIONS,
    event_ids_for_selected_metrics,
)
from backend.domains.simulation.schemas.presentation import (
    CompletionTimeView,
    EventLegendItemView,
    MetricLegendItemView,
    ResultPresentationView,
    ResultSectionDefinitionView,
    ResultSummaryView,
    SummaryItemView,
    SummaryStatusView,
)


METRIC_PRESENTATION = {
    "cognitive_load": {
        "description": (
            "Beschreibt, wie stark das simulierte Profil während der "
            "Aufgabenbearbeitung mental beansprucht wird."
        ),
        "preferred_direction": "niedriger ist günstiger",
        "influencing_factors": [
            "Aufgabenkomplexität",
            "Textmenge und Lesbarkeit",
            "Navigationsaufwand",
            "Gedächtnis- und Entscheidungsanforderungen",
            "Ermüdung im Verlauf",
        ],
        "design_context": [
            "Informationen stärker strukturieren",
            "Schritte vereinfachen",
            "gleichzeitige Anforderungen reduzieren",
        ],
    },
    "error_risk": {
        "description": (
            "Schätzt, wie wahrscheinlich Fehler, unsichere Entscheidungen "
            "oder notwendige Wiederholungen während der Bearbeitung werden."
        ),
        "preferred_direction": "niedriger ist günstiger",
        "influencing_factors": [
            "kognitive Belastung",
            "geringe Aufmerksamkeit",
            "Ermüdung",
            "Zeitdruck",
            "unklare Eingaben oder Entscheidungen",
        ],
        "design_context": [
            "Eingaben absichern",
            "Rückmeldungen verständlicher machen",
            "kritische Entscheidungen klarer erklären",
        ],
    },
    "completion_time": {
        "description": (
            "Zeigt, wie lange ein Profil für das gesamte Szenario oder einen "
            "einzelnen Schritt benötigt."
        ),
        "preferred_direction": (
            "nur im Verhältnis zur GOMS-Basiszeit oder zu einem Zeitlimit bewerten"
        ),
        "influencing_factors": [
            "GOMS-Basisdauer",
            "profilspezifische Belastungen",
            "Zustandsveränderungen",
            "Events und Wiederholungen",
        ],
        "design_context": [
            "langsame Schritte priorisieren",
            "unnötige Zwischenhandlungen reduzieren",
            "wichtige Aktionen schneller auffindbar machen",
        ],
    },
    "completion_efficiency": {
        "description": (
            "Beschreibt das Verhältnis zwischen erreichtem Aufgabenfortschritt "
            "und dem dafür benötigten Aufwand beziehungsweise der benötigten Zeit."
        ),
        "preferred_direction": "höher ist günstiger",
        "influencing_factors": [
            "Bearbeitungszeit",
            "Aufmerksamkeit",
            "Lesegeschwindigkeit",
            "Aufgabenerfolg",
        ],
        "design_context": [
            "Abläufe kürzen",
            "Orientierung verbessern",
            "Rework vermeiden",
        ],
    },
    "task_success_score": {
        "description": (
            "Schätzt, wie wahrscheinlich das Profil das Szenario vollständig "
            "und ohne Abbruch bewältigt."
        ),
        "preferred_direction": "höher ist günstiger",
        "influencing_factors": [
            "Fehlerrisiko",
            "kognitive Belastung",
            "Navigationsaufwand",
            "Abbruch- und Rework-Ereignisse",
        ],
        "design_context": [
            "kritische Schritte vereinfachen",
            "Fehlerprävention ergänzen",
            "Aufgabenabschluss eindeutiger machen",
        ],
    },
    "time_limit_risk": {
        "description": (
            "Zeigt nur dann ein tatsächliches Zeitrisiko an, wenn für das "
            "Szenario ein externes Zeitlimit vorhanden ist."
        ),
        "preferred_direction": "niedriger ist günstiger",
        "influencing_factors": [
            "simulierte Bearbeitungszeit",
            "externes Zeitlimit",
            "noch offener Arbeitsumfang",
        ],
        "design_context": [
            "Zeitlimits prüfen",
            "Aufgabe verkürzen",
            "Zwischenschritte priorisieren",
        ],
    },
}

EVENT_PRESENTATION = {
    "high_error_risk": {
        "label": "Erhöhtes Fehlerrisiko",
        "description": (
            "Das berechnete Fehlerrisiko hat den festgelegten Schwellenwert "
            "überschritten."
        ),
        "trigger": "Fehlerrisiko ≥ {threshold}",
        "state_changes": ["Aufmerksamkeit kann sinken", "Ermüdung kann steigen"],
        "related_metrics": [
            "Fehlerrisiko",
            "Bearbeitungszeit",
            "Aufgabenerfolgswert",
            "Bearbeitungseffizienz",
        ],
        "possible_consequences": [
            "unsichere Entscheidungen",
            "falsche Eingaben",
            "Wiederholungen",
        ],
        "design_context": [
            "Feedback verbessern",
            "Eingaben vereinfachen",
            "Fehlerprävention ergänzen",
        ],
    },
    "very_high_cognitive_load": {
        "label": "Sehr hohe kognitive Belastung",
        "description": (
            "Die simulierte mentale Belastung hat einen kritischen Bereich erreicht."
        ),
        "trigger": "Kognitive Belastung ≥ {threshold}",
        "state_changes": ["Ermüdung steigt"],
        "related_metrics": [
            "Kognitive Belastung",
            "Fehlerrisiko",
            "Bearbeitungszeit",
            "Aufgabenerfolgswert",
        ],
        "possible_consequences": [
            "langsamere Bearbeitung",
            "mehr Fehlerrisiko",
            "schnellere Ermüdung",
        ],
        "design_context": [
            "Inhalte reduzieren",
            "Schritte vereinfachen",
            "Informationen klarer gruppieren",
        ],
    },
    "very_low_attention": {
        "label": "Stark reduzierte Aufmerksamkeit",
        "description": (
            "Die simulierte Aufmerksamkeit ist unter den definierten "
            "Schwellenwert gefallen."
        ),
        "trigger": "Aufmerksamkeit ≤ {threshold}",
        "state_changes": ["Aufmerksamkeit sinkt weiter"],
        "related_metrics": [
            "Fehlerrisiko",
            "Bearbeitungszeit",
            "Aufgabenerfolgswert",
        ],
        "possible_consequences": [
            "Hinweise werden übersehen",
            "nächste Schritte sind schwerer auffindbar",
            "Rework kann wahrscheinlicher werden",
        ],
        "design_context": [
            "Ablenkungen reduzieren",
            "wichtige Inhalte hervorheben",
            "Orientierungshilfen anbieten",
        ],
    },
    "time_pressure_warning": {
        "label": "Kritischer Zeitdruck",
        "description": (
            "Die verbleibende Zeit ist im Verhältnis zum noch ausstehenden "
            "Arbeitsaufwand kritisch."
        ),
        "trigger": "verbleibende Zeit ≤ {threshold} %",
        "state_changes": [
            "Aufmerksamkeit sinkt",
            "Ermüdung steigt",
        ],
        "related_metrics": [
            "Risiko einer Zeitüberschreitung",
            "Fehlerrisiko",
            "Bearbeitungszeit",
        ],
        "possible_consequences": [
            "schnellere, aber unsicherere Entscheidungen",
            "mehr Fehlerrisiko",
        ],
        "design_context": [
            "Zeitlimit prüfen",
            "Aufgabe verkürzen",
            "Zwischenstände ermöglichen",
        ],
    },
    "rework_event": {
        "label": "Schritt musste erneut bearbeitet werden",
        "description": (
            "Ein bereits bearbeiteter Schritt wurde aufgrund eines simulierten "
            "Fehlers oder erhöhten Fehlerrisikos wiederholt."
        ),
        "trigger": "Fehlerrisiko in rework-fähigem Schritt ≥ {threshold}",
        "state_changes": [
            "zusätzliche Bearbeitungszeit",
            "Ermüdung steigt",
        ],
        "related_metrics": [
            "Bearbeitungszeit",
            "Bearbeitungseffizienz",
            "Aufgabenerfolgswert",
        ],
        "possible_consequences": [
            "längere Bearbeitungszeit",
            "mehr Belastung",
            "geringere Effizienz",
        ],
        "design_context": [
            "Fehler früh anzeigen",
            "Korrekturen verständlich ermöglichen",
            "kritische Eingaben zusammenfassen",
        ],
    },
    "task_aborted": {
        "label": "Aufgabe wurde abgebrochen",
        "description": (
            "Das simulierte Profil hat die Bearbeitung nicht erfolgreich "
            "abgeschlossen, da eine definierte Abbruchbedingung erreicht wurde."
        ),
        "trigger": "Schrittdauer ≥ erlaubte maximale Schrittdauer",
        "state_changes": ["Simulation endet für dieses Profil"],
        "related_metrics": [
            "Aufgabenerfolgswert",
            "Bearbeitungszeit",
            "Bearbeitungseffizienz",
        ],
        "possible_consequences": [
            "Aufgabe wird nicht abgeschlossen",
            "Schritt ist für das Profil besonders kritisch",
        ],
        "design_context": [
            "kritischen Schritt vereinfachen",
            "zusätzliche Unterstützung anbieten",
            "Umfang reduzieren",
        ],
    },
    "high_inhibition_load": {
        "label": "Hohe Hemmungsanforderung",
        "description": (
            "Die Aufgabe verlangt stark, irrelevante Reize oder Handlungsimpulse "
            "zu unterdrücken."
        ),
        "trigger": "Hemmungsanforderung ≥ {threshold}",
        "state_changes": ["Aufmerksamkeit sinkt leicht", "Ermüdung steigt leicht"],
        "related_metrics": ["Fehlerrisiko", "Kognitive Belastung"],
        "possible_consequences": [
            "Ablenkungen werden belastender",
            "falsche Klicks werden plausibler",
        ],
        "design_context": [
            "visuelle Reize reduzieren",
            "primäre Aktionen klarer priorisieren",
        ],
    },
    "task_switching_strain": {
        "label": "Belastender Aufgabenwechsel",
        "description": (
            "Der Schritt verlangt belastende Wechsel zwischen Informationen "
            "oder Handlungsoptionen."
        ),
        "trigger": "Wechselanforderung ≥ {threshold} in Wechsel-Schritt",
        "state_changes": ["Aufmerksamkeit sinkt leicht", "Ermüdung steigt"],
        "related_metrics": [
            "Kognitive Belastung",
            "Fehlerrisiko",
            "Bearbeitungszeit",
        ],
        "possible_consequences": [
            "Orientierung geht leichter verloren",
            "Vergleiche dauern länger",
        ],
        "design_context": [
            "Vergleichsinformationen nebeneinander darstellen",
            "Schrittfolge deutlicher machen",
        ],
    },
}

SECTION_DEFINITIONS = {
    "profile_comparison": ResultSectionDefinitionView(
        section_id="profile_comparison",
        title="Metriken im Profilvergleich",
        short_explanation=(
            "Metriken fassen zentrale Ergebnisse der Simulation als Kennzahlen "
            "zusammen. Der Vergleich zeigt, wie sich Belastung, Fehlerrisiko, "
            "Bearbeitungszeit und Aufgabenerfolg zwischen den Nutzerprofilen "
            "unterscheiden."
        ),
        icon_id="bar-chart-3",
    ),
    "interpretation": ResultSectionDefinitionView(
        section_id="interpretation",
        title="Ergebnis einordnen",
        short_explanation=(
            "Dieser Bereich übersetzt die Simulation in verständliche nächste "
            "Schritte: zuerst konkrete Empfehlungen, daneben kurze Hilfen zu "
            "Metriken und Events."
        ),
        icon_id="lightbulb",
    ),
    "timeline": ResultSectionDefinitionView(
        section_id="timeline",
        title="Verlauf über die Aufgabe",
        short_explanation=(
            "Der Verlauf zeigt, wie sich ein ausgewählter Wert über die einzelnen "
            "Arbeitsschritte verändert. Dadurch wird sichtbar, wann ein Profil "
            "besonders belastet ist."
        ),
        icon_id="activity",
    ),
    "events": ResultSectionDefinitionView(
        section_id="events",
        title="Ausgelöste Events",
        short_explanation=(
            "Events markieren auffällige Situationen, die während einzelner "
            "Bearbeitungsschritte entstanden sind. Sie helfen zu verstehen, wann "
            "und warum sich der simulierte Zustand eines Profils verändert hat."
        ),
        icon_id="alert-triangle",
    ),
    "recommendations": ResultSectionDefinitionView(
        section_id="recommendations",
        title="Handlungsempfehlungen",
        short_explanation=(
            "Die Empfehlungen übersetzen auffällige Simulationsergebnisse in "
            "konkrete Designmaßnahmen. Sie zeigen, welcher Schritt betroffen ist, "
            "wodurch das Problem gestützt wird und was geprüft werden sollte."
        ),
        icon_id="lightbulb",
    ),
    "metric_legend": ResultSectionDefinitionView(
        section_id="metric_legend",
        title="Metrik-Legende",
        short_explanation=(
            "Die Legende erklärt die verwendeten Kennzahlen, ihre Richtung und "
            "welche Designaspekte sie beeinflussen können."
        ),
        icon_id="info",
    ),
    "event_legend": ResultSectionDefinitionView(
        section_id="event_legend",
        title="Event-Legende",
        short_explanation=(
            "Die Event-Legende erklärt, wann auffällige Situationen markiert werden und "
            "welche Metriken oder Zustände sie beeinflussen."
        ),
        icon_id="flag",
    ),
}


def _format_seconds(seconds: float) -> str:
    seconds = max(0, round(float(seconds)))
    minutes, rest = divmod(seconds, 60)
    if minutes:
        return f"{minutes} Min. {rest} Sek."
    return f"{rest} Sek."


def _metric_value(profile: dict, metric_id: str) -> float:
    metrics = profile.get("metrics") or profile.get("final_metrics") or {}
    if metric_id == "completion_time":
        return float(profile.get("completion_time_seconds") or 0)
    return float(metrics.get(metric_id, 0) or 0)


def _goms_basis_seconds(profile: dict) -> float:
    return sum(
        float(step.get("planned_duration_seconds") or 0)
        for step in profile.get("task_step_durations", [])
    )


def _event_count(profile: dict) -> int:
    display_events = profile.get("display_events")
    if display_events is not None:
        return len(display_events)
    return len(profile.get("events", [])) or sum(
        len(item.get("events", [])) for item in profile.get("timeline", [])
    )


def _summary_status(profiles: list[dict]) -> SummaryStatusView:
    if any(not profile.get("completed", True) for profile in profiles):
        return SummaryStatusView(
            status_id="aborted",
            label="Simulation vorzeitig abgebrochen",
            explanation=(
                "Mindestens ein simuliertes Nutzerprofil konnte das Szenario "
                "nicht vollständig bearbeiten. Der betroffene Schritt sollte "
                "priorisiert geprüft werden."
            ),
            severity="danger",
            icon_id="x-circle",
        )
    high_recommendations = sum(
        1
        for profile in profiles
        for card in profile.get("recommendation_cards", [])
        if card.get("priority") == "hoch"
    )
    total_events = sum(_event_count(profile) for profile in profiles)
    if high_recommendations:
        return SummaryStatusView(
            status_id="critical",
            label="Simulation mit kritischen Auffälligkeiten abgeschlossen",
            explanation=(
                "Alle simulierten Profile konnten das Szenario bearbeiten. "
                "Einige Ergebnisse weisen jedoch auf priorisierte "
                "Designprobleme hin."
            ),
            severity="warning",
            icon_id="alert-triangle",
            details=f"{high_recommendations} Empfehlung(en) mit hoher Priorität",
        )
    if total_events:
        return SummaryStatusView(
            status_id="completed_with_findings",
            label="Simulation mit Auffälligkeiten abgeschlossen",
            explanation=(
                "Alle ausgewählten Nutzerprofile konnten das Szenario vollständig "
                "bearbeiten. Während der Bearbeitung wurden jedoch auffällige "
                "Events erkannt."
            ),
            severity="notice",
            icon_id="check-circle",
            details=f"{total_events} auffällige Ereignisse erkannt",
        )
    return SummaryStatusView(
        status_id="completed_clear",
        label="Simulation erfolgreich abgeschlossen",
        explanation=(
            "Alle ausgewählten Nutzerprofile konnten das Szenario vollständig "
            "bearbeiten. Es wurden keine auffälligen Situationen markiert."
        ),
        severity="success",
        icon_id="check-circle",
    )


def _task_success_interpretation(value: float) -> str:
    if value >= 75:
        return "hohe Erfolgswahrscheinlichkeit"
    if value >= 50:
        return "mittlere Erfolgswahrscheinlichkeit"
    return "niedrige Erfolgswahrscheinlichkeit"


def _build_summary(profiles: list[dict]) -> ResultSummaryView:
    slowest_profile = max(
        profiles,
        key=lambda profile: profile.get("completion_time_seconds") or 0,
    )
    completion_seconds = float(slowest_profile.get("completion_time_seconds") or 0)
    goms_seconds = _goms_basis_seconds(slowest_profile)
    deviation = completion_seconds - goms_seconds
    deviation_percent = (deviation / goms_seconds * 100) if goms_seconds else 0
    profile_names = ", ".join(profile["profile_label"] for profile in profiles)
    total_events = sum(_event_count(profile) for profile in profiles)
    min_success_profile = min(
        profiles,
        key=lambda profile: _metric_value(profile, "task_success_score"),
    )
    min_success = _metric_value(min_success_profile, "task_success_score")

    return ResultSummaryView(
        status=_summary_status(profiles),
        primary_completion_time=CompletionTimeView(
            label="Simulierte Bearbeitungszeit",
            value_seconds=completion_seconds,
            value_label=_format_seconds(completion_seconds),
            basis_label=(
                "längste simulierte Bearbeitungszeit "
                f"({slowest_profile['profile_label']})"
            ),
            goms_basis_seconds=goms_seconds,
            goms_basis_label=_format_seconds(goms_seconds),
            deviation_seconds=deviation,
            deviation_label=(
                f"{deviation:+.0f} Sek. beziehungsweise {deviation_percent:+.0f} %"
            ),
            explanation=(
                "Die Basiszeit beschreibt die erwartete Bearbeitungsdauer "
                "unter günstigen Bedingungen. Die Simulation berücksichtigt "
                "zusätzlich profilspezifische Belastungen, Zustandsveränderungen, "
                "Events und mögliche Wiederholungen."
            ),
            icon_id="clock",
        ),
        secondary_items=[
            SummaryItemView(
                item_id="profiles",
                label=f"{len(profiles)} Nutzerprofile verglichen",
                value=str(len(profiles)),
                interpretation=profile_names,
                explanation=(
                    "Das Szenario wurde mit den ausgewählten Profilen simuliert, "
                    "damit Unterschiede in der Bearbeitung sichtbar werden."
                ),
                icon_id="users",
            ),
            SummaryItemView(
                item_id="task_success",
                label="Erfolgreiche Aufgabenbearbeitung",
                value=f"{min_success:.0f} von 100",
                interpretation=(
                    f"{_task_success_interpretation(min_success)} "
                    f"bei {min_success_profile['profile_label']}"
                ),
                explanation=(
                    "Dieser Wert beschreibt, wie wahrscheinlich es im Modell ist, "
                    "dass das Szenario vollständig und ohne Abbruch bearbeitet "
                    "wird. Ein höherer Wert ist günstiger."
                ),
                icon_id="target",
                direction="höher ist günstiger",
            ),
            SummaryItemView(
                item_id="events",
                label=f"{total_events} auffällige Ereignisse erkannt",
                value=str(total_events),
                interpretation=(
                    "keine auffälligen Ereignisse"
                    if total_events == 0
                    else "auffällige Situationen im Aufgabenverlauf"
                ),
                explanation=(
                    "Events markieren besondere Situationen innerhalb der "
                    "Simulation, beispielsweise stark sinkende Aufmerksamkeit, "
                    "hohe kognitive Belastung oder eine erneute Bearbeitung "
                    "eines Schritts."
                ),
                icon_id="flag",
                direction="weniger ist günstiger",
            ),
        ],
        explanation=(
            "Die Zusammenfassung zeigt zuerst, ob die Simulation abgeschlossen "
            "wurde und welche Bearbeitungszeit als repräsentativer Vergleichswert "
            "verwendet wird."
        ),
    )


def _metric_legend_items(
    selected_metric_ids: set[str] | None = None,
) -> list[MetricLegendItemView]:
    items = []
    for metric in get_predefined_evaluation_metrics():
        if (
            selected_metric_ids is not None
            and metric.metric_id not in selected_metric_ids
        ):
            continue
        presentation = METRIC_PRESENTATION.get(metric.metric_id)
        if not presentation:
            continue
        value_range = metric.expected_output_range or (0, 100)
        items.append(
            MetricLegendItemView(
                metric_id=metric.metric_id,
                label=metric.name,
                description=presentation["description"],
                value_range=f"{value_range[0]} bis {value_range[1]}",
                unit="Sekunden" if metric.metric_type == "time" else "Punkte",
                preferred_direction=presentation["preferred_direction"],
                interpretation_ranges=[
                    "0–24: sehr niedrig",
                    "25–49: niedrig bis moderat",
                    "50–74: deutlich vorhanden",
                    "75–100: stark ausgeprägt",
                ]
                if metric.metric_type != "time"
                else [
                    "Zeitwerte werden im Verhältnis zur GOMS-Basiszeit "
                    "oder zu einem expliziten Zeitlimit interpretiert."
                ],
                influencing_factors=presentation["influencing_factors"],
                related_events=[
                    EVENT_PRESENTATION[event_id]["label"]
                    for event_id in METRIC_EVENT_RELATIONS.get(metric.metric_id, [])
                    if event_id in EVENT_PRESENTATION
                ],
                design_context=presentation["design_context"],
            )
        )
    return items


def _event_legend_items(
    *,
    include_time_pressure: bool,
    selected_metric_ids: set[str] | None = None,
) -> list[EventLegendItemView]:
    thresholds = DEFAULT_SIMULATION_CONFIG.event_thresholds
    allowed_event_ids = event_ids_for_selected_metrics(selected_metric_ids)
    items = []
    for event_id, presentation in EVENT_PRESENTATION.items():
        if allowed_event_ids is not None and event_id not in allowed_event_ids:
            continue
        if event_id == "time_pressure_warning" and not include_time_pressure:
            continue
        threshold_key = "rework_error_risk" if event_id == "rework_event" else event_id
        threshold = thresholds.get(threshold_key)
        trigger_value = str(threshold) if threshold is not None else "dynamisch"
        trigger_description = presentation["trigger"].format(
            threshold=trigger_value
        )
        items.append(
            EventLegendItemView(
                event_id=event_id,
                label=presentation["label"],
                description=presentation["description"],
                trigger_description=trigger_description,
                trigger_value=trigger_value,
                severity="hoch",
                state_changes=presentation["state_changes"],
                related_metrics=presentation["related_metrics"],
                possible_consequences=presentation["possible_consequences"],
                design_context=presentation["design_context"],
            )
        )
    return items


def build_result_presentation_view(
    profile_results: list[dict],
    selected_metric_ids: set[str] | None = None,
) -> dict:
    include_time_pressure = any(
        profile.get("time_limit_seconds") is not None
        or any(
            event.get("event_type") == "time_pressure_warning"
            for event in profile.get("events", [])
        )
        for profile in profile_results
    )
    presentation = ResultPresentationView(
        summary=_build_summary(profile_results),
        sections=SECTION_DEFINITIONS,
        metric_legend=_metric_legend_items(selected_metric_ids),
        event_legend=_event_legend_items(
            include_time_pressure=include_time_pressure,
            selected_metric_ids=selected_metric_ids,
        ),
    )
    return presentation.model_dump()
