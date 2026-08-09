from typing import List

from pydantic import BaseModel, Field


class ParameterWeightSchema(BaseModel):
    attribute: str
    weight: float


class ComputedParameterSchema(BaseModel):
    used_basis_attributes: List[str] = Field(default_factory=list)
    used_weightings: List[ParameterWeightSchema] = Field(default_factory=list)
    formula: str
    value: int = Field(..., ge=0, le=100)
    explanation: str


class ComputedParametersSchema(BaseModel):
    text_complexity: ComputedParameterSchema
    navigation_effort: ComputedParameterSchema
    decoding_load: ComputedParameterSchema
    visual_reading_load: ComputedParameterSchema
    dyslexia_reading_load: ComputedParameterSchema
    sustained_attention_load: ComputedParameterSchema
    inhibition_load: ComputedParameterSchema
    attention_switching_load: ComputedParameterSchema
    adhd_interaction_load: ComputedParameterSchema
    assumptions: List[str] = Field(default_factory=list)
