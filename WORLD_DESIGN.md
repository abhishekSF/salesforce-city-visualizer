# 🗺️ Salesforce RPG World Design Specification

> A handcrafted retro-exploration RPG world for understanding Salesforce architecture.

---

## 🧭 World Map Layout & Zoning (28x28 Tiles @ 40px = 1120x1120px)

The world is organized into seven distinct architectural districts connected by paved avenues, cobblestone pedestrian paths, and animated data conduits.

```
       [0-8]                   [9-16]                  [17-27]
    +-----------------------+-----------------------+-------------------------+
0-8 | 🏢 ZONE 1:            | ⚡ ZONE 2:            | 🌊 ZONE 3:              |
    | METADATA CITADEL      | LOGIC & AUTOMATION    | DATA CLOUD HARBOR       |
    | - Standard Objects    | - Flow Powerhouse     | - Data Lake Reservoirs  |
    | - Custom Objects Works| - Apex Foundry        | - DMO Refinery          |
    | - Security Citadel    | - Platform Events     | - Vector RAG Vault      |
    |                       |                       | - Insights Lighthouse   |
    +-----------------------+-----------------------+-------------------------+
9-16| 🚀 ZONE 4:            | 🤖 ZONE 5:            | 🧠 ZONE 6:              |
    | HEADLESS 360 SKYPORT  | AGENTFORCE FORUM      | CLAUDEFORCE LABS        |
    | - API Gateway         | - Atlas Reasoning     | - Cognitive Observatory |
    | - HXL Terminals       | - Trust Layer Bastion | - Document Vision Lab   |
    +-----------------------+-----------------------+-------------------------+
17-27                       | 🔌 ZONE 7:                                      |
                            | DUAL-PLANE MCP INTERCHANGE                      |
                            | - Plane 1: Data 360 Context Server              |
                            | - Plane 2: Headless 360 Action Dispatcher       |
                            +-------------------------------------------------+
```

---

## 🏛️ Architectural Landmark Silhouettes

1. **Metadata Citadel (NW)**:
   - *Standard Objects Tower*: High-rise stone civic archive with arched stained-glass windows, slate mansard roof, and brass double doors.
   - *Custom Objects Works*: Stone mason workshop with blueprint displays, timber eaves, and smoking stone chimney.
   - *Security Citadel*: Crenellated stone fortress with iron portcullis, heraldic security banners, and perimeter watchlamps.

2. **Logic & Automation Grid (N)**:
   - *Flow Hydro-Automation Plant*: Industrial pumping station with turning water wheel, brass steam valves, and conduit pipes.
   - *Apex Foundry*: Heavy brick forge with glowing molten furnace vents, steel gantry crane, and iron smoke stack.
   - *Platform Event Bus*: Telecommunications broadcast tower with blinking ruby strobe and radial radio wave rings.

3. **Data Cloud & Semantic Harbor (NE)**:
   - *Data Lake Reservoirs*: Deep sapphire water basin with stone seawall embankment and intake weir floodgates.
   - *Identity Resolution Refinery*: Coastal processing facility with glass fractionation columns and harbor crane.
   - *Calculated Insights Lighthouse*: Octagonal striped lighthouse on rocky bluff casting a rotating 360° beacon beam.
   - *Vector RAG Vault*: Hexagonal obsidian pavilion housing a floating, rotating polyhedral vector crystal.

4. **Headless 360 Skyport (SW)**:
   - *Headless API Gateway*: Modern cantilevered aerospace departure concourse with illuminated runway approach lights.
   - *Headless Experience Layer (HXL)*: Dispatch terminals with dedicated bays for Slack Concierge, mobile units, and coworker drones.

5. **Agentforce Autonomous Forum (Center)**:
   - *Atlas Reasoning Engine Spire*: Soaring crystalline rotunda with revolving gyroscopic gimbal rings and pulsing violet Atlas core.
   - *Einstein Trust Layer Bastion*: Octagonal glass sanctuary with glowing cyan security shielding and biometric archway.

6. **Claudeforce Research Complex (E-Center)**:
   - *Claude 3.5 Cognitive Observatory*: Neoclassical scholarly institute with patinated copper dome, brass astrolabe, and library courtyards.

7. **Dual-Plane MCP Interchange (SE)**:
   - *Plane 1 Data 360 Context Station*: Subterranean data switching facility with glowing blue server arrays.
   - *Plane 2 Headless 360 Action Station*: Elevated railway switching tower with safety interlocks and magenta signal lamps.

---

## 🎮 Exploration Mechanics

- **Player Character**: "Salesforce Explorer" with 4-directional walking animations, directional orientation, and soft ground shadow.
- **Depth Sorting**: Every entity (player, trees, buildings, streetlamps) is Y-sorted each frame for natural visual overlap.
- **Discovery**: 17 landmarks to discover with real-time Field Guide progress tracking in `localStorage`.
- **Two UX Modes**:
  - **Explore**: Walkable retro RPG town with real-time ambiance and landmark interaction.
  - **Atlas**: High-level 2.5D architectural masterplan with search, filters, and relationship diagrams.
