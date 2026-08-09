TASK_ATTRIBUTE_LABELS = {
    "task_complexity": "Aufgabenkomplexität",
    "number_of_steps": "Anzahl der Schritte",
    "reading_demand": "Leseanforderung",
    "unfamiliar_word_density": "Unbekannte Wörter",
    "orthographic_irregularity": "Orthografischer Anspruch",
    "morphological_complexity": "Wortform-Komplexität",
    "sustained_attention_demand": "Daueraufmerksamkeit",
    "task_switching_demand": "Wechselanforderung",
    "inhibition_demand": "Inhibitionsanforderung",
    "divided_attention_demand": "Geteilte Aufmerksamkeit",
    "input_demand": "Eingabeanforderung",
    "memory_demand": "Gedächtnisanforderung",
    "decision_demand": "Entscheidungsanforderung",
    "error_criticality": "Fehlerkritikalität",
}

INTERFACE_ATTRIBUTE_LABELS = {
    "text_volume": "Textmenge",
    "sentence_length": "Satzlänge",
    "word_difficulty": "Wortschwierigkeit",
    "technical_terms": "Fachbegriffe",
    "visual_clutter": "Visuelle Unruhe",
    "navigation_complexity": "Navigationskomplexität",
    "accessibility_support": "Unterstützende Funktionen",
    "feedback_quality": "Feedbackqualität",
    "text_legibility": "Textlesbarkeit",
    "text_density": "Textdichte",
    "line_tracking_difficulty": "Zeilenverfolgung",
    "stimulus_density": "Reizdichte",
    "irrelevant_signal_load": "Irrelevante Signale",
    "feedback_interruptiveness": "Unterbrechendes Feedback",
    "focus_guidance": "Fokusführung",
}

ENVIRONMENT_ATTRIBUTE_LABELS = {
    "noise_level": "Geräuschpegel",
    "distractions": "Ablenkungen",
    "time_pressure": "Zeitdruck",
    "context_stability": "Kontextstabilität",
    "visual_distraction": "Visuelle Ablenkung",
    "interruption_risk": "Unterbrechungsrisiko",
    "social_pressure": "Sozialer Druck",
    "device_constraints": "Geräteeinschränkungen",
    "lighting_quality": "Lichtqualität",
    "mobility_context": "Nutzung in Bewegung",
    "external_interruption_frequency": "Externe Unterbrechungen",
    "attention_recovery_support": "Wiedereinstiegsunterstützung",
}

MODEL_ATTRIBUTE_LABELS = {
    **TASK_ATTRIBUTE_LABELS,
    **INTERFACE_ATTRIBUTE_LABELS,
    **ENVIRONMENT_ATTRIBUTE_LABELS,
}


def attribute_items(labels: dict[str, str]) -> tuple[tuple[str, str], ...]:
    return tuple(labels.items())
