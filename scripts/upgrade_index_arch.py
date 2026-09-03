html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Salesforce Org Axonometric Masterplan // Architectural Visualizer</title>
  <link rel="stylesheet" href="./src/styles/pixel-city.css" />
</head>
<body>

  <!-- Fullscreen Axonometric Drafting Canvas -->
  <canvas id="city-canvas"></canvas>

  <!-- Architectural Drafting Grid Overlay -->
  <div class="drafting-grid"></div>

  <!-- Vellum Edge Vignette -->
  <div class="vellum-vignette"></div>

  <!-- Top Architectural Navigation Bar -->
  <header class="arch-header">
    <!-- Brand & Masterplan Identification -->
    <div class="arch-brand">
      <div class="arch-logo">SF</div>
      <div>
        <div class="arch-title">
          <span>SALESFORCE ORG MASTERPLAN</span>
          <span class="datum-tag" style="border-color: rgba(0, 240, 255, 0.4); color: #00f0ff;">AXONOMETRIC v66.0</span>
        </div>
        <div class="arch-subtitle">METADATA, SEMANTIC GRAPH & COGNITIVE FABRIC</div>
      </div>
    </div>

    <!-- Architectural Zoning / District Filter -->
    <div class="program-selector">
      <button data-filter="all" class="filter-btn program-btn active">Masterplan (All)</button>
      <button data-filter="metadata" class="filter-btn program-btn">1. Metadata</button>
      <button data-filter="automation" class="filter-btn program-btn">2. Logic Grid</button>
      <button data-filter="semantic" class="filter-btn program-btn">3. Semantic Lake</button>
      <button data-filter="headless" class="filter-btn program-btn">4. Headless 360</button>
      <button data-filter="agentforce" class="filter-btn program-btn">5. Agentforce</button>
      <button data-filter="claudeforce" class="filter-btn program-btn">6. Claudeforce</button>
      <button data-filter="mcp" class="filter-btn program-btn">7. Dual MCPs</button>
    </div>

    <!-- Architectural Controls & Studio -->
    <div style="display: flex; align-items: center; gap: 8px;">
      <button id="btn-open-academy" class="action-btn-primary" style="background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%); border-color: rgba(99, 102, 241, 0.4);">
        <span>🏛️</span>
        <span>Concept Studio</span>
      </button>

      <button id="btn-run-simulation" class="action-btn-primary" style="background: linear-gradient(135deg, #059669 0%, #065f46 100%); border-color: rgba(16, 185, 129, 0.4);">
        <span>⚡</span>
        <span>Run Rescue Protocol</span>
      </button>

      <button id="btn-toggle-callouts" class="action-btn-ghost" title="Toggle Architectural Callouts">
        📐 Callouts
      </button>

      <button id="btn-toggle-sound" class="action-btn-ghost">
        🔊 Sound FX
      </button>

      <button id="btn-center-camera" class="action-btn-ghost" title="Center View (C)">
        🎯 Center
      </button>
    </div>
  </header>

  <!-- Live Operation Protocol Banner -->
  <div id="sim-banner" class="hidden">
    <div style="display: flex; align-items: flex-start; gap: 14px;">
      <div style="font-size: 22px;">🚨</div>
      <div style="flex: 1;">
        <div id="sim-banner-title" style="font-size: 13px; font-weight: 700; color: #10b981; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; letter-spacing: 0.04em;">SIMULATION IN PROGRESS</div>
        <div id="sim-banner-detail" style="font-size: 12px; color: #f1f5f9; margin-top: 4px; line-height: 1.5;">Broadcasting operational state change through org layers...</div>
      </div>
    </div>
  </div>

  <!-- Slide-Over Architectural Dossier -->
  <aside id="building-inspector" class="hidden"></aside>

  <!-- Bottom Architectural Dock & Scale -->
  <footer class="arch-dock">
    <div style="display: flex; align-items: center; gap: 6px; overflow-x: auto;">
      <span style="font-size: 10px; color: #64748b; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; margin-right: 6px;">ZONE SELECT:</span>
      <button data-target="b_standard_objects" class="district-jump-btn program-btn" style="color: #38bdf8;">1. Metadata Citadel</button>
      <button data-target="b_apex_foundry" class="district-jump-btn program-btn" style="color: #f59e0b;">2. Logic Grid</button>
      <button data-target="b_data_lake" class="district-jump-btn program-btn" style="color: #06b6d4;">3. Semantic Lake</button>
      <button data-target="b_headless_gateway" class="district-jump-btn program-btn" style="color: #10b981;">4. Headless 360</button>
      <button data-target="b_agentforce_core" class="district-jump-btn program-btn" style="color: #a855f7;">5. Agentforce Spire</button>
      <button data-target="b_claudeforce_lab" class="district-jump-btn program-btn" style="color: #f97316;">6. Claudeforce Lab</button>
      <button data-target="b_mcp_context" class="district-jump-btn program-btn" style="color: #ec4899;">7. Dual MCPs</button>
    </div>
    <div style="display: flex; align-items: center; gap: 14px; font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace;">
      <span>DRAG: PAN</span> • <span>SCROLL: ZOOM</span> • <span>CLICK: INSPECT NODE</span>
    </div>
  </footer>

  <!-- Architectural Concept Studio Modal -->
  <div id="concept-modal" class="hidden"></div>

  <!-- Application Bootstrap -->
  <script type="module" src="./src/main.js"></script>
</body>
</html>
'''

with open('/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer/index.html', 'w') as f:
    f.write(html_content)

print("Architectural index.html written successfully!")
