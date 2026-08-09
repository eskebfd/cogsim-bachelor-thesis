LOADING_OVERLAY_CSS = """
    .cogsim-loading-overlay {
        position: fixed;
        inset: 0;
        z-index: 999999;

        display: flex;
        align-items: center;
        justify-content: center;

        padding: 1.5rem;

        background:
            linear-gradient(
                180deg,
                rgba(245, 246, 248, 0.74) 0%,
                rgba(245, 246, 248, 0.82) 100%
            );

        backdrop-filter: blur(7px);
        -webkit-backdrop-filter: blur(7px);

        pointer-events: auto;
    }

    .cogsim-loading-overlay__panel {
        width: min(390px, calc(100vw - 3rem));

        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.78rem;

        padding: 1.6rem 1.5rem;

        border: 1px solid rgba(222, 219, 234, 0.88);
        border-radius: 18px;

        background: rgba(255, 255, 255, 0.92);
        box-shadow: 0 18px 48px rgba(47, 39, 92, 0.14);

        text-align: center;
    }

    .cogsim-loading-overlay__mascot-track {
        position: relative;

        width: 100%;
        height: 34px;

        overflow: hidden;

        border: 1px solid rgba(91, 91, 214, 0.12);
        border-radius: 999px;

        background:
            linear-gradient(
                180deg,
                rgba(238, 242, 255, 0.9) 0%,
                rgba(255, 255, 255, 0.82) 100%
            );
    }

    .cogsim-loading-overlay__mascot-track::after {
        content: "";
        position: absolute;
        right: 0.8rem;
        bottom: 0.62rem;
        left: 0.8rem;

        height: 1px;

        background:
            repeating-linear-gradient(
                90deg,
                rgba(91, 91, 214, 0.22) 0 8px,
                transparent 8px 15px
            );
    }

    .cogsim-loading-overlay__mascot {
        position: absolute;
        bottom: 0.26rem;
        left: 0;
        z-index: 1;

        animation:
            cogsim-loading-dino-run var(--cogsim-loading-duration, 18s)
                linear forwards,
            cogsim-loading-dino-bob 0.42s ease-in-out infinite;
    }

    .cogsim-pixel-dino {
        position: relative;
        display: block;

        width: 28px;
        height: 22px;
    }

    .cogsim-pixel-dino span {
        position: absolute;
        display: block;

        background: var(--cogsim-primary);
        border-radius: 2px;
        box-shadow: 0 1px 0 rgba(47, 39, 92, 0.16);
    }

    .cogsim-pixel-dino__body {
        width: 16px;
        height: 10px;

        left: 6px;
        top: 8px;
    }

    .cogsim-pixel-dino__head {
        width: 11px;
        height: 10px;

        left: 16px;
        top: 3px;
    }

    .cogsim-pixel-dino__tail {
        width: 9px;
        height: 5px;

        left: 0;
        top: 9px;

        transform: rotate(-22deg);
        transform-origin: right center;
    }

    .cogsim-pixel-dino__leg {
        width: 4px;
        height: 7px;

        top: 16px;
    }

    .cogsim-pixel-dino__leg--front {
        left: 17px;
        animation: cogsim-loading-dino-leg-front 0.42s steps(2, end) infinite;
    }

    .cogsim-pixel-dino__leg--back {
        left: 9px;
        animation: cogsim-loading-dino-leg-back 0.42s steps(2, end) infinite;
    }

    .cogsim-pixel-dino__eye {
        width: 2px;
        height: 2px;

        left: 23px;
        top: 6px;

        background: var(--cogsim-surface) !important;
        box-shadow: none !important;
    }

    .cogsim-loading-overlay__message {
        color: var(--cogsim-text);

        font-size: 0.92rem;
        font-weight: 700;
        letter-spacing: -0.015em;
        line-height: 1.35;
    }

    .cogsim-loading-overlay__estimate {
        color: var(--cogsim-text-secondary);

        font-size: 0.72rem;
        font-weight: 650;
        line-height: 1.3;
    }

    .cogsim-loading-overlay__progress {
        position: relative;

        width: 100%;
        height: 8px;

        overflow: hidden;

        border-radius: 999px;
        background: rgba(91, 91, 214, 0.10);
    }

    .cogsim-loading-overlay__progress-bar {
        position: absolute;
        inset: 0 auto 0 0;

        width: 8%;

        border-radius: inherit;
        background:
            linear-gradient(
                90deg,
                rgba(91, 91, 214, 0.72) 0%,
                var(--cogsim-primary) 62%,
                rgba(124, 77, 255, 0.72) 100%
            );

        box-shadow: 0 0 12px rgba(91, 91, 214, 0.18);

        animation:
            cogsim-loading-progress var(--cogsim-loading-duration, 18s)
                linear forwards,
            cogsim-loading-progress-pulse 1.1s ease-in-out infinite;
    }

    .cogsim-loading-overlay__hint {
        max-width: 28ch;

        color: var(--cogsim-text-muted);

        font-size: 0.76rem;
        line-height: 1.45;
    }

    @keyframes cogsim-loading-dino-run {
        0% {
            left: 0;
        }

        100% {
            left: calc(92% - 1.65rem);
        }
    }

    @keyframes cogsim-loading-dino-bob {
        0% {
            margin-bottom: 0;
        }

        50% {
            margin-bottom: 0.16rem;
        }

        100% {
            margin-bottom: 0;
        }
    }

    @keyframes cogsim-loading-dino-leg-front {
        0%,
        100% {
            height: 7px;
        }

        50% {
            height: 4px;
        }
    }

    @keyframes cogsim-loading-dino-leg-back {
        0%,
        100% {
            height: 4px;
        }

        50% {
            height: 7px;
        }
    }

    @keyframes cogsim-loading-progress {
        0% {
            width: 8%;
        }

        100% {
            width: 92%;
        }
    }

    @keyframes cogsim-loading-progress-pulse {
        0%,
        100% {
            filter: brightness(1);
        }

        50% {
            filter: brightness(1.08);
        }
    }
"""
