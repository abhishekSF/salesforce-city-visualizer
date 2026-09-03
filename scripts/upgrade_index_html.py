html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Salesforce Org 2.5D City Visualizer</title>
  <link rel="stylesheet" href="./src/styles/pixel-city.css" />
</head>
<body>

  <!-- Fullscreen 2.5D Isometric Canvas -->
  <canvas id="city-canvas"></canvas>

  <!-- Ambient Vignette Overlay -->
  <div class="vignette"></div>

  <!-- Top Glassmorphic Navigation Bar -->
  <header class="nav-header">
    <!-- Brand / Org Identification -->
    <div class="brand-group">
      <div class="brand-icon">☁️</div>
      <div>
        <div class="brand-title">
          <span>SALESFORCE ORG CITY</span>
          <span class="badge-pill" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3);">v66.0</span>
          <span class="pulse-dot" title="Live Synced"></span>
        </div>
        <div class="brand-subtitle">Metadata & Semantic Layer 2.5D Visualizer</div>
      </div>
    </div>

    <!-- Segmented District Filter -->
    <div class="district-segmented">
      <button data-filter="all" class="filter-btn segmented-btn active">All Districts</button>
      <button data-filter="metadata" class="filter-btn segmented-btn">🏢 Metadata</button>
      <button data-filter="automation" class="filter-btn segmented-btn">⚡ Automation</button>
      <button data-filter="semantic" class="filter-btn segmented-btn">🌊 Data Cloud</button>
      <button data-filter="headless" class="filter-btn segmented-btn">🚀 Headless 360</button>
      <button data-filter="agentforce" class="filter-btn segmented-btn">🤖 Agentforce</button>
      <button data-filter="claudeforce" class="filter-btn segmented-btn">🧠 Claudeforce</button>
      <button data-filter="mcp" class="filter-btn segmented-btn">🔌 Dual MCPs</button>
    </div>

    <!-- Action Tools -->
    <div style="display: flex; align-items: center; gap: 8px;">
      <button id="btn-open-academy" class="btn-primary" style="background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%); border-color: rgba(168, 85, 247, 0.4); box-shadow: 0 4px 14px rgba(124, 58, 237, 0.4);">
        <span>🎓</span>
        <span>Concept Academy</span>
      </button>

      <button id="btn-run-simulation" class="btn-primary" style="background: linear-gradient(135deg, #059669 0%, #0d9488 100%); border-color: rgba(16, 185, 129, 0.4); box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);">
        <span>⚡</span>
        <span>Run Rescue Demo</span>
      </button>

      <button id="btn-toggle-sound" class="btn-secondary">
        🔊 Sound FX
      </button>

      <button id="btn-toggle-night" class="btn-secondary">
        🌙 Cyber Night
      </button>

      <button id="btn-center-camera" class="btn-secondary" title="Center View (C)">
        🎯 Center
      </button>
    </div>
  </header>

  <!-- Live Simulation Toast Banner -->
  <div id="sim-banner" class="hidden">
    <div style="display: flex; align-items: flex-start; gap: 14px;">
      <div style="font-size: 24px;">🚨</div>
      <div style="flex: 1;">
        <div id="sim-banner-title" style="font-size: 13px; font-weight: 700; color: #34d399; text-transform: uppercase; letter-spacing: 0.04em;">Simulation In Progress</div>
        <div id="sim-banner-detail" style="font-size: 12px; color: #f1f5f9; margin-top: 4px; line-height: 1.5;">Broadcasting operational state change through org layers...</div>
      </div>
    </div>
  </div>

  <!-- Building Inspector Slide-over Drawer -->
  <aside id="building-inspector" class="hidden"></aside>

  <!-- Bottom Quick-Jump Dock -->
  <footer class="bottom-dock">
    <div style="display: flex; align-items: center; gap: 6px; overflow-x: auto;">
      <span style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 600; margin-right: 6px;">Quick Jump:</span>
      <button data-target="b_standard_objects" class="district-jump-btn segmented-btn" style="color: #38bdf8;">1. Metadata</button>
      <button data-target="b_apex_foundry" class="district-jump-btn segmented-btn" style="color: #f59e0b;">2. Automation</button>
      <button data-target="b_data_lake" class="district-jump-btn segmented-btn" style="color: #06b6d4;">3. Data Cloud</button>
      <button data-target="b_headless_gateway" class="district-jump-btn segmented-btn" style="color: #10b981;">4. Headless 360</button>
      <button data-target="b_agentforce_core" class="district-jump-btn segmented-btn" style="color: #a855f7;">5. Agentforce</button>
      <button data-target="b_claudeforce_lab" class="district-jump-btn segmented-btn" style="color: #f97316;">6. Claudeforce</button>
      <button data-target="b_mcp_context" class="district-jump-btn segmented-btn" style="color: #ec4899;">7. Dual MCPs</button>
    </div>
    <div style="display: flex; align-items: center; gap: 12px; font-size: 11px; color: #64748b;">
      <span>Drag: Pan</span> • <span>Scroll: Zoom</span> • <span>Click: Inspect Building</span>
    </div>
  </footer>

  <!-- Concept Academy Modal -->
  <div id="concept-modal" class="hidden"></div>

  <!-- Application Bootstrap -->
  <script type="module" src="./src/main.js"></script>
</body>
</html>
'''

with open('/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer/index.html', 'w') as f:
    f.write(html_content)

print("Upgraded index.html successfully!")
