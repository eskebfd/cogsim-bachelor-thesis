from backend.domains.simulation.schemas.recommendations import (
    PositiveFindingView,
    RecommendationView,
)

from backend.domains.simulation.recommendation_helpers import (
    RECOMMENDATION_THRESHOLDS,
    _confidence,
    _contextual_error_reasoning,
    _contextual_fallback_actions,
    _delay_values,
    _event_labels,
    _event_types,
    _events_for_rows,
    _is_decision_step,
    _is_input_step,
    _is_reading_step,
    _is_significant_delay,
    _metric,
    _priority,
    _rows_by_step,
    _step_label,
    _step_stats,
    _structured_recommendation,
    _with_interpretation_context,
)


def _make_text_recommendation(
    *,
    profile_id: str,
    profile_label: str,
    step: dict,
    rows: list[dict],
    events: list[dict],
) -> RecommendationView:
    planned, actual, relative = _delay_values(step)
    stats = _step_stats(rows)
    evidence = [
        f"Basiszeit {planned:.0f} Sekunden, simulierte Zeit {actual:.0f} Sekunden",
        f"relative Zeitabweichung {relative * 100:.0f} %",
        f"niedrigste Lesegeschwindigkeit {stats['min_reading_speed']:.1f} von 100",
    ]
    if stats["max_cognitive_load"] >= RECOMMENDATION_THRESHOLDS["notable_cognitive_load"]:
        evidence.append(f"kognitive Belastung bis {stats['max_cognitive_load']:.1f} von 100")
    if events:
        evidence.append("Events: " + ", ".join(_event_labels(events)))
    priority = _priority(
        event_count=len(events),
        relative_delay=relative,
        event_types=_event_types(events),
        critical=stats["min_reading_speed"] < RECOMMENDATION_THRESHOLDS["critical_reading_speed"],
    )
    return _with_interpretation_context(RecommendationView(
        recommendation_id=f"{profile_id}_{step.get('step_id')}_text_structure",
        profile_id=profile_id,
        title="Textinformationen klarer gliedern",
        priority=priority,
        finding=(
            f"Beim simulierten Profil {profile_label} ist der Schritt "
            f"„{_step_label(step)}“ als Lese- oder Prüfschritt auffällig."
        ),
        affected_step=_step_label(step),
        reasoning=(
            "Die Auffälligkeit passt zu einem textbezogenen Problem, weil der "
            "betroffene Schritt Informationsaufnahme enthält und die Simulation "
            "eine reduzierte Lesegeschwindigkeit beziehungsweise zusätzliche Zeit zeigt."
        ),
        supported_causes=[
            "Textmenge oder Informationsdichte",
            "mehrere parallel zu erfassende Informationen",
            "möglicherweise unklare Begriffe oder lange Beschreibungen",
        ],
        evidence=evidence,
        suggested_actions=[
            "wichtigste Information am Anfang des Abschnitts platzieren",
            "Beschreibungstexte kürzen",
            "Zwischenüberschriften oder visuelle Gruppierung ergänzen",
            "Detailinformationen optional aufklappbar machen",
            "Fachbegriffe kurz erklären",
        ],
        expected_effects=[
            "geringere Leseanforderung",
            "kürzere Bearbeitungszeit",
            "geringere kognitive Belastung",
        ],
        affected_metrics=["Lesegeschwindigkeit", "Bearbeitungszeit", "Kognitive Belastung"],
        related_events=_event_labels(events),
        usability_principles=["Selbstbeschreibungsfähigkeit", "Aufgabenangemessenheit"],
        confidence=_confidence(len(evidence), bool(events)),
        source_rule_ids=["reading_step_delay"],
        structured_recommendation=_structured_recommendation(
            step=step,
            events=events,
            fallback_metric_ids=["completion_time", "cognitive_load"],
            cause="Textmenge, Informationsdichte oder schwer erfassbare Begriffe",
            severity="mittel" if priority != "hoch" else "hoch",
            design_principle="Selbstbeschreibungsfähigkeit",
            general_recommendation=(
                "Textinformationen kürzen, gliedern und wichtige Inhalte "
                "visuell priorisieren."
            ),
            priority=priority,
            rule_id="reading_step_delay",
        ),
    ))


def _make_attention_recommendation(
    *,
    profile_id: str,
    profile_label: str,
    step: dict,
    rows: list[dict],
    events: list[dict],
) -> RecommendationView:
    planned, actual, relative = _delay_values(step)
    stats = _step_stats(rows)
    evidence = [
        f"niedrigste Aufmerksamkeit {stats['min_attention']:.1f} von 100",
    ]
    if _is_significant_delay(step):
        evidence.append(f"simulierte Zeit {actual:.0f} statt {planned:.0f} Sekunden")
    if stats["max_error_risk"] >= RECOMMENDATION_THRESHOLDS["notable_error_risk"]:
        evidence.append(f"Fehlerrisiko bis {stats['max_error_risk']:.1f} von 100")
    if events:
        evidence.append("Events: " + ", ".join(_event_labels(events)))
    priority = _priority(
        event_count=len(events),
        relative_delay=relative,
        event_types=_event_types(events),
        critical=stats["min_attention"] < RECOMMENDATION_THRESHOLDS["critical_attention"],
    )
    return _with_interpretation_context(RecommendationView(
        recommendation_id=f"{profile_id}_{step.get('step_id')}_attention_guidance",
        profile_id=profile_id,
        title="Orientierung und nächste Aktion deutlicher machen",
        priority=priority,
        finding=(
            f"Beim simulierten Profil {profile_label} sinkt die Aufmerksamkeit "
            f"im Schritt „{_step_label(step)}“ auffällig."
        ),
        affected_step=_step_label(step),
        reasoning=(
            "Die Empfehlung wird nur ausgelöst, weil in diesem Schritt eine "
            "auffällige Aufmerksamkeitssituation oder ein Attention-bezogenes Event vorliegt."
        ),
        supported_causes=[
            "visuelle Konkurrenz",
            "unklare Fortsetzung",
            "mehrere gleichwertige Handlungsoptionen",
        ],
        evidence=evidence,
        suggested_actions=[
            "primäre nächste Aktion visuell hervorheben",
            "konkurrierende Elemente reduzieren",
            "aktuellen Bearbeitungsstand sichtbar machen",
            "zusammengehörige Optionen klar gruppieren",
        ],
        expected_effects=[
            "stabilere Aufmerksamkeit",
            "weniger Suchaufwand",
            "geringeres Fehlerrisiko",
        ],
        affected_metrics=["Aufmerksamkeit", "Fehlerrisiko", "Bearbeitungszeit"],
        related_events=_event_labels(events),
        usability_principles=["Steuerbarkeit", "Erwartungskonformität"],
        confidence=_confidence(len(evidence), bool(events)),
        source_rule_ids=["attention_drop"],
        structured_recommendation=_structured_recommendation(
            step=step,
            events=events,
            fallback_metric_ids=["error_risk", "completion_time"],
            cause="reduzierte Aufmerksamkeit, konkurrierende Reize oder unklare Fortsetzung",
            severity="mittel" if priority != "hoch" else "hoch",
            design_principle="Erwartungskonformität",
            general_recommendation=(
                "Den nächsten Handlungsschritt deutlicher hervorheben und "
                "konkurrierende Reize reduzieren."
            ),
            priority=priority,
            rule_id="attention_drop",
        ),
    ))


def _make_error_recommendation(
    *,
    profile_id: str,
    profile_label: str,
    step: dict,
    rows: list[dict],
    events: list[dict],
) -> RecommendationView:
    _, _, relative = _delay_values(step)
    stats = _step_stats(rows)
    is_input = _is_input_step(step)
    is_decision = _is_decision_step(step)
    if is_input:
        actions = [
            "Pflichtangaben klar markieren",
            "Eingaben direkt prüfen",
            "Fehlermeldungen konkret und handlungsorientiert formulieren",
            "kritische Eingaben vor dem Absenden zusammenfassen",
        ]
        causes = ["unsichere Eingabe", "fehlende Rückmeldung", "kritische Bestätigung"]
    elif is_decision:
        actions = [
            "Optionen vergleichbar darstellen",
            "Entscheidungskriterien sichtbar machen",
            "Anzahl paralleler Optionen reduzieren",
            "Folgen der Auswahl klar erklären",
        ]
        causes = ["schwer vergleichbare Optionen", "unklare Entscheidungskriterien"]
    else:
        actions = [
            "Beschriftungen präzisieren",
            "Auswahlzustände sichtbar machen",
            "Rückmeldung nach Klicks deutlicher anzeigen",
            "Orientierungshilfen ergänzen",
        ]
        causes = ["unklare Orientierung", "unsichere Auswahl", "fehlende Rückmeldung"]
    evidence = [f"Fehlerrisiko bis {stats['max_error_risk']:.1f} von 100"]
    if events:
        evidence.append("Events: " + ", ".join(_event_labels(events)))
    priority = _priority(
        event_count=len(events),
        relative_delay=relative,
        event_types=_event_types(events),
        critical=stats["max_error_risk"] >= RECOMMENDATION_THRESHOLDS["critical_error_risk"],
    )
    return _with_interpretation_context(RecommendationView(
        recommendation_id=f"{profile_id}_{step.get('step_id')}_error_prevention",
        profile_id=profile_id,
        title="Fehler an dieser Stelle gezielt vorbeugen",
        priority=priority,
        finding=(
            f"Im Schritt „{_step_label(step)}“ ist das Fehlerrisiko für "
            f"{profile_label} auffällig."
        ),
        affected_step=_step_label(step),
        reasoning=_contextual_error_reasoning(
            profile_label=profile_label,
            step=step,
            stats=stats,
            events=events,
        ),
        supported_causes=causes,
        evidence=evidence,
        suggested_actions=actions,
        expected_effects=[
            "weniger Fehlentscheidungen",
            "klarere Rückmeldung",
            "höherer Aufgabenerfolgswert",
        ],
        affected_metrics=["Fehlerrisiko", "Aufgabenerfolgswert"],
        related_events=_event_labels(events),
        usability_principles=["Fehlertoleranz", "Selbstbeschreibungsfähigkeit"],
        confidence=_confidence(len(evidence), bool(events)),
        source_rule_ids=["error_risk"],
        structured_recommendation=_structured_recommendation(
            step=step,
            events=events,
            fallback_metric_ids=["error_risk", "task_success_score"],
            cause=", ".join(causes[:2]),
            severity="mittel" if priority != "hoch" else "hoch",
            design_principle="Fehlertoleranz",
            general_recommendation=(
                "Fehlerprävention, klare Rückmeldungen und sichere "
                "Korrekturmöglichkeiten ergänzen."
            ),
            priority=priority,
            rule_id="error_risk",
        ),
    ))


def _make_complexity_recommendation(
    *,
    profile_id: str,
    profile_label: str,
    step: dict,
    rows: list[dict],
    events: list[dict],
) -> RecommendationView:
    planned, actual, relative = _delay_values(step)
    stats = _step_stats(rows)
    evidence = [
        f"kognitive Belastung bis {stats['max_cognitive_load']:.1f} von 100",
    ]
    if _is_significant_delay(step):
        evidence.append(f"simulierte Zeit {actual:.0f} statt {planned:.0f} Sekunden")
    if events:
        evidence.append("Events: " + ", ".join(_event_labels(events)))
    actions = [
        "den Schritt in kleinere Teilaufgaben aufteilen",
        "Informationen in sichtbare Gruppen gliedern",
        "nur eine primäre Handlung pro Abschnitt hervorheben",
    ]
    if _is_decision_step(step):
        actions.append("Entscheidungskriterien direkt neben den Optionen anzeigen")
    priority = _priority(
        event_count=len(events),
        relative_delay=relative,
        event_types=_event_types(events),
        critical=stats["max_cognitive_load"] >= RECOMMENDATION_THRESHOLDS["critical_cognitive_load"],
    )
    return _with_interpretation_context(RecommendationView(
        recommendation_id=f"{profile_id}_{step.get('step_id')}_reduce_complexity",
        profile_id=profile_id,
        title="Schritt vereinfachen und klarer strukturieren",
        priority=priority,
        finding=(
            f"Der Schritt „{_step_label(step)}“ erzeugt für {profile_label} "
            "eine erhöhte mentale Belastung."
        ),
        affected_step=_step_label(step),
        reasoning=(
            "Die Empfehlung wird aus erhöhter kognitiver Belastung, Events oder "
            "einer relevanten Zeitabweichung im selben Schritt abgeleitet."
        ),
        supported_causes=[
            "mehrere gleichzeitige Anforderungen",
            "hohe Entscheidungs- oder Gedächtnisanforderung",
            "komplexe Informationsstruktur",
        ],
        evidence=evidence,
        suggested_actions=actions,
        expected_effects=[
            "geringere kognitive Belastung",
            "stabilerer Aufgabenfortschritt",
            "weniger Fehlerrisiko",
        ],
        affected_metrics=["Kognitive Belastung", "Bearbeitungszeit", "Fehlerrisiko"],
        related_events=_event_labels(events),
        usability_principles=["Aufgabenangemessenheit", "Lernförderlichkeit"],
        confidence=_confidence(len(evidence), bool(events)),
        source_rule_ids=["cognitive_load"],
        structured_recommendation=_structured_recommendation(
            step=step,
            events=events,
            fallback_metric_ids=["cognitive_load", "error_risk"],
            cause="mehrere gleichzeitige Anforderungen oder komplexe Informationsstruktur",
            severity="mittel" if priority != "hoch" else "hoch",
            design_principle="Aufgabenangemessenheit",
            general_recommendation=(
                "Den Schritt in kleinere Einheiten gliedern und parallele "
                "Anforderungen reduzieren."
            ),
            priority=priority,
            rule_id="cognitive_load",
        ),
    ))


def _make_fallback_recommendation(
    *,
    profile_id: str,
    profile_label: str,
    step: dict,
) -> RecommendationView:
    planned, actual, relative = _delay_values(step)
    return _with_interpretation_context(RecommendationView(
        recommendation_id=f"{profile_id}_{step.get('step_id')}_inspect_step",
        profile_id=profile_id,
        title="Auffälligen Schritt ergänzend prüfen",
        priority="niedrig",
        finding=(
            f"Der Schritt „{_step_label(step)}“ dauert bei {profile_label} "
            f"{actual:.0f} Sekunden statt {planned:.0f} Sekunden."
        ),
        affected_step=_step_label(step),
        reasoning=(
            "Die Zeitabweichung lässt sich anhand der aktuell protokollierten Daten "
            "nicht eindeutig einem einzelnen Faktor zuordnen."
        ),
        supported_causes=["unklare Ursache"],
        evidence=[f"relative Zeitabweichung {relative * 100:.0f} %"],
        suggested_actions=_contextual_fallback_actions(step),
        expected_effects=[
            "klarerer nächster Schritt",
            "weniger unnötiger Such- oder Prüfaufwand",
            "bessere Einordnung der Ursache",
        ],
        affected_metrics=["Bearbeitungszeit"],
        confidence="niedrig",
        source_rule_ids=["unattributed_delay"],
        structured_recommendation=_structured_recommendation(
            step=step,
            events=[],
            fallback_metric_ids=["completion_time"],
            cause="Zeitabweichung ohne eindeutig zuordenbaren Einzelfaktor",
            severity="niedrig",
            design_principle="Aufgabenangemessenheit",
            general_recommendation=(
                "Den Schritt mit realen Nutzenden prüfen und Ursache der "
                "Zeitabweichung genauer einordnen."
            ),
            priority="niedrig",
            rule_id="unattributed_delay",
        ),
    ))


def _dedupe_recommendations(
    recommendations: list[RecommendationView],
) -> list[RecommendationView]:
    seen = set()
    deduped = []
    for recommendation in sorted(
        recommendations,
        key=lambda item: {"hoch": 0, "mittel": 1, "niedrig": 2}.get(item.priority, 3),
    ):
        key = (
            recommendation.profile_id,
            recommendation.affected_step,
            recommendation.source_rule_ids[0] if recommendation.source_rule_ids else recommendation.title,
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(recommendation)
    return deduped


def build_profile_recommendation_views(
    *,
    profile_id: str,
    profile_label: str,
    timeline: list[dict],
    task_step_durations: list[dict],
    metrics: dict,
    completed: bool = True,
) -> tuple[list[str], list[str], list[dict], list[dict]]:
    rows_by_step = _rows_by_step(timeline)
    recommendations: list[RecommendationView] = []
    problems: list[str] = []

    for step in task_step_durations:
        step_id = str(step.get("step_id") or "")
        rows = rows_by_step.get(step_id, [])
        events = _events_for_rows(rows)
        event_types = _event_types(events)
        stats = _step_stats(rows)
        significant_delay = _is_significant_delay(step)
        has_attention_evidence = (
            "very_low_attention" in event_types
            or stats["min_attention"] < RECOMMENDATION_THRESHOLDS["critical_attention"]
            or (
                profile_id == "adhd"
                and stats["min_attention"] < RECOMMENDATION_THRESHOLDS["notable_attention"]
                and significant_delay
            )
        )
        has_reading_evidence = (
            _is_reading_step(step)
            and (
                stats["min_reading_speed"] < RECOMMENDATION_THRESHOLDS["critical_reading_speed"]
                or (
                    profile_id in {"dyslexie", "dyslexia"}
                    and stats["min_reading_speed"] < RECOMMENDATION_THRESHOLDS["notable_reading_speed"]
                    and significant_delay
                )
            )
        )
        has_error_evidence = (
            "high_error_risk" in event_types
            or "rework_event" in event_types
            or stats["max_error_risk"] >= RECOMMENDATION_THRESHOLDS["notable_error_risk"]
        )
        has_complexity_evidence = (
            "very_high_cognitive_load" in event_types
            or stats["max_cognitive_load"] >= RECOMMENDATION_THRESHOLDS["notable_cognitive_load"]
        )

        if not completed and step.get("status") == "aborted":
            has_complexity_evidence = True

        if has_reading_evidence:
            recommendations.append(
                _make_text_recommendation(
                    profile_id=profile_id,
                    profile_label=profile_label,
                    step=step,
                    rows=rows,
                    events=events,
                )
            )
        if has_attention_evidence:
            recommendations.append(
                _make_attention_recommendation(
                    profile_id=profile_id,
                    profile_label=profile_label,
                    step=step,
                    rows=rows,
                    events=events,
                )
            )
        if has_error_evidence:
            recommendations.append(
                _make_error_recommendation(
                    profile_id=profile_id,
                    profile_label=profile_label,
                    step=step,
                    rows=rows,
                    events=events,
                )
            )
        if has_complexity_evidence:
            recommendations.append(
                _make_complexity_recommendation(
                    profile_id=profile_id,
                    profile_label=profile_label,
                    step=step,
                    rows=rows,
                    events=events,
                )
            )
        if significant_delay and not (
            has_reading_evidence
            or has_attention_evidence
            or has_error_evidence
            or has_complexity_evidence
        ):
            recommendations.append(
                _make_fallback_recommendation(
                    profile_id=profile_id,
                    profile_label=profile_label,
                    step=step,
                )
            )

    recommendation_views = _dedupe_recommendations(recommendations)
    for recommendation in recommendation_views:
        problems.append(recommendation.finding)

    positive_findings = []
    if not recommendation_views:
        event_count = sum(len(row.get("events", [])) for row in timeline)
        completion_efficiency = _metric(metrics, "completion_efficiency")
        task_success = _metric(metrics, "task_success_score")
        finding = (
            f"Für {profile_label} wurden keine kritischen Auffälligkeiten erkannt."
        )
        evidence = []
        if event_count == 0:
            evidence.append("keine auffälligen Situationen")
        if completion_efficiency >= 65:
            evidence.append(f"Bearbeitungseffizienz {completion_efficiency:.1f} von 100")
        if task_success >= 65:
            evidence.append(f"Aufgabenerfolgswert {task_success:.1f} von 100")
        positive_findings.append(
            PositiveFindingView(
                profile_id=profile_id,
                title="Kein dringender Anpassungsbedarf",
                finding=finding,
                evidence=evidence,
            )
        )

    legacy_recommendations = [
        recommendation.title for recommendation in recommendation_views
    ]
    return (
        problems,
        legacy_recommendations,
        [recommendation.model_dump() for recommendation in recommendation_views],
        [finding.model_dump() for finding in positive_findings],
    )
