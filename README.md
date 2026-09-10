# 🏛️ Salesforce World // Retro RPG Explorer & Architecture Atlas

> A handcrafted retro-exploration RPG world and 2.5D architectural visualizer representing the entire metadata, semantic graph, and cognitive agent fabric of an enterprise Salesforce organization.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Salesforce: Spring '26 / v66.0](https://img.shields.io/badge/Salesforce-v66.0-00a1e0.svg)](https://developer.salesforce.com)
[![Modes: Explore + Atlas](https://img.shields.io/badge/Modes-RPG%20%2B%202.5D%20Atlas-00f0ff.svg)](#-two-unified-ux-layers)

---

## 🌟 Executive Overview

Salesforce architecture is often taught as abstract, disconnected diagrams. **Salesforce World** reimagines an enterprise Salesforce org as a living, explorable retro RPG town and architectural masterplan.

Walk the streets as the **Salesforce Explorer**, discover 17 landmark institutions across 7 architectural districts, inspect real-world metadata schemas and code contracts, or switch instantly to the **2.5D Architecture Atlas** for high-altitude systems inspection.

```
+-----------------------------------------------------------------------------------------+
|                      SALESFORCE WORLD DUAL-LAYER ARCHITECTURE                           |
|                                                                                         |
|   [ 🎮 EXPLORE LAYER: Retro RPG Town ]      <--->     [ 🏛️ ATLAS LAYER: 2.5D Masterplan ]|
|   - Smooth 4-way character exploration                - Isometric axonometric projection |
|   - Handcrafted pixel/vector landmarks                - Multi-tier structural massings   |
|   - Depth-sorted Y-ordered entities                   - Dynamic architectural callouts   |
|   - Discovery journal & Field Guide (0/17)            - District filters & camera pan    |
|   - Ambient water, smoke, light halos & conduits      - Universal ⌘K search & fast travel|
+-----------------------------------------------------------------------------------------+
```

---

## 🎮 Two Unified UX Layers

### 1. 🎮 Explore Mode (Handcrafted Retro RPG World)
- **Salesforce Explorer**: Control a small adventurer character with 4-directional walk cycles, idle breathing animation, and sub-pixel smooth movement.
- **True Depth Sorting (Y-Ordering)**: The player and environmental elements (trees, streetlamps, props) naturally render in front of and behind buildings based on their ground position.
- **Landmark Discovery & Field Guide (`G`)**: Approaching landmarks for the first time triggers a celebratory discovery banner and records progress in persistent `localStorage`.
- **Living Town Ambiance**:
  - Churning water ripples and shoreline foam in the Data Cloud Harbor
  - Chimney smoke puffs at the Apex Foundry
  - Rotating 360° lighthouse searchlight beam at Calculated Insights
  - Pulsing violet energy core and revolving planetary rings at the Agentforce Spire
  - Rotating observatory telescope and copper dome at Claudeforce
  - Warm ambient light pools under street lamps
  - Dynamic data conduits carrying energy pulses between connected districts

### 2. 🏛️ Atlas Mode (2.5D Architectural Masterplan)
- **High-Altitude Overview**: Switch seamlessly between Explore and Atlas using the header toggle or the `V` key.
- **Systems Architecture**: Filter by district, view structural floor plates, inspect conduits, and fly the camera smoothly across the masterplan.
- **Technical Dossiers**: Every building features an interactive slide-over dossier with technical summaries, production metrics, and live syntax-highlighted XML, Apex, and SOQL snippets.

---

## 🏛️ The Seven Thematic Districts & 17 Landmarks

| District | Landmark | Architectural Metaphor & Function |
| :--- | :--- | :--- |
| **🏢 1. Metadata Citadel** | **Standard Objects Tower** | Grand stone archive housing core relational entities (`Account`, `Contact`, `Opportunity`, `Case`). |
| | **Custom Objects Works** | Artisan stonemason workshop with drafting tables for custom schemas (`__c`). |
| | **Security Citadel** | Fortified stone keep with battlements, iron portcullis, FLS, and Org-Wide Defaults (OWD). |
| **⚡ 2. Logic & Automation** | **Flow Hydro-Plant** | Pumping station with turning water wheel driving declarative automations. |
| | **Apex Foundry** | Heavy brick forge with blast furnace windows compiling Apex `WITH USER_MODE`. |
| | **Platform Event Bus** | Broadcast relay tower with high-frequency antenna streaming Kafka events. |
| **🌊 3. Data Cloud Harbor** | **Data Lake Reservoirs** | Deep sapphire reservoir basin with stone embankments ingesting poly-cloud DLOs. |
| | **DMO Refinery** | Maritime processing plant running Identity Resolution into the Golden Record. |
| | **Vector RAG Vault** | Obsidian pavilion with a floating polyhedral crystal storing semantic vector embeddings. |
| | **Insights Lighthouse** | Striped stone lighthouse with rotating searchlight projecting Calculated Insights. |
| **🚀 4. Headless 360 Skyport** | **Headless API Gateway** | Modern departure terminal with runway lights: *"The API is the UI. No browser required."* |
| | **HXL Concourse** | Multi-gate transit hub dispatching directly to Slack Concierge, mobile units, and AI agents. |
| **🤖 5. Agentforce Forum** | **Atlas Reasoning Spire** | Modern research rotunda with a floating, pulsing violet core running the Atlas cognitive loop. |
| | **Trust Layer Bastion** | Protective glass sanctuary with cyan energy shields enforcing PII masking & zero data retention. |
| **🧠 6. Claudeforce Labs** | **Cognitive Observatory** | Neoclassical institute with copper dome and brass telescope running Claude 3.5 200k audits. |
| **🔌 7. Dual-Plane MCP** | **Plane 1: Context Server** | Subterranean terminal switching station exposing `data360` context tools (`search`, `execute`). |
| | **Plane 2: Action Dispatcher**| Elevated railway control tower executing governed state mutations `WITH USER_MODE`. |

---

## ⌨️ Controls & Keyboard Shortcuts

| Shortcut | Action | Mode |
| :--- | :--- | :--- |
| **`W A S D` / `Arrows`** | Move Explorer | Explore |
| **`E`** | Interact with Building Entrance / Open Dossier | Explore |
| **`V`** | Toggle View Mode (Explore RPG ↔ Atlas 2.5D) | Both |
| **`G`** | Open Architectural Field Guide | Both |
| **`⌘K` / `Ctrl+K`** | Universal Command Palette & Search | Both |
| **`Space`** | Play / Pause Emergency Rescue Simulation | Both |
| **`T`** | Start / Stop Guided Architectural Tour | Atlas |
| **`1` – `7`** | Fast Travel to Districts 1 through 7 | Both |
| **`M`** | Toggle Procedural Sound FX | Both |
| **`?`** | Open Keyboard Navigation Cheatsheet | Both |
| **`Esc`** | Close Open Modal / Drawer | Both |

*Mobile & Touch: Features on-screen virtual D-Pad and Action Button `[E]`, plus tap-to-travel.*

---

## 🧪 Interactive Operational Simulation Studio

Test the **Cold-Chain Excursion Rescue Protocol** (`Space`):

1. **Stage 1: IoT Ingestion**: Sensor `DC-HYD-04` reports 9.2°C excursion on consignment `SH-88392`.
2. **Stage 2: Identity Resolution**: Data Cloud links telemetry to Dr. Meera Reddy (VIP Patient `UID-88291`).
3. **Stage 3: Kafka Event Broadcast**: `INDRA_Care_Signal__e` Platform Event published to asynchronous event bus.
4. **Stage 4: Atlas Reasoning Loop**: Einstein Trust Layer masks PII $\rightarrow$ Matches Topic `ColdChain_Rescue` $\rightarrow$ Grounds in cold-chain contingency SOP.
5. **Stage 5: Headless MCP Dispatch**: Plane 2 tool `headless360_dispatch` invoked `WITH USER_MODE`, creating P0 Case `CASE-99120`.
6. **Stage 6: Slack HXL Concierge**: Interactive Slack Block Kit notification dispatched to operations concierge with 1-click rescue authorization.

*Click **"Inspect JSON Payload 📄"** on any step to examine raw runtime JSON payloads, event headers, and JSON-RPC frames.*

---

## 🚀 Running Locally

### Option 1: Standalone Single-File Bundle (Zero Dependencies)
Open `standalone.html` in any web browser:
```bash
open standalone.html
```

### Option 2: Modular Source Code Development
```bash
git clone https://github.com/abhishekSF/salesforce-city-visualizer.git
cd salesforce-city-visualizer
git checkout feature/rpg-city
python3 -m http.server 8080
open http://localhost:8080
```

---

## 📂 Project Architecture

```
salesforce-city-visualizer/
├── index.html                      # Web application shell (Dual-Mode)
├── standalone.html                 # Complete, self-contained single-file build
├── README.md                       # Architecture & user guide
├── WORLD_DESIGN.md                 # Handcrafted RPG world & landmarks design spec
├── src/
│   ├── main.js                     # Application bootstrap & lifecycle manager
│   ├── styles/
│   │   └── pixel-city.css          # Glassmorphism, Swiss typography & mobile controls
│   ├── components/
│   │   ├── Atlas.js                # Dual-layer view coordinator & conduit overlay
│   │   ├── FieldGuide.js           # Discovery journal & localStorage persistence
│   │   ├── CommandPalette.js       # Universal ⌘K search modal & keyboard navigation
│   │   ├── GuidedTour.js           # 7-chapter narrative guided walkthrough
│   │   ├── SimulationController.js # Scrubbable timeline player & payload inspector
│   │   ├── BuildingInspector.js    # Slide-over architectural dossier & schema viewer
│   │   └── ConceptModal.js         # Deep-dive system architecture studio
│   ├── data/
│   │   ├── cityLayout.js           # 28x28 grid tile mapping (water, roads, plazas)
│   │   ├── metadataCatalog.js      # SObject schemas, DMO definitions, and conduits
│   │   └── conceptGuides.js        # Technical whitepapers (Headless 360, Atlas, MCP)
│   └── engine/
│       ├── PlayerCharacter.js      # Explorer character with 4-way walk animations
│       ├── TopDownWorld.js         # Top-down RPG world engine with Y-depth sorting
│       ├── IsometricCanvas.js      # 2.5D axonometric projection & rendering engine
│       ├── ParticleSystem.js       # Discrete data packet conduits & drone particles
│       └── SoundFx.js              # Synthesized procedural audio (Web Audio API)
└── scripts/
    └── rebuild_artifact.py         # Automated single-file bundler
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
