def _signal(value, sicher=None, angenommen=None, fehlend=None, rueckfragen=None):
    evidence = (sicher or angenommen or fehlend or ["Neutrale Annahme."])[0]
    confidence = "high" if sicher else "medium" if angenommen else "low"
    return {
        "value": value,
        "label": "vorläufiger Wert",
        "scale_min_description": "Eigenschaft ist kaum vorhanden",
        "scale_max_description": "Eigenschaft ist stark ausgeprägt",
        "rationale": evidence,
        "confidence": confidence,
    }


def _attribute(value, minimum, maximum, explanation, confidence="medium"):
    return {
        "value": value,
        "scale_min_description": minimum,
        "scale_max_description": maximum,
        "explanation": explanation,
        "confidence": confidence,
    }


MOCK_DIMENSIONS = {
    "detected_device": "Laptop",
    "primary_task": {
        "label": "Urlaubsantrag ausfüllen",
        "description": (
            "Mitarbeitende wählen Urlaubstage aus, geben einen Zeitraum an "
            "und senden den Antrag ab."
        ),
        "begründung": "Das Szenario beschreibt einen vollständigen Formularprozess.",
    },
    "scenario_summary": (
        "Eine Person füllt an einem Laptop einen digitalen Urlaubsantrag aus."
    ),
    "interface_context": {
        "interface_typ": "Online-Formular",
        "zentrale_ui_elemente": [
            "Kalenderauswahl",
            "Datumsfelder",
            "Prüfansicht",
            "Absenden-Button",
        ],
        "interaktionsumfang": "formularprozess",
        "beschreibung": "Mehrstufiger Formularprozess zur Beantragung von Urlaub.",
    },
    "task_options": [
        {
            "label": "Urlaubsantrag ausfüllen",
            "description": "Urlaubsantrag mit Datumswahl und Bestätigung.",
            "begründung": "Diese Aufgabe bildet den beschriebenen Prozess vollständig ab.",
        }
    ],
    "environment_options": [
        {
            "label": "Büro",
            "description": "Normale Büroumgebung mit gelegentlichen Unterbrechungen.",
        }
    ],
    "suggested_metrics": [
        "Bearbeitungszeit pro Schritt",
        "Kognitive Belastung pro Schritt",
        "Fehlerrisiko pro Schritt",
    ],
    "task_signals": {
        "task_complexity": _signal(
            55,
            sicher=["Urlaubsantrag umfasst Auswahl, Eingabe, Prüfung und Absenden."],
        ),
        "number_of_steps": _signal(
            5,
            sicher=["Mehrere Prozessschritte sind beschrieben."],
        ),
        "reading_demand": _signal(
            35,
            angenommen=["Formularhinweise müssen gelesen werden."],
        ),
        "input_demand": _signal(
            60,
            sicher=["Datum und Urlaubstage müssen ausgewählt werden."],
        ),
        "memory_demand": _signal(
            45,
            sicher=["Start- und Enddatum müssen zusammen geprüft werden."],
        ),
        "unfamiliar_word_density": _signal(
            20,
            angenommen=["Die Formularbegriffe sind überwiegend vertraut."],
        ),
        "orthographic_irregularity": _signal(
            15,
            angenommen=["Es sind keine orthografisch ungewöhnlichen Begriffe erkennbar."],
        ),
        "morphological_complexity": _signal(
            25,
            angenommen=["Die Wortformen wirken überwiegend einfach bis moderat."],
        ),
        "sustained_attention_demand": _signal(
            40,
            angenommen=["Der Formularprozess benötigt über mehrere Schritte Aufmerksamkeit."],
        ),
        "task_switching_demand": _signal(
            45,
            sicher=["Zwischen Datumsauswahl, Prüfung und Absenden wird gewechselt."],
        ),
        "inhibition_demand": _signal(
            30,
            angenommen=["Nur wenige irrelevante Handlungsoptionen sind beschrieben."],
        ),
        "divided_attention_demand": _signal(
            45,
            angenommen=["Mehrere Formularinformationen müssen gleichzeitig beachtet werden."],
        ),
    },
    "interface_signals": {
        "text_volume": _signal(40, angenommen=["Formular enthält moderate Textmenge."]),
        "sentence_length": _signal(35, angenommen=["Formulartexte sind eher kurz."]),
        "word_difficulty": _signal(25, angenommen=["Begriffe sind überwiegend bekannt."]),
        "technical_terms": _signal(20, angenommen=["Wenige organisatorische Fachbegriffe."]),
        "visual_clutter": _signal(45, sicher=["Kalender und Formularfelder sind relevant."]),
        "navigation_complexity": _signal(35, sicher=["Der Prozess bleibt formularbasiert."]),
        "accessibility_support": _signal(
            55,
            fehlend=["Konkrete Angaben zu Hilfetexten oder Barrierefreiheit."],
        ),
        "feedback_quality": _signal(
            60,
            fehlend=["Konkrete Angaben zu Fehlermeldungen und Statusfeedback."],
        ),
        "text_legibility": _signal(
            70,
            angenommen=["Keine Hinweise auf schlechte Lesbarkeit der Texte."],
        ),
        "text_density": _signal(
            35,
            angenommen=["Die Textdichte wirkt für ein Formular moderat."],
        ),
        "line_tracking_difficulty": _signal(
            25,
            angenommen=["Keine stark erschwerte Zeilenverfolgung erkennbar."],
        ),
        "stimulus_density": _signal(
            45,
            sicher=["Kalender, Eingabefelder und Prüfansicht konkurrieren visuell moderat."],
        ),
        "irrelevant_signal_load": _signal(
            25,
            angenommen=["Keine vielen irrelevanten Signale beschrieben."],
        ),
        "feedback_interruptiveness": _signal(
            30,
            fehlend=["Konkrete Popups oder unterbrechende Hinweise sind nicht beschrieben."],
        ),
        "focus_guidance": _signal(
            60,
            angenommen=["Der Formularablauf führt wahrscheinlich relativ klar durch die Aufgabe."],
        ),
    },
    "environment_signals": {
        "noise_level": _signal(35, angenommen=["Büroumgebung mit moderater Geräuschkulisse."]),
        "distractions": _signal(55, sicher=["Gelegentliche Unterbrechungen werden angenommen."]),
        "time_pressure": _signal(60, sicher=["Ein Zeitlimit ist als Parameter relevant."]),
        "context_stability": _signal(70, angenommen=["Büro ist grundsätzlich stabil."]),
        "external_interruption_frequency": _signal(
            45,
            sicher=["Gelegentliche Unterbrechungen werden angenommen."],
        ),
        "attention_recovery_support": _signal(
            60,
            angenommen=["Die Büroumgebung erlaubt wahrscheinlich einen Wiedereinstieg."],
        ),
    },
    "sichere_informationen": [
        "Es handelt sich um einen digitalen Urlaubsantrag.",
        "Der Ablauf enthält Auswahl-, Eingabe-, Prüf- und Absendehandlungen.",
    ],
    "angenommene_werte": [
        "Das Formular enthält moderate Textmenge.",
        "Die Nutzung findet an einem Laptop im Büro statt.",
    ],
    "fehlende_informationen": [
        "Konkrete Interface-Screens sind nicht beschrieben.",
        "Konkrete Fehlermeldungen und Hilfen sind nicht beschrieben.",
    ],
    "sinnvolle_rueckfragen": [
        "Gibt es ein hartes Zeitlimit?",
        "Welche Hilfen und Fehlermeldungen zeigt das Formular?",
    ],
    "annahmen": [
        "Fehlende Interface-Details wurden konservativ geschätzt.",
    ],
}

for _signal_group in (
    "task_signals",
    "interface_signals",
    "environment_signals",
):
    for _signal_id, _signal_data in MOCK_DIMENSIONS[_signal_group].items():
        _signal_data["id"] = _signal_id
        _signal_data["name"] = _signal_id.replace("_", " ").title()
        _signal_data["description"] = (
            f"Vorläufige Einschätzung für {_signal_data['name']}."
        )


MOCK_USER_MODEL = {
    "user_type": "ADHS + Dyslexie",
    "reading_difficulty": {
        "value": 70,
        "scale_min_description": "0 = keine Leseschwierigkeiten",
        "scale_max_description": "100 = sehr starke Leseschwierigkeiten",
        "explanation": "Die ausdrücklich genannte Dyslexie erhöht die modellierte Leseschwierigkeit.",
        "confidence": "high",
    },
    "attention_stability": {
        "value": 35,
        "scale_min_description": "0 = sehr instabile Aufmerksamkeit",
        "scale_max_description": "100 = sehr stabile Aufmerksamkeit",
        "explanation": "Das Nutzerprofil legt eine reduzierte Stabilität nahe.",
        "confidence": "medium",
    },
    "distraction_sensitivity": {
        "value": 80,
        "scale_min_description": "0 = kaum empfindlich gegenüber Ablenkungen",
        "scale_max_description": "100 = sehr empfindlich gegenüber Ablenkungen",
        "explanation": "Ablenkungen sind für dieses Nutzerprofil besonders relevant.",
        "confidence": "medium",
    },
    "task_switching_difficulty": {
        "value": 65,
        "scale_min_description": "0 = sehr leichter Wechsel zwischen Schritten",
        "scale_max_description": "100 = sehr schwieriger Wechsel zwischen Schritten",
        "explanation": "Der Prozess enthält mehrere Teilschritte.",
        "confidence": "medium",
    },
    "working_memory_stability": {
        "value": 45,
        "scale_min_description": "sehr instabil",
        "scale_max_description": "sehr stabil",
        "explanation": "Fester Profilwert.",
        "confidence": "high",
    },
    "assumptions": [
        "Das Nutzerprofil wird nur als Simulationsannahme interpretiert.",
        "Ablenkungen können die Aufmerksamkeit stärker beeinflussen.",
    ],
}


MOCK_TASK_MODEL = {
    "task_name": "Urlaubsantrag ausfüllen",
    "task_goal": "Urlaubsantrag vollständig prüfen und absenden",
    "task_complexity": {
        "value": 55,
        "scale_min_description": "0 = sehr einfache Einzelhandlung",
        "scale_max_description": "100 = sehr komplexer mehrstufiger Prozess",
        "explanation": "Der Urlaubsantrag besteht aus mehreren abhängigen Schritten.",
        "confidence": "high",
    },
    "number_of_steps": {
        "value": 6,
        "scale_min_description": "0 = keine relevanten Bearbeitungsschritte",
        "scale_max_description": "100 = sehr viele Bearbeitungsschritte",
        "explanation": "Die HTA enthält sechs konkrete Bearbeitungsschritte.",
        "confidence": "high",
    },
    "reading_demand": {
        "value": 35,
        "scale_min_description": "0 = keine relevante Leseanforderung",
        "scale_max_description": "100 = sehr hohe Leseanforderung",
        "explanation": "Es müssen Hinweise und Zusammenfassung gelesen werden.",
        "confidence": "medium",
    },
    "input_demand": {
        "value": 60,
        "scale_min_description": "0 = keine Eingaben oder Auswahlen",
        "scale_max_description": "100 = sehr viele präzise Eingaben",
        "explanation": "Datumsauswahl und Prüfung erfordern mehrere Eingaben.",
        "confidence": "high",
    },
    "memory_demand": {
        "value": 45,
        "scale_min_description": "0 = keine Merkanforderung",
        "scale_max_description": "100 = sehr hohe Merkanforderung",
        "explanation": "Start- und Enddatum müssen im Zusammenhang geprüft werden.",
        "confidence": "medium",
    },
    "decision_demand": _attribute(
        50,
        "0 = keine Entscheidung erforderlich",
        "100 = sehr viele komplexe Entscheidungen",
        "Zeitraum und Begründung erfordern mehrere Entscheidungen.",
    ),
    "error_criticality": _attribute(
        60,
        "0 = Fehler bleiben ohne Auswirkung",
        "100 = Fehler verhindern den Aufgabenabschluss",
        "Fehlerhafte Antragsdaten können eine Korrektur erforderlich machen.",
    ),
    "steps": [
        {
            "step_id": "step_1",
            "name": "Hinweise zum Urlaubsantrag lesen",
            "goal": "Voraussetzungen und Hinweise verstehen",
            "step_type": "read",
            "description": "Nutzer:innen lesen die einleitenden Textabschnitte.",
            "goms_operations": ["perceive", "read", "think"],
            "estimated_duration_seconds": 20,
        },
        {
            "step_id": "step_2",
            "name": "Urlaubszeitraum auswählen",
            "goal": "Start- und Enddatum festlegen",
            "step_type": "select",
            "description": "Nutzer:innen wählen den gewünschten Zeitraum aus.",
            "goms_operations": ["perceive", "think", "point", "click", "verify"],
            "estimated_duration_seconds": 28,
        },
        {
            "step_id": "step_3",
            "name": "Persönliche Angaben ergänzen",
            "goal": "Erforderliche Personendaten vervollständigen",
            "step_type": "input",
            "description": "Nutzer:innen füllen die persönlichen Formularfelder aus.",
            "goms_operations": ["perceive", "point", "click", "type", "verify"],
            "estimated_duration_seconds": 30,
        },
        {
            "step_id": "step_4",
            "name": "Urlaubsantrag begründen",
            "goal": "Eine nachvollziehbare Begründung eingeben",
            "step_type": "input",
            "description": "Nutzer:innen verfassen die Begründung für den Antrag.",
            "goms_operations": ["think", "point", "click", "type", "verify"],
            "estimated_duration_seconds": 30,
        },
        {
            "step_id": "step_5",
            "name": "Antrag überprüfen",
            "goal": "Eingaben vor dem Absenden kontrollieren",
            "step_type": "check",
            "description": "Nutzer:innen prüfen Zeitraum, Angaben und Begründung.",
            "goms_operations": ["read", "think", "verify"],
            "estimated_duration_seconds": 25,
        },
        {
            "step_id": "step_6",
            "name": "Antrag absenden",
            "goal": "Geprüften Antrag abschicken",
            "step_type": "submit",
            "description": "Nutzer:innen klicken auf den Absenden-Button.",
            "goms_operations": ["point", "click", "wait"],
            "estimated_duration_seconds": 6,
        },
    ],
    "assumptions": [
        "Die Schrittfolge wird als spätere Simulationsreihenfolge verwendet.",
        "Die Zeitwerte sind heuristische GOMS-Schätzungen.",
    ],
}


MOCK_INTERFACE_MODEL = {
    "text_volume": {
        "value": 40,
        "scale_min_description": "0 = kaum sichtbarer Text",
        "scale_max_description": "100 = sehr viel sichtbarer Text",
        "explanation": "Ein Formular enthält moderate Textmengen.",
        "confidence": "medium",
    },
    "sentence_length": {
        "value": 35,
        "scale_min_description": "0 = sehr kurze Sätze",
        "scale_max_description": "100 = sehr lange Sätze",
        "explanation": "Die erwarteten Formulartexte sind eher kurz.",
        "confidence": "medium",
    },
    "word_difficulty": {
        "value": 25,
        "scale_min_description": "0 = sehr einfache Wörter",
        "scale_max_description": "100 = sehr schwierige Wörter",
        "explanation": "Urlaubsanträge verwenden meist bekannte Begriffe.",
        "confidence": "medium",
    },
    "technical_terms": {
        "value": 20,
        "scale_min_description": "0 = keine Fachbegriffe",
        "scale_max_description": "100 = sehr viele Fachbegriffe",
        "explanation": "Nur wenige organisatorische Begriffe sind wahrscheinlich.",
        "confidence": "medium",
    },
    "visual_clutter": {
        "value": 45,
        "scale_min_description": "0 = sehr ruhiges Interface",
        "scale_max_description": "100 = sehr unübersichtliches Interface",
        "explanation": "Kalender und Formularfelder erzeugen moderate visuelle Dichte.",
        "confidence": "medium",
    },
    "navigation_complexity": {
        "value": 35,
        "scale_min_description": "0 = keine Navigation nötig",
        "scale_max_description": "100 = sehr komplexe Navigation",
        "explanation": "Der Ablauf bleibt innerhalb eines Formularprozesses.",
        "confidence": "medium",
    },
    "accessibility_support": {
        "value": 55,
        "scale_min_description": "0 = keine Unterstützung",
        "scale_max_description": "100 = sehr starke Barrierefreiheitsunterstützung",
        "explanation": "Es wird moderate Unterstützung angenommen.",
        "confidence": "low",
    },
    "feedback_quality": {
        "value": 60,
        "scale_min_description": "0 = keine Rückmeldung",
        "scale_max_description": "100 = sehr klare Rückmeldung",
        "explanation": "Formulare bieten wahrscheinlich Status- oder Fehlermeldungen.",
        "confidence": "medium",
    },
    "assumptions": [
        "Das Formular besitzt moderate visuelle Komplexität.",
        "Systemfeedback ist vorhanden, aber nicht stark hervorgehoben.",
    ],
}


MOCK_ENVIRONMENT_MODEL = {
    "noise_level": {
        "value": 35,
        "scale_min_description": "0 = keine wahrnehmbare Geräuschbelastung",
        "scale_max_description": "100 = sehr starke Geräuschbelastung",
        "explanation": "Eine Büroumgebung hat meist moderate Geräusche.",
        "confidence": "medium",
    },
    "distractions": {
        "value": 55,
        "scale_min_description": "0 = keine Ablenkungen",
        "scale_max_description": "100 = sehr viele Ablenkungen",
        "explanation": "Gelegentliche Unterbrechungen sind plausibel.",
        "confidence": "medium",
    },
    "time_pressure": {
        "value": 60,
        "scale_min_description": "0 = kein Zeitdruck",
        "scale_max_description": "100 = sehr hoher Zeitdruck",
        "explanation": "Ein zeitlich begrenzter Prozess erzeugt erhöhten Druck.",
        "confidence": "high",
    },
    "context_stability": {
        "value": 70,
        "scale_min_description": "0 = sehr instabiler Kontext",
        "scale_max_description": "100 = sehr stabiler Kontext",
        "explanation": "Die Büroumgebung ist grundsätzlich vorhersehbar.",
        "confidence": "medium",
    },
    "visual_distraction": _attribute(
        65,
        "0 = keine visuellen Ablenkungen",
        "100 = sehr starke visuelle Ablenkungen",
        "Benachrichtigungen und andere Anwendungen können sichtbar sein.",
    ),
    "interruption_risk": _attribute(
        55,
        "0 = keine Unterbrechungen",
        "100 = sehr häufige Unterbrechungen",
        "Benachrichtigungen können die Bearbeitung unterbrechen.",
    ),
    "social_pressure": _attribute(
        20,
        "0 = kein sozialer Druck",
        "100 = sehr hoher sozialer Druck",
        "Sozialer Druck ist im Szenario nicht ausdrücklich beschrieben.",
        "low",
    ),
    "device_constraints": _attribute(
        25,
        "0 = keine Gerätebeschränkungen",
        "100 = sehr starke Gerätebeschränkungen",
        "Der Laptop bietet ausreichend Platz für das Formular.",
    ),
    "lighting_quality": _attribute(
        70,
        "0 = sehr schlechte Lichtbedingungen",
        "100 = optimale Lichtbedingungen",
        "Für den Arbeitsplatz wird übliche Bürobeleuchtung angenommen.",
        "low",
    ),
    "mobility_context": _attribute(
        10,
        "0 = vollständig stationäre Nutzung",
        "100 = Nutzung in ständiger Bewegung",
        "Die Nutzung am Laptop wird als stationär modelliert.",
    ),
    "assumptions": [
        "Die Nutzung findet in einer grundsätzlich stabilen Büroumgebung statt.",
        "Gelegentliche Unterbrechungen bleiben möglich.",
    ],
}


MOCK_COMPUTED_PARAMETERS = {
    "text_complexity": {
        "used_basis_attributes": [
            "interface_model.text_volume.value",
            "interface_model.sentence_length.value",
            "interface_model.word_difficulty.value",
            "interface_model.technical_terms.value",
        ],
        "used_weightings": [
            {"attribute": "interface_model.text_volume.value", "weight": 0.25},
            {"attribute": "interface_model.sentence_length.value", "weight": 0.25},
            {"attribute": "interface_model.word_difficulty.value", "weight": 0.25},
            {"attribute": "interface_model.technical_terms.value", "weight": 0.25},
        ],
        "formula": "0.25*text_volume + 0.25*sentence_length + 0.25*word_difficulty + 0.25*technical_terms",
        "value": 30,
        "explanation": "Die Textkomplexität ist moderat, weil Textumfang, Satzlänge, Wortschwierigkeit und Fachbegriffe begrenzt bleiben.",
    },
    "navigation_effort": {
        "used_basis_attributes": [
            "task_model.number_of_steps.value",
            "interface_model.visual_clutter.value",
            "interface_model.navigation_complexity.value",
        ],
        "used_weightings": [
            {"attribute": "task_model.number_of_steps.value", "weight": 0.3333},
            {"attribute": "interface_model.visual_clutter.value", "weight": 0.3333},
            {"attribute": "interface_model.navigation_complexity.value", "weight": 0.3333},
        ],
        "formula": "(number_of_steps + visual_clutter + navigation_complexity) / 3",
        "value": 28,
        "explanation": "Der Navigationsaufwand bleibt moderat, weil der Prozess mehrstufig, aber nicht stark verzweigt ist.",
    },
    "decoding_load": {
        "used_basis_attributes": ["reading_demand", "unfamiliar_word_density", "orthographic_irregularity", "morphological_complexity"],
        "used_weightings": [
            {"attribute": "reading_demand", "weight": 0.25},
            {"attribute": "unfamiliar_word_density", "weight": 0.25},
            {"attribute": "orthographic_irregularity", "weight": 0.25},
            {"attribute": "morphological_complexity", "weight": 0.25},
        ],
        "formula": "0.25 * reading_demand + 0.25 * unfamiliar_word_density + 0.25 * orthographic_irregularity + 0.25 * morphological_complexity",
        "value": 24,
        "explanation": "Der Dekodieraufwand bleibt niedrig bis moderat.",
    },
    "visual_reading_load": {
        "used_basis_attributes": ["text_density", "line_tracking_difficulty", "visual_clutter", "inverse_text_legibility"],
        "used_weightings": [
            {"attribute": "text_density", "weight": 0.25},
            {"attribute": "line_tracking_difficulty", "weight": 0.25},
            {"attribute": "visual_clutter", "weight": 0.25},
            {"attribute": "inverse_text_legibility", "weight": 0.25},
        ],
        "formula": "0.25 * text_density + 0.25 * line_tracking_difficulty + 0.25 * visual_clutter + 0.25 * (100 - text_legibility)",
        "value": 34,
        "explanation": "Die visuelle Lesebelastung ist moderat.",
    },
    "dyslexia_reading_load": {
        "used_basis_attributes": ["decoding_load", "visual_reading_load", "reading_demand", "text_complexity"],
        "used_weightings": [
            {"attribute": "decoding_load", "weight": 0.35},
            {"attribute": "visual_reading_load", "weight": 0.25},
            {"attribute": "reading_demand", "weight": 0.25},
            {"attribute": "text_complexity", "weight": 0.15},
        ],
        "formula": "0.35 * decoding_load + 0.25 * visual_reading_load + 0.25 * reading_demand + 0.15 * text_complexity",
        "value": 31,
        "explanation": "Die dyslexierelevante Lesebelastung bleibt im Beispiel moderat.",
    },
    "sustained_attention_load": {
        "used_basis_attributes": ["sustained_attention_demand", "time_pressure", "task_complexity", "distractions"],
        "used_weightings": [
            {"attribute": "sustained_attention_demand", "weight": 0.35},
            {"attribute": "time_pressure", "weight": 0.25},
            {"attribute": "task_complexity", "weight": 0.20},
            {"attribute": "distractions", "weight": 0.20},
        ],
        "formula": "0.35 * sustained_attention_demand + 0.25 * time_pressure + 0.20 * task_complexity + 0.20 * distractions",
        "value": 38,
        "explanation": "Die Daueraufmerksamkeitsbelastung ist moderat.",
    },
    "inhibition_load": {
        "used_basis_attributes": ["inhibition_demand", "irrelevant_signal_load", "visual_clutter", "feedback_interruptiveness"],
        "used_weightings": [
            {"attribute": "inhibition_demand", "weight": 0.35},
            {"attribute": "irrelevant_signal_load", "weight": 0.30},
            {"attribute": "visual_clutter", "weight": 0.20},
            {"attribute": "feedback_interruptiveness", "weight": 0.15},
        ],
        "formula": "0.35 * inhibition_demand + 0.30 * irrelevant_signal_load + 0.20 * visual_clutter + 0.15 * feedback_interruptiveness",
        "value": 32,
        "explanation": "Die Inhibitionsbelastung bleibt moderat.",
    },
    "attention_switching_load": {
        "used_basis_attributes": ["task_switching_demand", "navigation_complexity", "memory_demand", "divided_attention_demand"],
        "used_weightings": [
            {"attribute": "task_switching_demand", "weight": 0.35},
            {"attribute": "navigation_complexity", "weight": 0.25},
            {"attribute": "memory_demand", "weight": 0.20},
            {"attribute": "divided_attention_demand", "weight": 0.20},
        ],
        "formula": "0.35 * task_switching_demand + 0.25 * navigation_complexity + 0.20 * memory_demand + 0.20 * divided_attention_demand",
        "value": 43,
        "explanation": "Die Wechselbelastung ist moderat.",
    },
    "adhd_interaction_load": {
        "used_basis_attributes": ["sustained_attention_load", "inhibition_load", "attention_switching_load", "visual_clutter"],
        "used_weightings": [
            {"attribute": "sustained_attention_load", "weight": 0.30},
            {"attribute": "inhibition_load", "weight": 0.25},
            {"attribute": "attention_switching_load", "weight": 0.25},
            {"attribute": "visual_clutter", "weight": 0.20},
        ],
        "formula": "0.30 * sustained_attention_load + 0.25 * inhibition_load + 0.25 * attention_switching_load + 0.20 * visual_clutter",
        "value": 39,
        "explanation": "Die ADHS-relevante Interaktionsbelastung ist moderat.",
    },
    "assumptions": [
        "Zeitdruck und Ablenkbarkeit erhöhen vor allem Prüf- und Eingabeschritte.",
        "Die Basiswerte sind vorbereitende Simulationsinputs.",
    ],
}


def _mock_profile_result(
    profile_id,
    profile_label,
    attention,
    fatigue,
    reading_speed,
    cognitive_load,
    error_risk,
    recommendations,
):
    timeline = [
        {
            "timestamp": "00:01",
            "timestamp_seconds": 1,
            "current_task_step": {
                "step_id": "step_1",
                "name": "Hinweise lesen",
            },
            "reading_speed": reading_speed + 3,
            "attention": attention + 5,
            "fatigue": fatigue - 4,
            "cognitive_load": cognitive_load - 3,
            "error_risk": error_risk - 4,
            "task_success_score": 100 - error_risk,
            "completion_efficiency": 68,
            "events": [],
        },
        {
            "timestamp": "00:02",
            "timestamp_seconds": 2,
            "current_task_step": {
                "step_id": "step_2",
                "name": "Formulardaten eingeben",
            },
            "reading_speed": reading_speed,
            "attention": attention,
            "fatigue": fatigue,
            "cognitive_load": cognitive_load,
            "error_risk": error_risk,
            "task_success_score": 100 - error_risk,
            "completion_efficiency": 62,
            "events": [
                {
                    "event_type": "high_error_risk",
                    "step_id": "step_2",
                }
            ] if error_risk >= 60 else [],
        },
    ]
    events = [
        {
            **event,
            "timestamp": item["timestamp"],
        }
        for item in timeline
        for event in item["events"]
    ]
    return {
        "completed": True,
        "profile_id": profile_id,
        "profile_label": profile_label,
        "initial_user_state": {"attention": attention + 10, "fatigue": 10},
        "final_state": {
            "attention": attention,
            "fatigue": fatigue,
            "reading_speed": reading_speed,
        },
        "metrics": {
            "cognitive_load": cognitive_load,
            "error_risk": error_risk,
            "task_success_score": 100 - error_risk,
            "completion_efficiency": 62,
        },
        "events": events,
        "timeline": timeline,
        "logs": timeline,
        "problems": [f"{profile_label} zeigt erhöhte Belastung im Eingabeschritt."],
        "recommendations": recommendations,
    }


_MOCK_PROFILE_RESULTS = {
    "generic": _mock_profile_result(
        "generic",
        "Generic",
        72,
        32,
        74,
        48,
        38,
        ["Fortschrittsanzeige ergänzen."],
    ),
    "adhd": _mock_profile_result(
        "adhd",
        "ADHS",
        42,
        58,
        60,
        72,
        68,
        [
            "Visuelle Ablenkungen reduzieren.",
            "Fortschrittsanzeige ergänzen.",
        ],
    ),
    "dyslexie": _mock_profile_result(
        "dyslexie",
        "Dyslexie",
        61,
        49,
        43,
        66,
        57,
        ["Texte kürzen.", "Hilfetexte vereinfachen."],
    ),
}


MOCK_SIMULATION_RESULT = {
    "results": _MOCK_PROFILE_RESULTS["generic"],
    "logs": _MOCK_PROFILE_RESULTS["generic"]["timeline"],
    "simulation_results": {
        "completed": True,
        "profile_count": 3,
        "profile_ids": ["generic", "adhd", "dyslexie"],
        "baseline_profile_id": "generic",
        "results_by_profile": _MOCK_PROFILE_RESULTS,
        "runs": list(_MOCK_PROFILE_RESULTS.values()),
        "comparison_summary": {},
    },
}


MOCK_BASE_MODEL_PREVIEW = {
    "user_model": MOCK_USER_MODEL,
    "task_model": MOCK_TASK_MODEL,
    "interface_model": MOCK_INTERFACE_MODEL,
    "environment_model": MOCK_ENVIRONMENT_MODEL,
}

MOCK_USER_MODEL_PREVIEW = {
    "user_model": MOCK_USER_MODEL,
}

MOCK_TASK_MODEL_PREVIEW = {
    "task_model": MOCK_TASK_MODEL,
}

MOCK_INTERFACE_MODEL_PREVIEW = {
    "interface_model": MOCK_INTERFACE_MODEL,
}

MOCK_ENVIRONMENT_MODEL_PREVIEW = {
    "environment_model": MOCK_ENVIRONMENT_MODEL,
}

MOCK_SIMULATION_MODEL = {
    "time_step_seconds": 1,
    "initial_user_state": {"attention": 45, "fatigue": 10},
    "response_rates": {"attention": 1.0, "fatigue": 0.05},
    "event_thresholds": {
        "high_error_risk": 75,
        "very_high_cognitive_load": 80,
        "very_low_attention": 20,
        "high_dyslexia_reading_load": 65,
        "attention_lapse": 60,
        "high_inhibition_load": 65,
        "task_switching_strain": 65,
    },
    "model_weights": {
        "text_complexity": [0.25, 0.25, 0.25, 0.25],
        "navigation_effort": [1 / 3, 1 / 3, 1 / 3],
        "decoding_load": [0.25, 0.25, 0.25, 0.25],
        "visual_reading_load": [0.25, 0.25, 0.25, 0.25],
        "dyslexia_reading_load": [0.35, 0.25, 0.25, 0.15],
        "sustained_attention_load": [0.35, 0.25, 0.20, 0.20],
        "inhibition_load": [0.35, 0.30, 0.20, 0.15],
        "attention_switching_load": [0.35, 0.25, 0.20, 0.20],
        "adhd_interaction_load": [0.30, 0.25, 0.25, 0.20],
        "reading_speed": [0.25, 0.25, 0.25, 0.25],
        "attention": [1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6],
        "fatigue": [0.2, 0.2, 0.2, 0.2, 0.2],
        "cognitive_load": [0.2, 0.2, 0.2, 0.2, 0.2],
        "error_risk": [0.25, 0.25, 0.25, 0.25],
        "task_success_score": [1 / 3, 1 / 3, 1 / 3],
        "completion_efficiency": [1 / 3, 1 / 3, 1 / 3],
    },
    "task_step_modifiers": [],
    "assumptions": ["Standardkonfiguration für Frontend-Tests."],
}

MOCK_COMPUTED_PARAMETERS_PREVIEW = {
    "computed_parameters": MOCK_COMPUTED_PARAMETERS,
    "simulation_model": MOCK_SIMULATION_MODEL,
}
