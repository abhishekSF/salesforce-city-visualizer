# 🏛️ Salesforce Org Axonometric Masterplan // 2.5D City Visualizer

> An interactive 2.5D architectural axonometric visualizer representing the entire metadata, semantic graph, and cognitive agent fabric of an enterprise Salesforce organization.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Salesforce: Spring '26 / v66.0](https://img.shields.io/badge/Salesforce-v66.0-00a1e0.svg)](https://developer.salesforce.com)
[![Architecture: Swiss Axonometric](https://img.shields.io/badge/Style-Axonometric%20Drafting-00f0ff.svg)](#-architectural-design-philosophy)

---

## 🌟 Executive Overview & Architectural Concept

Traditional enterprise architecture diagrams represent Salesforce as dry, disconnected box-and-line charts. **Salesforce Org Masterplan** reimagines the entire metadata catalog, transactional engine, data lake, and AI reasoning loop as a living architectural metropolis.

Designed with architectural drafting discipline, Swiss International Style typography, and deep systems engineering principles, this tool bridges the mental gap between **relational storage**, **declarative metadata**, **semantic context graphs**, and **autonomous agentic execution**.

```
+-----------------------------------------------------------------------------------------+
|                    SALESFORCE ORG AXONOMETRIC MASTERPLAN (2.5D)                         |
|                                                                                         |
|   [ 🏢 ZONE 1: METADATA CITADEL ]       <--->       [ ⚡ ZONE 2: LOGIC & AUTOMATION ]   |
|      Standard/Custom SObjects (Account,                 Apex (WITH USER_MODE), Flows,   |
|      Depot__c), FLS, OWD, Sharing Rules                 High-Throughput Kafka Events    |
|                     ^                                                ^                  |
|                     |                                                |                  |
|                     v                                                v                  |
|   [ 🚀 ZONE 4: HEADLESS 360 SKYPORT ]   <--->       [ 🤖 ZONE 5: AGENTFORCE SPIRE ]    |
|      "The API is the UI. No browser"                    Atlas Reasoning Engine Loop,    |
|      GraphQL, Composite Graph, Slack HXL                Trust Layer, Invocable Actions  |
|                     ^                                                ^                  |
|                     |                                                |                  |
|                     v                                                v                  |
|   [ 🔌 ZONE 7: DUAL-PLANE MCP INTERCHANGE ] <->     [ 🧠 ZONE 6: CLAUDEFORCE LABS ]     |
|      Plane 1 (Context data360) vs                       Anthropic Claude 3.5 Sonnet,    |
|      Plane 2 (Action headless-360)                      200k Context, Vision BOL Parser |
|                     ^                                                                   |
|                     |                                                                   |
|                     v                                                                   |
|   [ 🌊 ZONE 3: DATA CLOUD & SEMANTIC HARBOR ]                                           |
|      DLO Lake Ingestion, CIM Harmonization, Golden Identity Graph, Calculated Insights  |
+-----------------------------------------------------------------------------------------+
```

---

## 🏛️ The Seven Thematic Urban Districts

### 1. 🏢 Metadata Citadel (Relational Schema & Security Perimeter)
- **Standard Objects Tower**: `Account`, `Contact`, `Opportunity`, `Case`, `Lead`.
- **Custom Objects Works (`__c`)**: Custom facility and cold-chain schema (`INDRA_Shipment__c`, `Logistics_Depot__c`).
- **Security Citadel**: Profiles, Permission Sets, Field-Level Security (FLS), Organization-Wide Defaults (OWD).

### 2. ⚡ Logic & Automation Grid (Transactional Execution Engine)
- **Flow Hydro-Automation Plant**: Autolaunched, Record-Triggered, and Orchestrator Flows.
- **Apex Foundry**: Strongly-typed business logic compiled `WITH USER_MODE` for compile-time permission verification.
- **Platform Event Bus**: High-throughput Kafka event streaming backbone broadcasting delta events (`INDRA_Care_Signal__e`).

### 3. 🌊 Data Cloud & Semantic Harbor (Context Lake & Ontologies)
- **Data Lake Reservoirs (DLOs)**: Poly-cloud lakehouse ingestion (S3, Iceberg, Snowflake Zero-Copy).
- **Identity Resolution Refinery**: Deterministic and probabilistic rule engines resolving disparate touchpoints into a unified **Golden Record** (`UnifiedIndividual__dlm`).
- **Vector Knowledge Vault**: High-dimensional semantic embeddings of cold-chain SOPs and regulatory contingency plans.
- **Calculated Insights Lighthouse**: Continuous streaming SQL aggregations (Care Risk Score, Depot Stress Index).

### 4. 🚀 Headless 360 Skyport (Composable Architecture & HXL)
- **Headless API Gateway**: *"The API is the UI. No browser required."* Single-roundtrip GraphQL, Composite Graph API, SCAPI.
- **Headless Experience Layer (HXL)**: Direct delivery into Slack, mobile handhelds, Next.js micro-frontends, and automated AI runtimes.

### 5. 🤖 Agentforce Autonomous Spire (Cognitive Reasoning Loop)
- **Atlas Reasoning Engine**: Closed-loop perception, intent evaluation, topic classification, semantic grounding, and action planning.
- **Einstein Trust Layer Bastion**: Zero data retention, automated PII de-identification (reversible tokenization), and toxic content gating.

### 6. 🧠 Claudeforce Research Complex (Frontier Multimodal AI)
- **Claude 3.5 Sonnet Cognitive Observatory**: 200,000 token context window for whole-org architectural audits and automated governor-limit-compliant Apex synthesis.
- **Multimodal Vision Ingestion**: Directly converts physical paper manifests, bills of lading (BOL), and clinical temperature recorder strips into structured SObject records.

### 7. 🔌 Dual-Plane Hosted MCP Interchange (Model Context Protocol)
- **Plane 1: Data 360 MCP Server (`data360`) — System of Context**: Read-only isolation (`search`, `payload_examples`, `execute`).
- **Plane 2: Headless 360 MCP Server (`headless-360`) — System of Action**: Standardized tool interface (`discover`, `describe`, `dispatch`, `dispatch_readonly`) executing strictly in authenticated user context with native FLS/CRUD enforcement.

---

## 🧭 Interaction Design & Power-User Features

| Shortcut | Feature | Description |
| :--- | :--- | :--- |
| **`⌘K` / `Ctrl+K`** | **Universal Search** | Instant command palette searching across SObjects, DMOs, Flows, Apex, and architectural concepts. |
| **`T`** | **Guided Tour** | 7-chapter narrative walkthrough gliding the camera through each district with architectural commentary. |
| **`Space`** | **Interactive Scenario** | Starts and toggles play/pause on the scrubbable cold-chain rescue simulation. |
| **`1` – `7`** | **Quick Zone Jump** | Teleports camera focus directly to any of the 7 thematic districts. |
| **`C`** | **Center Camera** | Recenters the masterplan in the viewport. |
| **`M`** | **Audio Mute** | Toggles procedural 8-bit audio synthesized via Web Audio API. |
| **`?`** | **Shortcuts Cheatsheet** | Displays keyboard navigation overlay. |
| **`Esc`** | **Dismiss Overlay** | Closes any active drawer, modal, or palette. |

---

## 🧪 Interactive Operational Simulation Studio

The visualizer includes an end-to-end **Cold-Chain Excursion Rescue Protocol** that you can step through and scrub interactively:

1. **Stage 1: IoT Telemetry Ingestion**: Sensor `DC-HYD-04` reports 9.2°C temperature excursion (+1.2°C above threshold).
2. **Stage 2: Semantic Identity Resolution**: Data Cloud unifies telemetry DLO to Dr. Meera Reddy (VIP Patient Household `UID-88291`).
3. **Stage 3: Kafka Event Bus Broadcast**: Asynchronous `INDRA_Care_Signal__e` Platform Event published to Kafka bus.
4. **Stage 4: Agentforce Atlas Reasoning**: Einstein Trust Layer masks PII $\rightarrow$ Matches Topic `ColdChain_Rescue` $\rightarrow$ Grounds in cold-chain contingency SOP vector.
5. **Stage 5: Headless 360 MCP Dispatch**: Plane 2 tool `headless360_dispatch` invoked `WITH USER_MODE`, creating P0 Case `CASE-99120`.
6. **Stage 6: Slack HXL Concierge**: Interactive Slack Block Kit notification dispatched to operations concierge with 1-click rescue authorization.

*Click **"Inspect JSON Payload 📄"** on any step to examine raw runtime JSON payloads, event headers, and JSON-RPC frames.*

---

## 🚀 Running Locally

### Option 1: Standalone Single-File Bundle (Zero Dependencies)
Simply double-click or open `standalone.html` in any modern web browser:
```bash
open standalone.html
```

### Option 2: Local HTTP Server (Modular Source Code)
To explore or develop the modular ES6 architecture (`src/`):
```bash
# Clone the repository
git clone https://github.com/abhishekSF/salesforce-city-visualizer.git
cd salesforce-city-visualizer

# Run a lightweight local server
python3 -m http.server 8080

# Open in your browser
open http://localhost:8080
```

---

## 📂 Project Architecture

```
salesforce-city-visualizer/
├── index.html                      # Modular web application shell
├── standalone.html                 # Self-contained, single-file distribution build
├── README.md                       # Architectural design documentation
├── src/
│   ├── main.js                     # Application lifecycle & event controller
│   ├── styles/
│   │   └── pixel-city.css          # Swiss architectural styling & glassmorphism
│   ├── components/
│   │   ├── CommandPalette.js       # Global ⌘K search modal & keyboard navigation
│   │   ├── GuidedTour.js           # 7-chapter narrative guided walkthrough
│   │   ├── SimulationController.js # Scrubbable timeline player & payload inspector
│   │   ├── BuildingInspector.js    # Slide-over architectural dossier & schema viewer
│   │   └── ConceptModal.js         # Deep-dive system architecture studio
│   ├── data/
│   │   ├── cityLayout.js           # Isometric grid coordinate mapping
│   │   ├── metadataCatalog.js      # SObject schemas, DMO definitions, and conduits
│   │   └── conceptGuides.js        # Technical whitepapers (Headless 360, Atlas, MCP)
│   └── engine/
│       ├── IsometricCanvas.js      # 2.5D axonometric projection & rendering engine
│       ├── ParticleSystem.js       # Discrete data packet conduits & drone particles
│       └── SoundFx.js              # Synthesized procedural audio (Web Audio API)
└── scripts/
    └── rebuild_artifact.py         # Automated bundler synthesizing modular code into standalone.html
```

---

## 🛠️ Technical Implementation Highlights

- **Pure Web Standards**: Built exclusively with Vanilla ES6 modules, HTML5 Canvas 2D, CSS3, and the Web Audio API. Zero bloated frameworks, zero npm dependencies.
- **Axonometric 2:1 Projection**: Geometric isometric transformation ($x' = (x - y) \cdot \frac{W}{2}$, $y' = (y + x) \cdot \frac{H}{2}$) with depth-sorted painter's algorithm rendering.
- **Synthesized Audio Engine**: All interaction sounds (clicks, select chirps, conduit pulses) are synthesized procedurally in real-time using Web Audio oscillators.
- **Enterprise Security Grounding**: Implements realistic Salesforce Spring '26 / v66.0 architecture patterns including `WITH USER_MODE`, Dual-Plane Hosted MCP isolation, and Einstein Trust Layer de-identification protocols.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

Developed with architectural discipline for the global Salesforce engineering and architecture community.
