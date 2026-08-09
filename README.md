# CogSim

CogSim ist ein Forschungsprototyp zur simulationsgestützten Analyse von
Nutzungsszenarien. Das System überführt natürlichsprachliche Beschreibungen und
optional Screenshots mithilfe eines Large Language Models in strukturierte
Modelle der Aufgabe, der Benutzungsschnittstelle und der Nutzungsumgebung.
Diese Modelle werden anschließend mit vordefinierten Nutzerprofilen kombiniert
und in einer deterministischen Simulation ausgewertet.

Der Prototyp wurde im Rahmen einer Bachelorarbeit in der Medieninformatik
entwickelt. Er dient der explorativen Unterstützung früher Gestaltungsphasen
und ersetzt keine empirische Usability- oder Accessibility-Evaluation mit
realen Nutzer:innen.

## Voraussetzungen

- Python 3.12
- Ein OpenAI-API-Key oder ein OpenAI-kompatibler lokaler LLM-Endpunkt

Die Python-Abhängigkeiten sind in `requirements.txt` definiert.

## Installation

Repository klonen und in das Projektverzeichnis wechseln:

```bash
git clone https://github.com/eskebfd/cogsim-bachelor-thesis.git
cd cogsim-bachelor-thesis
```

Virtuelle Umgebung erstellen und aktivieren:

```bash
python -m venv .venv
source .venv/bin/activate
```

Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

Lokale Konfigurationsdatei anlegen:

```bash
cp .env.example .env
```

Echte API-Keys dürfen nicht in das Repository committed werden.

## Konfiguration

Für die Standardkonfiguration mit OpenAI wird in `.env` ein API-Key gesetzt:

```text
OPENAI_API_KEY=<eigener-api-key>
```

Weitere optionale Variablen sind in `.env.example` dokumentiert.

## LLM-Konfiguration

Die LLM-Anbindung erfolgt im Backend über einen OpenAI-kompatiblen Chat-Client
in `backend/core/llm/client.py`. Ohne zusätzliche Konfiguration verwendet
CogSim das Modell `gpt-4o-mini` und den Wert aus `OPENAI_API_KEY`.

Optional können Modellname, Base URL und API-Key über neutrale Variablen
überschrieben werden:

```text
LLM_MODEL=<modellname>
LLM_BASE_URL=<openai-kompatible-base-url>
LLM_API_KEY=<api-key>
```

Wenn `LLM_API_KEY` nicht gesetzt ist, wird `OPENAI_API_KEY` verwendet.

Ein lokal über Ollama bereitgestelltes Modell kann genutzt werden, sofern es
über die OpenAI-kompatible Schnittstelle erreichbar ist und die benötigten
strukturierten Ausgaben zuverlässig erzeugt. Ollama muss dafür lokal laufen und
das gewünschte Modell muss vorher verfügbar sein.

Beispiel:

```text
LLM_MODEL=llama3.1
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
```

## Anwendung starten

Die Befehle werden aus dem Projektverzeichnis heraus ausgeführt.

Backend starten:

```bash
uvicorn backend.main:app --reload --port 8000
```

Frontend in einem zweiten Terminal starten:

```bash
python -m streamlit run frontend/app.py
```

Das Frontend ruft die Backend-API unter `http://127.0.0.1:8000` auf. Der
zentrale Workflow-Endpunkt ist `/workflow/dispatch`.

## Tests ausführen

Die Testsuite kann mit folgendem Befehl ausgeführt werden:

```bash
pytest -q
```

Für lokale Testläufe ohne echten API-Key kann ein Dummy-Wert gesetzt werden:

```bash
OPENAI_API_KEY=test pytest -q
```

Die vorhandenen Tests sind so aufgebaut, dass keine realen externen LLM-Aufrufe
ausgeführt werden.

## Projektstruktur

```text
backend/      FastAPI-Backend, Workflow, LLM-Anbindung, Domänenlogik und Simulation
frontend/     Streamlit-Frontend und UI-Komponenten
tests/        Unit- und Integrationstests
```

Wichtige Backend-Bereiche:

```text
backend/api/          API-Routen
backend/core/         LLM-Client, Prompt-Laden und Logging
backend/domains/      Fachliche Domänen für Modelle, Planung, Simulation und Profile
backend/prompts/      Prompt-Vorlagen
backend/transport/    Request- und Response-Schemata
backend/workflow/     LangGraph-Workflow und gemeinsamer Workflow-State
```

## Lizenz

Im Repository ist aktuell keine Lizenzdatei enthalten.
