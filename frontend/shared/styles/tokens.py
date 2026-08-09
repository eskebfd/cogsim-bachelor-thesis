import base64
from pathlib import Path


def load_background_data_uri() -> str:
    frontend_root = Path(__file__).resolve().parents[2]
    background_path = frontend_root / "assets" / "cogsim-background.svg"
    encoded_background = base64.b64encode(background_path.read_bytes()).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded_background}"


def build_token_css() -> str:
    return """
        :root {
            --cogsim-bg: #F5F6F8;
            --cogsim-surface: #FFFFFF;
            --cogsim-surface-muted: #FBFAFF;
            --cogsim-border: #DEDBEA;
            --cogsim-border-strong: #C8C3DE;
            --cogsim-text: #171717;
            --cogsim-text-secondary: #3F3D56;
            --cogsim-text-muted: #6F6A80;
            --cogsim-text-subtle: #6F6A80;
            --cogsim-primary: #5B5BD6;
            --cogsim-primary-hover: #4848B8;
            --cogsim-primary-soft: #F1EEFF;
            --cogsim-success: #168A4A;
            --cogsim-warning: #B7791F;
            --cogsim-danger: #C2413B;
            --cogsim-info: #3E66C6;
            --cogsim-radius: 14px;
            --cogsim-shadow: 0 10px 28px rgba(47, 39, 92, 0.06);
        }
    """


def build_background_css() -> str:
    background_data_uri = load_background_data_uri()
    return f"""
        .stApp {{
            background:
                linear-gradient(
                    180deg,
                    rgba(245, 246, 248, 0.90) 0%,
                    rgba(245, 246, 248, 0.96) 44%,
                    rgba(245, 246, 248, 0.98) 100%
                ),
                radial-gradient(
                    circle at 14% 6%,
                    rgba(91, 91, 214, 0.08) 0,
                    rgba(91, 91, 214, 0) 34%
                ),
                url("{background_data_uri}");
            background-size: cover, auto, cover;
            background-position: center, center, center;
            background-attachment: fixed, fixed, fixed;
            background-repeat: no-repeat;
        }}

        [data-testid="stAppViewContainer"] > .main {{
            background: transparent;
        }}
    """
