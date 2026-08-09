# CODE_GUIDE

## 1. Zweck der Dokumentation

Diese Datei dient als kompakte Orientierungshilfe für den Quellcode des
CogSim-Prototyps. Sie ergänzt die `README.md`, wiederholt jedoch nicht die
Installations- und Startanweisungen. Während die `README.md` den Betrieb der
Anwendung beschreibt, erläutert dieser Code Guide die fachliche Struktur des
Repositorys und benennt die wichtigsten Einstiegspunkte für das Verständnis der
Implementierung.

Die Dokumentation richtet sich an Personen, die den Quellcode im Kontext der
Bachelorarbeit nachvollziehen möchten. Sie stellt kein vollständiges API- oder
Entwicklerhandbuch dar, sondern beschreibt die zentralen Komponenten, ihre
Verantwortlichkeiten und den typischen Ablauf eines Simulationsdurchlaufs.

Die folgenden Ebenen bilden den grundlegenden technischen Zusammenhang:

```text
Benutzungsschnittstelle
        │
        ▼
Frontend (Streamlit)
        │
        ▼
Backend (FastAPI)
        │
        ▼
Workflow (LangGraph)
        │
        ├──────────────► LLM-gestützte Modellkonstruktion
        │
        └──────────────► Deterministische Simulation
```

## 2. Projektstruktur

Das Repository ist in Backend, Frontend, Prompt-Vorlagen und Tests gegliedert.
Die Struktur folgt einer Trennung zwischen fachlicher Verarbeitung,
Benutzungsoberfläche und LLM-gestützter Modellkonstruktion.

```text
backend/          FastAPI-Backend, Workflow, LLM-Anbindung und Domänenlogik
frontend/         Streamlit-Frontend, Workflowseiten und Ergebnisdarstellung
backend/prompts/  Prompt-Vorlagen für Szenarioanalyse, Modellgenerierung und Revision
tests/            Unit- und Integrationstests
```

Der Ordner `backend/domains/` enthält die fachlichen Teilbereiche des Systems.
Dazu gehören Szenarioanalyse, Modellkonstruktion, Planung, Simulation,
Evaluation und Nutzerprofile. Die technische Workflow-Orchestrierung erfolgt in
`backend/workflow/`, während die funktionsbezogenen Frontend-Ansichten unter
`frontend/features/` organisiert sind.

## 3. Wichtige Einstiegspunkte

### Backend

Der Backend-Einstiegspunkt befindet sich in `backend/main.py`. Dort wird die
FastAPI-Anwendung erzeugt und die API-Routen werden eingebunden. Die eigentliche
fachliche Verarbeitung erfolgt nicht direkt in dieser Datei, sondern wird über
Routen, Workflow-Nodes und Domänenmodule weitergeleitet.

Die zentrale API-Route befindet sich in `backend/api/routes.py`. Dort wird der
Workflow-Endpunkt `/workflow/dispatch` bereitgestellt. Dieser Endpunkt nimmt
Workflow-Kommandos aus dem Frontend entgegen, aktualisiert den Workflow-State
und gibt strukturierte Antworten an das Frontend zurück.

### Frontend

Der Frontend-Einstiegspunkt befindet sich in `frontend/app.py`. Diese Datei
initialisiert die Streamlit-Anwendung, lädt zentrale Styles und rendert die
aktuelle Ansicht des Analyseworkflows.

Der gemeinsame Frontend-State wird in `frontend/state.py` verwaltet. Dort liegen
unter anderem das Default-Szenario, die Initialisierung der Session-Werte und
Hilfsfunktionen zur Übertragung von Workflow-Ergebnissen in den Frontend-State.

### Workflow

Der zustandsbasierte Workflow wird in `backend/workflow/graph.py` aufgebaut.
Die Datei definiert den LangGraph-Workflow, registriert die Verarbeitungsschritte
als Nodes und legt fest, welche Übergänge zwischen Szenarioanalyse,
Modellgenerierung, Revision, Simulation und Ergebnisaufbereitung möglich sind.

Das gemeinsame State-Schema befindet sich in `backend/workflow/state.py`.
Dieser State bildet den Übergabevertrag zwischen den Workflow-Nodes und enthält
Szenariodaten, generierte Modelle, Simulationsgrundlagen, Ergebnisse und
Visualisierungsdaten.

## 4. Aufbau des Backends

### API und Transport

Die API-Schicht befindet sich in `backend/api/` und `backend/transport/`.
Während `backend/api/routes.py` die HTTP-Endpunkte bereitstellt, definieren die
Schemata in `backend/transport/schemas/` die Struktur der eingehenden und
ausgehenden Workflow-Nachrichten.

Diese Trennung ist wichtig, weil das Frontend nicht direkt auf fachliche
Backend-Funktionen zugreift. Stattdessen kommuniziert es über strukturierte
HTTP-Nachrichten mit dem Workflow.

### Workflow-Orchestrierung

Der Ordner `backend/workflow/` enthält die technische Orchestrierung des
Analyseprozesses. Die einzelnen Verarbeitungsschritte sind in
`backend/workflow/nodes/` abgelegt. Dort befinden sich unter anderem Nodes für
Szenarioanalyse, Modellkonstruktion, Planung, Simulation, Revision und
Ergebnisaufbereitung.

Die Datei `backend/workflow/routing.py` enthält die Bedingungen, anhand derer
der Workflow entscheidet, welcher Verarbeitungsschritt als Nächstes ausgeführt
wird. Dadurch können einzelne Schritte gezielt erneut ausgeführt werden,
beispielsweise nach einer manuellen Modellüberarbeitung.

### LLM-Anbindung und Prompt-Verwaltung

Die LLM-Anbindung befindet sich in `backend/core/llm/client.py`. Dort werden der
OpenAI-kompatible Chat-Client, strukturierte Ausgabemodelle und die gemeinsame
Fehlerbehandlung für LLM-Aufrufe gebündelt.

Die Prompttexte liegen nicht direkt im Produktivcode, sondern unter
`backend/prompts/`. Der Zugriff erfolgt über `backend/core/llm/prompt_loader.py`.
Diese Struktur trennt Prompt-Vorlagen von Programmlogik und erleichtert die
Nachvollziehbarkeit der LLM-gestützten Modellkonstruktion.

### Fachliche Domänen

Die fachlichen Bestandteile des Backends liegen unter `backend/domains/`.
Besonders relevant sind:

```text
backend/domains/scenario/    Szenario- und Screenshotanalyse
backend/domains/models/      Task-, Interface- und Environment-Modelle
backend/domains/planning/    Simulationsplan und abgeleitete Parameter
backend/domains/simulation/  Simulationsengine, Metriken, Events und Ergebnisse
backend/domains/users/       Vordefinierte Nutzerprofile
backend/domains/evaluation/  Auswahl und Beschreibung von Auswertungsmetriken
```

Diese Domänenstruktur verhindert, dass die gesamte fachliche Logik in einer
einzigen Service-Schicht zusammenläuft. Stattdessen sind Modellkonstruktion,
Planung, Simulation und Ergebnisaufbereitung als getrennte Verantwortlichkeiten
organisiert.

### Simulation

Die zentrale Simulationslogik befindet sich in `backend/domains/simulation/`.
Die Datei `backend/domains/simulation/engine.py` führt die zeitdiskrete
Simulation aus. Weitere Teilberechnungen liegen in Unterordnern wie
`algorithms/`, `metrics/` und `events/`.

Diese Aufteilung macht sichtbar, dass die Simulation nicht durch das
Sprachmodell ausgeführt wird. Die LLM-gestützte Modellkonstruktion erzeugt
strukturierte Eingangsmodelle, während die Simulation deterministisch auf Basis
dieser validierten Daten berechnet wird.

## 5. Aufbau des Frontends

Das Frontend ist als mehrstufiger Analyseworkflow umgesetzt. Die Steuerung der
Ansichten erfolgt über `frontend/workflow/`. Dort sind die Schritte des
Workflows, die Navigation und gemeinsame UI-Elemente des Prozessablaufs
definiert.

Die einzelnen fachlichen Ansichten liegen unter `frontend/features/`. Beispiele
sind:

```text
frontend/features/user_profiles/        Auswahl der Nutzerprofile
frontend/features/evaluation_goals/     Auswahl der Auswertungsmetriken
frontend/features/scenario/             Szenarioeingabe und Screenshot-Unterstützung
frontend/features/task_flow/            Prüfung des Aufgabenablaufs
frontend/features/dimensions/           Prüfung erkannter Anforderungen
frontend/features/models/               Prüfung der Simulationsgrundlagen
frontend/features/computed_parameters/  Simulationsplan und abgeleitete Werte
frontend/features/simulation/           Simulationsergebnisse
```

Die Ergebnisdarstellung ist innerhalb von `frontend/features/simulation/` weiter
unterteilt. Komponenten für Zusammenfassungen, Diagramme, Events und
Handlungsempfehlungen liegen in `components/`, während CSS-Fragmente unter
`styles/` organisiert sind. Gemeinsame Hilfsfunktionen befinden sich in
`utils/`.

Die Kommunikation mit dem Backend erfolgt über
`frontend/shared/services/workflow_api.py` und
`frontend/shared/services/workflow_payloads.py`. Dadurch bleibt die Darstellung
im Frontend von der konkreten Struktur der HTTP-Payloads getrennt.

## 6. Typischer Programmablauf

Ein vollständiger Durchlauf folgt im Prototyp einer festen fachlichen Struktur.
Die einzelnen Schritte werden technisch durch Frontend-Aktionen,
Backend-Kommandos und Workflow-Nodes umgesetzt.

Der Ablauf wird zustandsbasiert durch LangGraph orchestriert. Zwischen den
Verarbeitungsschritten erfolgt die Datenübergabe über einen gemeinsamen
Workflow-State.

1. Ein Nutzungsszenario wird im Frontend beschrieben. Optional kann ein
   Screenshot ergänzt werden.
2. Das Backend analysiert die Szenariobeschreibung und extrahiert strukturierte
   Signale zu Aufgabe, Benutzungsschnittstelle und Umgebung.
3. Aus den Signalen werden Task Model, Interface Model und Environment Model
   erzeugt.
4. Die generierten Modelle werden im Frontend angezeigt und können geprüft oder
   angepasst werden.
5. Aus den Modellwerten und den ausgewählten Nutzerprofilen wird ein
   Simulationsplan vorbereitet.
6. Abgeleitete Parameter werden deterministisch aus vorhandenen Modellwerten
   berechnet.
7. Die Simulationsengine verarbeitet den Aufgabenablauf zeitdiskret und erzeugt
   Zustände, Metriken, Events und Timeline-Daten.
8. Die Ergebnisse werden im Frontend als Profilvergleich, Verlauf,
   Eventübersicht und Handlungsempfehlungen dargestellt.

Der Ablauf verbindet damit LLM-gestützte Interpretation mit deterministischer
Simulation. Die Modellkonstruktion dient der strukturierten Vorbereitung der
Simulation; die eigentliche Simulationsberechnung erfolgt anschließend ohne
LLM-Aufruf.

## 7. Zentrale Implementierungsdateien

### `backend/main.py`

Diese Datei bildet den technischen Einstiegspunkt des Backends. Sie erstellt die
FastAPI-Anwendung und bindet die API-Routen ein. Für das Verständnis des
Systems ist sie relevant, weil hier sichtbar wird, welche Backend-Schnittstellen
nach außen bereitgestellt werden.

### `backend/api/routes.py`

Diese Datei enthält den zentralen Workflow-Endpunkt `/workflow/dispatch`. Dort
werden eingehende Workflow-Kommandos aus dem Frontend angenommen, in den
gemeinsamen State überführt und an den LangGraph-Workflow weitergegeben. Die
Datei ist damit die wichtigste Verbindung zwischen HTTP-Schnittstelle und
fachlichem Verarbeitungsprozess.

### `backend/workflow/graph.py`

Diese Datei definiert den zustandsbasierten Workflow. Sie zeigt, welche
Verarbeitungsschritte als Nodes registriert sind und wie der Ablauf zwischen
Szenarioanalyse, Modellgenerierung, Revision, Simulation und Ergebnisaufbereitung
strukturiert ist. Für das Verständnis der Gesamtarchitektur ist dies eine der
zentralen Dateien.

### `backend/workflow/state.py`

Diese Datei beschreibt den gemeinsamen Workflow-State. Der State enthält die
Zwischenergebnisse aller relevanten Verarbeitungsschritte und macht sichtbar,
welche Daten im Workflow zwischen Frontend, Modellkonstruktion und Simulation
weitergegeben werden.

### `backend/core/llm/client.py`

Diese Datei kapselt die technische LLM-Anbindung. Sie definiert den
OpenAI-kompatiblen Chat-Client und die strukturierten Ausgabemodelle, mit denen
Szenarioinformationen, Modelle und Screenshotinformationen erzeugt werden. Die
Datei ist besonders relevant, um die Grenze zwischen LLM-gestützter
Interpretation und deterministischer Simulation nachzuvollziehen.

### `backend/core/llm/prompt_loader.py`

Diese Datei verwaltet die Zuordnung zwischen Prompt-IDs und Prompt-Dateien. Sie
ist wichtig, weil die produktiv verwendeten Prompttexte zentral aus
`backend/prompts/` geladen werden und nicht verteilt im Python-Code definiert
sind.

### `backend/domains/planning/services/computed_parameters.py`

Diese Datei berechnet abgeleitete Parameter aus vorhandenen Modellwerten. Sie
ist relevant, weil hier die Zwischenschicht zwischen generierten Modellen und
Simulationsengine entsteht. Die Berechnungen erfolgen deterministisch und bilden
modellinterne Einflussgrößen wie Textkomplexität, Navigationsaufwand und weitere
Belastungswerte.

### `backend/domains/simulation/engine.py`

Diese Datei enthält die zeitdiskrete Simulationsengine. Dort wird der
Aufgabenablauf Schritt für Schritt verarbeitet. Zustandsaktualisierung,
Metrikberechnung, Eventprüfung, Fortschrittsberechnung und Timeline-Erzeugung
werden in einer definierten Reihenfolge koordiniert.

### `backend/domains/simulation/results.py`

Diese Datei aggregiert und strukturiert Simulationsergebnisse. Sie bildet eine
Schnittstelle zwischen der rohen Timeline der Simulation und den Datenstrukturen,
die später im Frontend für Profilvergleich, Detailansichten und Exporte
verwendet werden.

### `backend/domains/simulation/recommendations.py`

Diese Datei erzeugt regelbasierte Handlungsempfehlungen auf Basis der
Simulationsergebnisse. Sie ist relevant, weil dort auffällige Metriken, Events
und Arbeitsschritte in strukturierte Hinweise für die Ergebnisdarstellung
überführt werden.

### `backend/domains/users/registry.py`

Diese Datei verwaltet die vordefinierten Nutzerprofile. Sie macht sichtbar,
dass die Profile nicht aus dem Szenario generiert, sondern als feste
Referenzprofile bereitgestellt und für Simulationsläufe kopiert werden.

### `frontend/app.py`

Diese Datei bildet den Einstiegspunkt der Streamlit-Anwendung. Sie initialisiert
den Frontend-State, lädt Styles und rendert die jeweils aktuelle Workflowansicht.

### `frontend/state.py`

Diese Datei verwaltet zentrale Session-Werte des Frontends. Dazu gehören das
Default-Szenario, der Backend-State, ausgewählte Profile, Modellwerte und
Simulationsergebnisse.

### `frontend/shared/services/workflow_api.py`

Diese Datei kapselt die HTTP-Kommunikation mit dem Backend. Sie enthält die
Aufrufe an den Workflow-Endpunkt und die Fehlerbehandlung für Backend-Antworten.
Damit ist sie die wichtigste technische Schnittstelle zwischen Frontend und
Backend.

### `frontend/features/simulation/results.py`

Diese Datei bildet den Einstiegspunkt der Ergebnisdarstellung im Frontend. Sie
koordiniert die Anzeige von Profilvergleich, Verlaufsdiagrammen, Events,
Handlungsempfehlungen und Exportfunktionen.

## 8. Hinweise zur Erweiterbarkeit

Die vorhandene Struktur unterstützt Erweiterungen an mehreren fachlichen
Punkten, ohne dass der gesamte Analyseworkflow neu aufgebaut werden muss.

Prompt-Vorlagen sind unter `backend/prompts/` organisiert. Die produktive
Nutzung erfolgt über die Zuordnung im Prompt Loader, wodurch nachvollziehbar
bleibt, welche Promptdateien Teil des LLM-Pfads sind.

Weitere Nutzerprofile können auf Ebene der Profildefinitionen in
`backend/domains/users/profiles/` und der Registry in
`backend/domains/users/registry.py` eingeordnet werden. Dadurch bleiben
Referenzprofile zentral auffindbar und können im Simulationsplan konsistent
verwendet werden.

Die Ergänzung weiterer Metriken ist innerhalb von
`backend/domains/simulation/metrics/` vorgesehen. Die Registrierung über die
bestehende Registry-Infrastruktur ermöglicht die Berechnung über stabile IDs
und die spätere Einbindung in Ergebnisdarstellung oder Profilvergleich.

Weitere Events können entsprechend der bestehenden Struktur in
`backend/domains/simulation/events/` ergänzt und über die Event-Registry
eingebunden werden. Dadurch bleibt die Simulationsengine von einzelnen
Eventdefinitionen weitgehend getrennt.

Algorithmische Teilberechnungen sind in
`backend/domains/simulation/algorithms/` organisiert. Die Registry-Struktur
ermöglicht, Berechnungsmodelle separat zu registrieren und aus der
Simulationsengine heraus über fachliche IDs aufzurufen.

Die Ergebnisdarstellung ist in `frontend/features/simulation/` gegliedert. Die
Trennung in `components/`, `styles/` und `utils/` bildet eine Struktur für
Ansichten, CSS-Fragmente und reine Hilfsfunktionen.

## 9. Auswahl der zentralen Einstiegspunkte

Die genannten Dateien und Verzeichnisse wurden ausgewählt, weil sie die
wichtigsten Übergänge im System abbilden: Start der Anwendung, HTTP-Kommunikation,
Workflow-Orchestrierung, LLM-gestützte Modellkonstruktion, deterministische
Simulation, Ergebnisaggregation und Frontend-Darstellung.

Nicht jede Datei des Repositorys wird einzeln aufgeführt. Entscheidend sind
diejenigen Stellen, an denen die fachlichen Konzepte der Bachelorarbeit in
technische Verarbeitungsschritte überführt werden. Der Code Guide konzentriert
sich deshalb auf Dateien, die für das Verständnis des Gesamtablaufs besonders
relevant sind.
