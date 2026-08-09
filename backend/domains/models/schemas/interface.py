from typing import List

from pydantic import BaseModel, Field

from backend.domains.models.schemas.attribute import AttributeValueSchema


def _attribute_default(
    value: int,
    minimum: str,
    maximum: str,
) -> AttributeValueSchema:
    return AttributeValueSchema(
        value=value,
        scale_min_description=minimum,
        scale_max_description=maximum,
        explanation="Kompatibler Standardwert für ältere Interface-Model-Payloads.",
        confidence="medium",
    )


class InterfaceModelSchema(BaseModel):
    text_volume: AttributeValueSchema = Field(
        ...,
        description="Menge sichtbaren oder zu verarbeitenden Texts.",
    )

    sentence_length: AttributeValueSchema = Field(
        ...,
        description="Komplexität durch Satzlänge und Textstruktur.",
    )

    word_difficulty: AttributeValueSchema = Field(
        ...,
        description="Schwierigkeit der verwendeten Wörter.",
    )

    technical_terms: AttributeValueSchema = Field(
        ...,
        description="Anteil oder Relevanz technischer bzw. fachlicher Begriffe.",
    )

    visual_clutter: AttributeValueSchema = Field(
        ...,
        description="Visuelle Unruhe oder Dichte gleichzeitiger Elemente.",
    )

    navigation_complexity: AttributeValueSchema = Field(
        ...,
        description="Komplexität der Navigation oder Orientierung im Interface.",
    )

    accessibility_support: AttributeValueSchema = Field(
        ...,
        description="Ausmaß unterstützender Barrierefreiheits- oder Hilfefunktionen.",
    )

    feedback_quality: AttributeValueSchema = Field(
        ...,
        description="Qualität von Rückmeldungen, Fehlermeldungen und Statusinformationen.",
    )

    text_legibility: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            75,
            "Text ist sehr schwer lesbar",
            "Text ist sehr gut lesbar",
        ),
        description="Lesbarkeit durch Schriftgröße, Kontrast, Zeilenhöhe und typografische Klarheit.",
    )

    text_density: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            35,
            "Sehr luftige und leicht erfassbare Textstruktur",
            "Sehr dichte Textstruktur mit hoher Informationsmenge",
        ),
        description="Dichte und visuelle Konzentration der Textinformationen.",
    )

    line_tracking_difficulty: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            25,
            "Zeilen und Textabschnitte sind sehr leicht zu verfolgen",
            "Zeilen und Textabschnitte sind sehr schwer zu verfolgen",
        ),
        description="Schwierigkeit, Zeilen oder Textbereiche visuell stabil zu verfolgen.",
    )

    stimulus_density: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            35,
            "Sehr wenige gleichzeitige Reize",
            "Sehr viele gleichzeitige visuelle oder interaktive Reize",
        ),
        description="Dichte gleichzeitig sichtbarer Reize, Optionen und Interface-Elemente.",
    )

    irrelevant_signal_load: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            25,
            "Kaum irrelevante Signale oder Ablenkungen",
            "Sehr viele irrelevante Signale, Banner oder konkurrierende Hinweise",
        ),
        description="Belastung durch irrelevante oder konkurrierende Interface-Signale.",
    )

    feedback_interruptiveness: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            25,
            "Feedback unterbricht den Fokus kaum",
            "Feedback, Popups oder Statushinweise unterbrechen den Fokus stark",
        ),
        description="Ausmaß, in dem Rückmeldungen oder Hinweise den Fokus unterbrechen.",
    )

    focus_guidance: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            65,
            "Oberfläche führt den Fokus kaum",
            "Oberfläche führt den Fokus sehr klar zum nächsten Schritt",
        ),
        description="Klarheit, mit der das Interface Aufmerksamkeit und nächsten Handlungsschritt lenkt.",
    )

    assumptions: List[str] = Field(
        default_factory=list,
        description="Kurze Annahmen zur Herleitung der Interface-Werte.",
    )
