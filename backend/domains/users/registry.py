from backend.domains.users.profiles import (
    ADHD_PROFILE,
    DYSLEXIA_PROFILE,
    GENERIC_PROFILE,
)
from backend.domains.users.schemas.profile_definition import UserProfileDefinition


class UserProfileRegistry:
    def __init__(self) -> None:
        self._profiles: dict[str, UserProfileDefinition] = {}
        self._baseline_profile_id: str | None = None

    def register(
        self,
        profile: UserProfileDefinition,
        *,
        baseline: bool | None = None,
    ) -> None:
        if profile.profile_id in self._profiles:
            raise ValueError(f"User profile already registered: {profile.profile_id}")

        is_baseline = profile.is_baseline if baseline is None else baseline
        if is_baseline and self._baseline_profile_id is not None:
            raise ValueError(
                "Baseline user profile already registered: "
                f"{self._baseline_profile_id}"
            )

        stored_profile = profile.model_copy(
            update={"is_baseline": is_baseline},
            deep=True,
        )
        self._profiles[stored_profile.profile_id] = stored_profile
        if stored_profile.is_baseline:
            self._baseline_profile_id = stored_profile.profile_id

    def list_profiles(self) -> list[UserProfileDefinition]:
        return [profile.model_copy(deep=True) for profile in self._profiles.values()]

    def get(self, profile_id: str) -> UserProfileDefinition | None:
        profile = self._profiles.get(profile_id)
        return profile.model_copy(deep=True) if profile is not None else None

    def require(self, profile_id: str) -> UserProfileDefinition:
        profile = self.get(profile_id)
        if profile is None:
            raise ValueError(f"Unknown user profile ID: {profile_id}")
        return profile

    def baseline(self) -> UserProfileDefinition:
        if self._baseline_profile_id is None:
            raise ValueError("No baseline user profile registered.")
        return self.require(self._baseline_profile_id)

    def baseline_profile_id(self) -> str:
        return self.baseline().profile_id

    def validate_ids(self, profile_ids: list[str]) -> None:
        unknown_ids = [
            profile_id
            for profile_id in profile_ids
            if profile_id not in self._profiles
        ]
        if unknown_ids:
            raise ValueError("Unknown user profile IDs: " + ", ".join(unknown_ids))


def build_default_user_profile_registry() -> UserProfileRegistry:
    registry = UserProfileRegistry()
    registry.register(GENERIC_PROFILE)
    registry.register(ADHD_PROFILE)
    registry.register(DYSLEXIA_PROFILE)
    return registry


USER_PROFILE_REGISTRY = build_default_user_profile_registry()


def register_user_profile(
    profile: UserProfileDefinition,
    *,
    baseline: bool | None = None,
    registry: UserProfileRegistry = USER_PROFILE_REGISTRY,
) -> None:
    registry.register(profile, baseline=baseline)


def list_user_profiles(
    registry: UserProfileRegistry = USER_PROFILE_REGISTRY,
) -> list[UserProfileDefinition]:
    return registry.list_profiles()


def get_user_profile(
    profile_id: str,
    registry: UserProfileRegistry = USER_PROFILE_REGISTRY,
) -> UserProfileDefinition | None:
    return registry.get(profile_id)


def require_user_profile(
    profile_id: str,
    registry: UserProfileRegistry = USER_PROFILE_REGISTRY,
) -> UserProfileDefinition:
    return registry.require(profile_id)


def get_baseline_user_profile(
    registry: UserProfileRegistry = USER_PROFILE_REGISTRY,
) -> UserProfileDefinition:
    return registry.baseline()


def get_baseline_user_profile_id(
    registry: UserProfileRegistry = USER_PROFILE_REGISTRY,
) -> str:
    return registry.baseline_profile_id()


def validate_user_profile_ids(
    profile_ids: list[str],
    registry: UserProfileRegistry = USER_PROFILE_REGISTRY,
) -> None:
    registry.validate_ids(profile_ids)
