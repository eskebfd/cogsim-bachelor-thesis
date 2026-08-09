import streamlit as st
import hashlib
import json

from frontend.shared.services.workflow_api import (
    prepare_simulation_workflow,
    review_base_model,
)
from frontend.state import (
    apply_workflow_state,
    build_scenario_context,
    get_session_id,
)
from frontend.workflow.steps import SIMULATION_PLAN_STEP


def apply_base_review(
    feedback_target: str,
    feedback: dict,
    on_success=None,
) -> None:
    scenario_description = st.session_state.get(
        "scenario_input",
        "",
    )

    backend_state = st.session_state.get(
        "backend_state",
        {},
    )
    base_models = st.session_state.get("base_model_preview") or {}
    task_model = (
        base_models.get("task_model")
        or backend_state.get("task_model")
        or {}
    )
    interface_model = (
        base_models.get("interface_model")
        or backend_state.get("interface_model")
        or {}
    )
    environment_model = (
        base_models.get("environment_model")
        or backend_state.get("environment_model")
        or {}
    )
    user_model = (
        base_models.get("user_model")
        or backend_state.get("user_model")
        or {}
    )

    try:
        result = review_base_model(
            description=scenario_description,
            scenario_context=build_scenario_context(scenario_description),
            user_model=user_model,
            task_model=task_model,
            interface_model=interface_model,
            environment_model=environment_model,
            feedback_target=feedback_target,
            feedback=feedback,
            session_id=get_session_id(),
            simulation_plan=backend_state.get("simulation_plan"),
        )

    except RuntimeError as exc:
        st.error("Das Modell konnte nicht aktualisiert werden. "  f"{exc}")
        return

    apply_workflow_state(
        result,
        feedback_scope="base",
        invalidate_downstream=True,
    )

    if on_success is not None:
        on_success()

    st.rerun()


def add_missing_task_step(
    missing_step_description: str,
) -> None:
    normalized_description = missing_step_description.strip()

    if not normalized_description:
        st.warning("Bitte beschreibe den fehlenden Arbeitsschritt.")
        return

    current_task_model = (
        (st.session_state.get("base_model_preview") or {}).get("task_model")
        or (st.session_state.get("backend_state") or {}).get("task_model")
        or {}
    )
    request_key = hashlib.sha256(
        json.dumps(
            {
                "description": normalized_description,
                "task_model": current_task_model,
            },
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()

    if st.session_state.get("pending_missing_task_step_request") == request_key:
        return

    st.session_state.pending_missing_task_step_request = request_key

    feedback = {
        "missing_task_step": (
            "Überarbeite das bestehende Task Model anhand des folgenden "
            "Hinweises zur HTA-Aufgabenstruktur:\n\n"
            f"{normalized_description}\n\n"
            "Wenn der Hinweis einen tatsächlich fehlenden Arbeitsschritt "
            "beschreibt, ergänze ihn an einer fachlich sinnvollen Position. "
            "Wenn der Hinweis dagegen einen bestehenden Schritt präzisiert "
            "oder dessen Umfang verändert, passe diesen vorhandenen Schritt "
            "an, statt einen neuen Schritt zu erzeugen. Beispiel: Wenn ein "
            "Leseschritt deutlich umfangreicher ist, aktualisiere "
            "GOMS-Operationen, Operation-Time-Estimates und "
            "estimated_duration_seconds dieses Leseschritts. Aktualisiere "
            "danach Nummerierung, Reihenfolge und abhängige Aufgabenattribute "
            "auf Grundlage der vollständigen HTA. Erhalte alle bestehenden "
            "Schritte, sofern keine Anpassung für eine konsistente Struktur "
            "erforderlich ist."
        )
    }

    def clear_processed_missing_step() -> None:
        st.session_state.processed_missing_task_step_request = request_key
        st.session_state.pending_missing_task_step_request = None
        st.session_state.clear_missing_task_step_description = True

    try:
        apply_base_review(
            feedback_target="task_model",
            feedback=feedback,
            on_success=clear_processed_missing_step,
        )
    finally:
        if st.session_state.get("pending_missing_task_step_request") == request_key:
            st.session_state.pending_missing_task_step_request = None


def prepare_simulation() -> None:
    scenario_description = st.session_state.get(
        "scenario_input",
        "",
    )

    base_models = st.session_state.get("base_model_preview") or {}

    scenario_context = build_scenario_context(scenario_description)

    backend_state = st.session_state.get(
        "backend_state",
        {},
    )

    try:
        simulation_plan = backend_state["simulation_plan"]

        result = prepare_simulation_workflow(
            description=scenario_description,
            scenario_context=scenario_context,
            user_model=base_models.get(
                "user_model",
                {},
            ),
            task_model=base_models.get("task_model", {}),
            interface_model=base_models.get("interface_model", {}),
            environment_model=base_models.get("environment_model", {}),
            user_models=base_models.get(
                "user_models",
                {},
            ),
            evaluation_goal_selection=backend_state.get("evaluation_goal_selection"),
            evaluation_metrics=(
                backend_state.get("evaluation_metrics")
                or {"selected_metrics": simulation_plan["evaluation_metrics"]}
            ),
            simulation_plan=simulation_plan,
            session_id=get_session_id(),
        )

    except KeyError:
        st.error("Es wurde noch kein Simulationsplan erstellt.")
        return

    except RuntimeError as exc:
        st.error("Die Simulation konnte nicht vorbereitet werden. "  f"{exc}")
        return

    apply_workflow_state(
        result,
        target_step=SIMULATION_PLAN_STEP,
    )

    st.rerun()
