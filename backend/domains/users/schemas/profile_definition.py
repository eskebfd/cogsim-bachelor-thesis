from pydantic import BaseModel, ConfigDict, Field


class UserProfileBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UserProfileAttribute(UserProfileBaseModel):
    attribute_id: str = Field(
        ...,
        min_length=1,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="Stabile technische ID des Profilattributs.",
    )
    name: str = Field(..., min_length=1, description="Lesbarer Attributname.")
    value: float = Field(
        ...,
        ge=0,
        le=100,
        description="Feste Profilannahme auf einer Skala von 0 bis 100.",
    )
    description: str | None = Field(
        None,
        description="Optionale Erläuterung der fachlichen Bedeutung.",
    )


class UserProfileDefinition(UserProfileBaseModel):
    profile_id: str = Field(
        ...,
        min_length=1,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="Stabile technische ID des Nutzerprofils.",
    )
    label: str = Field(..., min_length=1, description="Lesbarer Profilname.")
    is_baseline: bool = Field(
        False,
        description="Kennzeichnet das generische Vergleichsprofil.",
    )
    attributes: dict[str, UserProfileAttribute] = Field(
        ...,
        min_length=1,
        description="Feste, einheitlich strukturierte Profilattribute.",
    )
