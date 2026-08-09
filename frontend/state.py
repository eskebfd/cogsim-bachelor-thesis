import uuid

import streamlit as st

DEFAULT_SCENARIO_TASK = (
    "Eine Person möchte für einen dreitägigen beruflichen Aufenthalt in Berlin "
    "eine geeignete Unterkunft über eine Hotelbuchungsseite buchen.\n\n"
    "- Reiseziel, Anreise- und Abreisedatum sowie Gästeanzahl eingeben\n"
    "- Treffer nach Preis, Lage und Bewertung filtern\n"
    "- Mehrere Angebote vergleichen und einzelne Hoteldetails öffnen\n"
    "- Informationen zu Zimmerausstattung, Frühstück, WLAN, Stornierung und "
    "Entfernung zum Veranstaltungsort lesen\n"
    "- Ein Angebot auswählen, das zum Budget und zu den Terminbedingungen passt\n"
    "- Persönliche Daten, E-Mail-Adresse und Zahlungsinformationen eingeben\n"
    "- Alle Angaben vor dem Absenden prüfen und die Buchungsbestätigung "
    "nachvollziehen"
)

DEFAULT_SCENARIO_INTERFACE = (
    "Die Hotelbuchungsseite besteht aus einer Suchmaske, einer Ergebnisliste "
    "mit mehreren Hotelkarten, seitlichen Filtern und Hoteldetails mit langen "
    "Textabschnitten.\n\n"
    "- Hotelkarten zeigen Preis, Bewertung, Lagehinweise, Verfügbarkeitsstatus "
    "und mehrere Handlungsbuttons\n"
    "- Detailseiten enthalten Tabs und ausklappbare Bereiche zu Zimmeroptionen, "
    "Zusatzkosten und Stornierungsbedingungen\n"
    "- Während der Buchung erscheinen Hinweise zu verbleibenden Zimmern, "
    "Preisänderungen und fehlenden Pflichtfeldern\n"
    "- Einige Rückmeldungen sind farblich hervorgehoben, andere erscheinen nur "
    "als kurzer Text unterhalb des jeweiligen Eingabefeldes"
)

DEFAULT_SCENARIO_ENVIRONMENT = (
    "Die Nutzung findet auf einem Laptop in einem Großraumbüro statt.\n\n"
    "- Im Hintergrund finden Gespräche statt\n"
    "- Gelegentlich erscheinen Benachrichtigungen\n"
    "- Es besteht leichter Zeitdruck, weil die Buchung vor einem anschließenden "
    "Termin abgeschlossen werden soll\n"
    "- Eingabefehler sollen vermieden werden, da die Buchung verbindlich ist "
    "und falsche Reise- oder Zahlungsdaten später nur mit Aufwand korrigiert "
    "werden können"
)

DEFAULT_SCENARIO = (
    f"Aufgabe\n{DEFAULT_SCENARIO_TASK}\n\n"
    f"Interface\n{DEFAULT_SCENARIO_INTERFACE}\n\n"
    f"Umgebung\n{DEFAULT_SCENARIO_ENVIRONMENT}"
)


def create_empty_backend_state() -> dict:
    return {
        "scenario_description": "",
        "scenario_text": None,
        "scenario_image": None,
        "scenario_image_metadata": None,
        "multimodal_analysis": None,
        "screenshot_task_analysis": None,
        "session_id": "",
        "current_stage": "dimensions",
        "scenario_context": {},
        "task_model": {},
        "user_model": {},
        "user_models": {},
        "interface_model": {},
        "environment_model": {},
        "evaluation_goal_selection": None,
        "evaluation_metrics": None,
        "simulation_plan": None,
        "computed_parameters": {},
        "simulation_model": {},
        "simulation_step": 0,
        "simulation_finished": False,
        "feedback_target": "",
        "feedback": {},
        "revision_instruction": "",
        "last_feedback": {},
        "logs": [],
        "results": {},
        "simulation_results": {},
        "visualization": {},
        "dimensions": {},
    }


def init_state() -> None:
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "current_view" not in st.session_state:
        st.session_state.current_view = "home"

    if "current_stage" not in st.session_state:
        st.session_state.current_stage = "dimensions"

    if "simulation_step" not in st.session_state:
        st.session_state.simulation_step = 1

    if "scenario_task" not in st.session_state:
        st.session_state.scenario_task = DEFAULT_SCENARIO_TASK

    if "scenario_interface" not in st.session_state:
        st.session_state.scenario_interface = DEFAULT_SCENARIO_INTERFACE

    if "scenario_environment" not in st.session_state:
        st.session_state.scenario_environment = DEFAULT_SCENARIO_ENVIRONMENT

    if "scenario_input" not in st.session_state:
        st.session_state.scenario_input = DEFAULT_SCENARIO

    if "scenario_image_upload" not in st.session_state:
        st.session_state.scenario_image_upload = None

    if "scenario_image_uploader_version" not in st.session_state:
        st.session_state.scenario_image_uploader_version = 0

    if "screenshot_task_analysis" not in st.session_state:
        st.session_state.screenshot_task_analysis = None

    if "screenshot_task_analysis_error" not in st.session_state:
        st.session_state.screenshot_task_analysis_error = None

    if "screenshot_task_analysis_image_key" not in st.session_state:
        st.session_state.screenshot_task_analysis_image_key = None

    if "screenshot_task_analysis_applied_key" not in st.session_state:
        st.session_state.screenshot_task_analysis_applied_key = None

    if "screenshot_task_analysis_pending_text" not in st.session_state:
        st.session_state.screenshot_task_analysis_pending_text = None

    if "screenshot_interface_analysis_pending_text" not in st.session_state:
        st.session_state.screenshot_interface_analysis_pending_text = None

    if "scenario_image_metadata" not in st.session_state:
        st.session_state.scenario_image_metadata = None

    if "multimodal_analysis" not in st.session_state:
        st.session_state.multimodal_analysis = None

    if "backend_state" not in st.session_state:
        backend_state = create_empty_backend_state()
        backend_state["session_id"] = st.session_state.session_id
        backend_state["scenario_description"] = st.session_state.scenario_input
        backend_state["current_stage"] = st.session_state.current_stage
        st.session_state.backend_state = backend_state

    if "dimensions" not in st.session_state:
        st.session_state.dimensions = None

    if "base_model_preview" not in st.session_state:
        st.session_state.base_model_preview = None

    if "computed_parameters_preview" not in st.session_state:
        st.session_state.computed_parameters_preview = None

    if "simulation_result" not in st.session_state:
        st.session_state.simulation_result = None

    if "user_profile" not in st.session_state:
        st.session_state.user_profile = None

    if "user_profiles" not in st.session_state:
        st.session_state.user_profiles = []

    if "comparison_baseline" not in st.session_state:
        st.session_state.comparison_baseline = "Generisch"

    if "device" not in st.session_state:
        st.session_state.device = None

    if "detected_task" not in st.session_state:
        st.session_state.detected_task = None

    if "environment" not in st.session_state:
        st.session_state.environment = None

    if "evaluation_metrics" not in st.session_state:
        st.session_state.evaluation_metrics = None

    if "evaluation_goal_selection" not in st.session_state:
        st.session_state.evaluation_goal_selection = None

    if "last_base_model_feedback" not in st.session_state:
        st.session_state.last_base_model_feedback = None


def get_session_id() -> str:
    return st.session_state.get(
        "session_id",
        "default_session",
    )


def update_backend_state(**updates) -> None:
    backend_state = st.session_state.get(
        "backend_state",
        {},
    )
    backend_state.update(updates)
    st.session_state.backend_state = backend_state


def _model_attribute_value(model: dict, attribute_id: str) -> int | None:
    attribute = model.get(attribute_id)
    if isinstance(attribute, dict):
        attribute = attribute.get("value")

    try:
        return max(0, min(100, int(round(float(attribute)))))
    except (TypeError, ValueError):
        return None


def _sync_dimension_group_from_model(
    *,
    dimensions: dict | None,
    group_key: str,
    model: dict,
) -> None:
    if not dimensions or not model:
        return

    signals = dimensions.get(group_key)
    if not isinstance(signals, dict):
        return

    for attribute_id in signals:
        value = _model_attribute_value(model, attribute_id)
        if value is None:
            continue

        signal = signals.get(attribute_id)
        if isinstance(signal, dict):
            signal["value"] = value
            slider_key = f"dimension_value_{group_key}_{attribute_id}"
            st.session_state[slider_key] = value


def _update_model_attribute_value(
    model: dict,
    attribute_id: str,
    value: int,
) -> None:
    attribute = model.get(attribute_id)
    if isinstance(attribute, dict):
        attribute["value"] = value
    else:
        model[attribute_id] = value


def apply_dimension_values_to_model_previews(
    dimensions: dict | None = None,
) -> None:
    dimensions = dimensions or st.session_state.get("dimensions") or {}
    base_model_preview = st.session_state.get("base_model_preview") or {}
    backend_state = st.session_state.get("backend_state") or {}

    groups = (
        ("task_signals", "task_model"),
        ("interface_signals", "interface_model"),
        ("environment_signals", "environment_model"),
    )

    for group_key, model_key in groups:
        signals = dimensions.get(group_key)
        if not isinstance(signals, dict):
            continue

        preview_model = base_model_preview.get(model_key)
        backend_model = backend_state.get(model_key)

        for attribute_id, signal in signals.items():
            if not isinstance(signal, dict):
                continue

            value = _model_attribute_value(signal, "value")
            if value is None:
                continue

            if isinstance(preview_model, dict) and attribute_id in preview_model:
                _update_model_attribute_value(
                    preview_model,
                    attribute_id,
                    value,
                )

            if isinstance(backend_model, dict) and attribute_id in backend_model:
                _update_model_attribute_value(
                    backend_model,
                    attribute_id,
                    value,
                )

    st.session_state.base_model_preview = base_model_preview
    backend_state["dimensions"] = dimensions
    backend_state["computed_parameters"] = {}
    backend_state["simulation_model"] = {}
    backend_state["results"] = {}
    backend_state["simulation_results"] = {}
    st.session_state.backend_state = backend_state
    st.session_state.computed_parameters_preview = None
    st.session_state.simulation_result = None


def apply_workflow_state(
    workflow_state: dict,
    *,
    target_step: int | None = None,
    feedback_scope: str | None = None,
    invalidate_downstream: bool = False,
) -> None:
    backend_state = st.session_state.get(
        "backend_state",
        {},
    )
    backend_state.update(workflow_state)
    st.session_state.backend_state = backend_state

    if workflow_state.get("dimensions"):
        st.session_state.dimensions = workflow_state["dimensions"]

    if "scenario_image_metadata" in workflow_state:
        st.session_state.scenario_image_metadata = workflow_state.get(
            "scenario_image_metadata"
        )

    if "multimodal_analysis" in workflow_state:
        st.session_state.multimodal_analysis = workflow_state.get("multimodal_analysis")

    if "screenshot_task_analysis" in workflow_state:
        st.session_state.screenshot_task_analysis = workflow_state.get(
            "screenshot_task_analysis"
        )

    has_base_models = any(
        workflow_state.get(key)
        for key in (
            "user_model",
            "task_model",
            "interface_model",
            "environment_model",
        )
    )

    if has_base_models:
        st.session_state.base_model_preview = {
            "user_model": workflow_state.get(
                "user_model",
                {},
            ),
            "task_model": workflow_state.get(
                "task_model",
                {},
            ),
            "interface_model": workflow_state.get(
                "interface_model",
                {},
            ),
            "environment_model": workflow_state.get(
                "environment_model",
                {},
            ),
        }

        if workflow_state.get("user_models"):
            st.session_state.base_model_preview["user_models"] = workflow_state[
                "user_models"
            ]

        if feedback_scope == "base":
            _sync_dimension_group_from_model(
                dimensions=st.session_state.get("dimensions"),
                group_key="task_signals",
                model=workflow_state.get("task_model") or {},
            )
            _sync_dimension_group_from_model(
                dimensions=st.session_state.get("dimensions"),
                group_key="interface_signals",
                model=workflow_state.get("interface_model") or {},
            )
            _sync_dimension_group_from_model(
                dimensions=st.session_state.get("dimensions"),
                group_key="environment_signals",
                model=workflow_state.get("environment_model") or {},
            )
            backend_state["dimensions"] = st.session_state.get("dimensions") or {}
            st.session_state.backend_state = backend_state

    if invalidate_downstream:
        st.session_state.computed_parameters_preview = None
        st.session_state.simulation_result = None

    if workflow_state.get("computed_parameters"):
        computed_parameters = workflow_state["computed_parameters"]
        simulation_model = workflow_state.get(
            "simulation_model",
            {},
        )

        st.session_state.computed_parameters_preview = {
            "computed_parameters": computed_parameters,
            "simulation_model": simulation_model,
        }

    if workflow_state.get("current_stage") == "simulation":
        st.session_state.simulation_result = workflow_state

    last_feedback = workflow_state.get("last_feedback")

    if feedback_scope == "base":
        st.session_state.last_base_model_feedback = last_feedback

    if target_step is not None:
        st.session_state.simulation_step = target_step


def build_scenario_context(
    scenario_description: str,
) -> dict:
    return {
        "description": scenario_description,
        "user_profile": st.session_state.get("user_profile"),
        "user_profiles": st.session_state.get(
            "user_profiles",
            [],
        ),
        "comparison_baseline": st.session_state.get(
            "comparison_baseline",
            "Generisch",
        ),
        "device": st.session_state.get("device"),
        "task": st.session_state.get("detected_task") or {},
        "environment": st.session_state.get("environment"),
    }


def reset_generated_data(
    *,
    preserve_profiles: bool = False,
    preserve_evaluation: bool = False,
) -> None:
    profiles = st.session_state.get(
        "user_profiles",
        [],
    )
    profile = st.session_state.get("user_profile")
    evaluation_metrics = st.session_state.get("evaluation_metrics")
    evaluation_goal_selection = st.session_state.get("evaluation_goal_selection")

    st.session_state.dimensions = None
    st.session_state.base_model_preview = None
    st.session_state.computed_parameters_preview = None
    st.session_state.simulation_result = None
    st.session_state.user_profile = profile if preserve_profiles else None
    st.session_state.user_profiles = profiles if preserve_profiles else []
    st.session_state.comparison_baseline = "Generisch"
    st.session_state.device = None
    st.session_state.detected_task = None
    st.session_state.environment = None
    st.session_state.scenario_image_upload = None
    st.session_state.screenshot_task_analysis = None
    st.session_state.screenshot_task_analysis_error = None
    st.session_state.screenshot_task_analysis_image_key = None
    st.session_state.screenshot_task_analysis_applied_key = None
    st.session_state.screenshot_task_analysis_pending_text = None
    st.session_state.screenshot_interface_analysis_pending_text = None
    st.session_state.scenario_image_metadata = None
    st.session_state.multimodal_analysis = None
    st.session_state.evaluation_metrics = (
        evaluation_metrics if preserve_evaluation else None
    )
    st.session_state.evaluation_goal_selection = (
        evaluation_goal_selection if preserve_evaluation else None
    )
    st.session_state.last_base_model_feedback = None
    update_backend_state(
        current_stage="dimensions",
        scenario_context={},
        scenario_image=None,
        scenario_image_metadata=None,
        multimodal_analysis=None,
        screenshot_task_analysis=None,
        task_model={},
        user_model={},
        user_models={},
        interface_model={},
        environment_model={},
        computed_parameters={},
        evaluation_goal_selection=(
            evaluation_goal_selection if preserve_evaluation else None
        ),
        evaluation_metrics=evaluation_metrics if preserve_evaluation else None,
        simulation_plan=None,
        simulation_model={},
        dimensions={},
        logs=[],
        results={},
        simulation_results={},
        visualization={},
        simulation_step=0,
        simulation_finished=False,
    )
