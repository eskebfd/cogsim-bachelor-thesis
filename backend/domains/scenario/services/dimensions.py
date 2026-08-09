from backend.core.llm.client import extract_scenario_dimensions
from backend.domains.scenario.schemas.dimensions import ScenarioDimensionsSchema
from backend.domains.scenario.schemas.multimodal import ScenarioImagePayload


def analyze_scenario_dimensions(
    scenario_description: str,
    scenario_image: ScenarioImagePayload | dict | None = None,
) -> ScenarioDimensionsSchema:
    """Analyze scenario text and optional screenshot into scenario dimensions."""
    return extract_scenario_dimensions(
        scenario_description,
        scenario_image,
    )
