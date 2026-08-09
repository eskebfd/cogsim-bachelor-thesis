import streamlit as st

from frontend.shared.ui.icons import render_icon

PROFILE_OPTIONS = [
    "Generisch",
    "ADHS",
    "Dyslexie",
]

PROFILE_SELECTION_CHANGED_FLAG = "_user_profiles_changed"

PROFILE_CARD_CONTENT = {
    "Generisch": {
        "title": "Generic",
        "description": (
            "Referenzprofil ohne spezifische Einschränkungen. "
            "Dient als Vergleichsbasis für alle Simulationen."
        ),
        "footer_label": "Baseline",
        "icon": "user",
    },
    "ADHS": {
        "title": "ADHS",
        "description": (
            "Simuliert ein Nutzerprofil mit erhöhter Ablenkbarkeit "
            "und geringerer Aufmerksamkeitsstabilität."
        ),
        "footer_label": "ADHS auswählen",
        "icon": "user",
    },
    "Dyslexie": {
        "title": "Dyslexie",
        "description": (
            "Simuliert ein Nutzerprofil mit erhöhtem Aufwand "
            "beim Lesen und Verarbeiten von Texten."
        ),
        "footer_label": "Dyslexie auswählen",
        "icon": "user",
    },
}


def normalize_user_profiles(
    selected_profiles: list[str],
) -> list[str]:
    selected = list(dict.fromkeys(selected_profiles or ["Generisch"]))

    if "Generisch" not in selected:
        selected.insert(0, "Generisch")

    return [profile for profile in PROFILE_OPTIONS if profile in selected]


def toggle_user_profile(
    current_profiles: list[str],
    profile: str,
) -> list[str]:
    profiles = normalize_user_profiles(current_profiles)

    if profile == "Generisch":
        return profiles

    if profile in profiles:
        profiles = [item for item in profiles if item != profile]
    else:
        profiles = [*profiles, profile]

    return normalize_user_profiles(profiles)


def update_user_profile_selection(profile: str) -> None:
    current_profiles = st.session_state.get(
        "user_profiles",
        ["Generisch"],
    )

    next_profiles = toggle_user_profile(
        current_profiles,
        profile,
    )

    if next_profiles != normalize_user_profiles(current_profiles):
        st.session_state.user_profiles = next_profiles
        st.session_state[PROFILE_SELECTION_CHANGED_FLAG] = True


def _profile_slug(profile: str) -> str:
    return (
        profile.lower()
        .replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
        .replace(" ", "_")
        .replace("-", "_")
    )


def _build_profile_content_html(
    profile: str,
    selected: bool,
) -> str:
    content = PROFILE_CARD_CONTENT[profile]

    state_classes = [
        "cogsim-profile-card__content",
    ]

    if selected:
        state_classes.append("is-selected")

    if profile == "Generisch":
        state_classes.append("is-baseline")

    class_names = " ".join(state_classes)

    icon_html = render_icon(
        content["icon"],
        size=34,
        stroke_width=1.7,
        label=f'{content["title"]} Profil',
    )

    check_html = ""

    if selected:
        check_html = (
            '<div class="cogsim-profile-card__check">'
            f'{render_icon("check", size=13, stroke_width=2.5)}'
            "</div>"
        )

    return (
        f'<div class="{class_names}">'
        f"{check_html}"
        '<div class="cogsim-profile-card__icon">'
        f"{icon_html}"
        "</div>"
        '<div class="cogsim-profile-card__title">'
        f'{content["title"]}'
        "</div>"
        '<div class="cogsim-profile-card__description">'
        f'{content["description"]}'
        "</div>"
        "</div>"
    )


def _render_profile_card(
    profile: str,
    selected: bool,
) -> None:
    content = PROFILE_CARD_CONTENT[profile]
    slug = _profile_slug(profile)
    state = "selected" if selected else "idle"

    with st.container(key=f"profile_option_{slug}_{state}"):
        card_html = _build_profile_content_html(
            profile=profile,
            selected=selected,
        )

        st.markdown(
            card_html,
            unsafe_allow_html=True,
        )

        if profile == "Generisch":
            st.markdown(
                (
                    '<div class="cogsim-profile-card__footer '
                    'is-static">'
                    f'{content["footer_label"]}'
                    "</div>"
                ),
                unsafe_allow_html=True,
            )
            return

        button_label = (
            f"{content['title']} abwählen" if selected else content["footer_label"]
        )

        st.button(
            button_label,
            key=f"profile_card_button_{slug}",
            use_container_width=True,
            on_click=update_user_profile_selection,
            args=(profile,),
        )


def render_user_profiles_section() -> list[str]:
    profiles = normalize_user_profiles(
        st.session_state.get(
            "user_profiles",
            ["Generisch"],
        )
    )

    st.markdown(
        (
            '<div class="cogsim-user-profiles-intro">'
            '<div class="cogsim-user-profiles-intro__title">'
            "Welche Perspektiven sollen verglichen werden?"
            "</div>"
            '<div class="cogsim-user-profiles-intro__text">'
            "Wähle die Nutzerprofile aus, für die CogSim dein Szenario "
            "simulieren soll. Das generische Profil bleibt als Vergleichsbasis "
            "immer aktiv."
            "</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    columns = st.columns(
        len(PROFILE_OPTIONS),
        gap="medium",
    )

    for column, profile in zip(
        columns,
        PROFILE_OPTIONS,
    ):
        with column:
            _render_profile_card(
                profile=profile,
                selected=profile in profiles,
            )

    return profiles
