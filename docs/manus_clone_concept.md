# Technisches Konzept und Architekturplan für den Manus AI Klon (Projektname: OpenManus)

## 1. Zielsetzung und Funktionsumfang

Das Ziel dieses Projekts ist die Entwicklung eines Open-Source-KI-Agenten-Systems ("OpenManus") für Debian/Ubuntu, das die Kernfunktionalitäten von Manus AI nachbildet. Der Funktionsumfang umfasst:

1. **Autonome Aufgabenverwaltung**: Interpretation komplexer Anweisungen, Zerlegung in Unterschritte und Orchestrierung der Ausführung.
2. **Sandbox-Umgebung**: Sichere Ausführung von Code (Python, Node.js) und Shell-Befehlen mit Dateisystemzugriff.
3. **Integrierter Browser**: Steuerung eines Webbrowsers für Recherche, Interaktion und Transaktionen (ähnlich dem "Comet Browser").
4. **Mediengenerierung**: Kostenlose, RAM-basierte Bilderzeugung.
5. **Multi-modale Fähigkeiten**: Verarbeitung und Erstellung von Text, Code, Daten und Bildern.

## 2. Architekturbersicht

Die Architektur von OpenManus wird in drei Hauptschichten unterteilt: den Agenten-Kern, die Tool- und Capability-Schicht und die Benutzeroberfläche (UI).

| Schicht | Beschreibung | Vorgeschlagene Open-Source-Technologien |
|---|---|---|
| **Agenten-Kern** | Die zentrale Logik für Aufgabenplanung, Tool-Auswahl und LLM-Interaktion. | **Agent Framework**: AutoGen, CrewAI, oder LangChain. **LLM**: Lokale Modelle (z.B. Llama 3, Mistral) über Ollama oder ggf. kostenlose API-Endpunkte. |
| **Tool- und Capability-Schicht** | Die Module, die die eigentlichen Aktionen ausführen. | **Sandbox**: Docker oder Firejail für Prozessisolierung. **Dateisystem**: Standard Linux-Dateisystem. **Shell**: Standard bash oder zsh. **Code-Ausführung**: Python mit pipenv oder conda, Node.js. |
| **Benutzeroberfläche (UI)** | Die Desktop-Anwendung für Debian/Ubuntu, die die Interaktion mit dem Agenten ermöglicht und die Sandbox-Ausgabe anzeigt. | **Desktop Framework**: Electron oder Qt. **Integrierter Browser**: Playwright oder Selenium zur Steuerung eines Headless/Headful Chromium-Prozesses. |

## 3. Detaillierte Komponentenbeschreibung

### 3.1. Agenten-Kern und LLM-Strategie

Um die Anforderung der Kostenersparnis zu erfüllen, muss der Agenten-Kern auf lokal laufenden Large Language Models (LLMs) basieren.

- **Inferenz-Engine**: Ollama oder llama.cpp bieten eine einfache Möglichkeit, verschiedene Modelle im GGUF-Format (quantisierte Modelle, die effizienter auf CPU/RAM laufen) zu hosten.
- **Modell-Auswahl**: Modelle wie Mistral 7B oder Llama 3 8B bieten eine gute Balance zwischen Leistung und RAM-Anforderungen (typischerweise 8-16 GB RAM).
- **Orchestrierung**: Ein Framework wie AutoGen ermöglicht die Definition von Multi-Agenten-Workflows, was die komplexe Aufgabenverwaltung von Manus AI nachbilden kann (z.B. ein Planungs-Agent, ein Code-Agent, ein Browser-Agent).

### 3.2. Sandbox- und Tool-Management

Die Sicherheit und Reproduzierbarkeit der Umgebung ist entscheidend.

- **Isolierung**: Docker bietet die robusteste Isolierung, erfordert jedoch eine Docker-Installation auf dem Host. Firejail ist eine leichtgewichtigere Alternative, die Prozesse in einer Sandbox einschränkt.
- **Dateisystem**: Der Agent muss in der Lage sein, Dateien im Sandbox-Dateisystem zu erstellen, zu lesen und zu bearbeiten. Dies wird über Standard-Shell-Befehle (cp, mv, rm) und Dateizugriffe innerhalb des isolierten Containers/Prozesses realisiert.

### 3.3. Integrierter Browser ("Comet Browser"-Klon)

Die Browser-Funktionalität muss sowohl eine visuelle Oberfläche für den Benutzer als auch eine programmatische Schnittstelle für den Agenten bieten.

- **Steuerung**: Playwright oder Selenium sind die Industriestandards für die Browser-Automatisierung. Playwright bietet eine moderne API und unterstützt Headless- sowie Headful-Modi.
- **Integration**: Die UI (z.B. in Electron) würde einen Chromium-Browser-View einbetten. Der Agenten-Kern würde über Playwright-Befehle mit diesem eingebetteten Browser interagieren, um Navigation, Klicks, Formulareingaben und das Extrahieren von Informationen durchzuführen.

### 3.4. Kostenlose, RAM-basierte Bilderzeugung

Dies ist die größte technische Herausforderung. Die Anforderung, kostenlos und RAM-basiert zu sein, schließt die Nutzung von Cloud-APIs und dedizierter GPU-Hardware aus.

- **Modell**: Stable Diffusion (SD) ist das Open-Source-Modell der Wahl.
- **Inferenz-Engine**: Die Nutzung von Stable Diffusion in C++ (SD.cpp) oder ComfyUI mit optimierten Backends (z.B. DirectML oder ONNX Runtime) für CPU-Inferenz ist notwendig.
- **RAM-Strategie**: Es muss auf quantisierte Modelle (z.B. 4-Bit oder 8-Bit Quantisierung) zurückgegriffen werden, um die VRAM-Anforderungen auf System-RAM zu verlagern.
- **Nachteil**: Die Generierungsgeschwindigkeit wird extrem langsam sein (potenziell Minuten pro Bild), und es wird eine erhebliche Menge an System-RAM benötigt (mindestens 32 GB, besser 64 GB für eine akzeptable Leistung).
- **Implementierung**: Ein dediziertes Python-Modul, das die CPU-optimierte Inferenz-Engine aufruft, wird in die Tool-Schicht integriert.

## 4. Nächste Schritte

Die nächsten Phasen des Projekts werden sich auf die Validierung und Detaillierung der vorgeschlagenen Technologien konzentrieren, insbesondere auf die Machbarkeit der RAM-basierten Bilderzeugung.

1. **Auswahl und Dokumentation der Open-Source-Technologien**: Detaillierte Begründung der finalen Technologieauswahl.
2. **Machbarkeitsstudie zur RAM-basierten Bilderzeugung**: Praktische Recherche zu Benchmarks und minimalen Hardwareanforderungen für SD.cpp/GGUF auf CPU.
3. **Implementierungsplan**: Erstellung eines detaillierten Plans für die schrittweise Entwicklung.
