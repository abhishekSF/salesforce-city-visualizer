import os
import re

base_dir = '/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer'
artifact_path = '/Users/asmgkr/.gemini/antigravity/brain/70c5c001-c5d6-45ac-acd0-3a33f17eabe3/salesforce_pixel_city.html'

def read_file(rel_path):
    with open(os.path.join(base_dir, rel_path), 'r') as f:
        return f.read()

# Read CSS
css_content = read_file('src/styles/pixel-city.css')

# Read JS modules and strip imports/exports
def clean_js(content):
    # Remove import lines
    content = re.sub(r'import\s+.*?from\s+[\'"].*?[\'"];?', '', content)
    # Replace export const / export function / export class with plain declaration
    content = re.sub(r'export\s+(const|let|var|function|class)\s+', r'\1 ', content)
    content = re.sub(r'export\s*\{[^}]*\};?', '', content)
    return content

js_metadata = clean_js(read_file('src/data/metadataCatalog.js'))
js_layout = clean_js(read_file('src/data/cityLayout.js'))
js_guides = clean_js(read_file('src/data/conceptGuides.js'))
js_sound = clean_js(read_file('src/engine/SoundFx.js'))
js_particles = clean_js(read_file('src/engine/ParticleSystem.js'))
js_canvas = clean_js(read_file('src/engine/IsometricCanvas.js'))
js_inspector = clean_js(read_file('src/components/BuildingInspector.js'))
js_modal = clean_js(read_file('src/components/ConceptModal.js'))
js_main = clean_js(read_file('src/main.js'))

# Combine JS into single script
combined_js = f"""
(function() {{
  {js_sound}
  {js_layout}
  {js_metadata}
  {js_guides}
  {js_particles}
  {js_canvas}
  {js_inspector}
  {js_modal}
  {js_main}
}})();
"""

standalone_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Salesforce Org 2.5D Pixel City Visualizer</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    {css_content}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 overflow-hidden select-none font-mono">

  <!-- Fullscreen 2.5D Isometric Canvas -->
  <canvas id="city-canvas" class="absolute inset-0 w-full h-full block z-0 cursor-default"></canvas>

  <!-- CRT Scanlines Overlay -->
  <div class="scanlines absolute inset-0 z-10 pointer-events-none opacity-40"></div>

  <!-- Top Navigation & Control Bar -->
  <header class="absolute top-3 left-3 right-3 z-20 flex flex-wrap items-center justify-between gap-3 p-2.5 bg-slate-900/90 backdrop-blur-md border-2 border-slate-700 rounded-lg shadow-xl">
    <!-- Brand / Org Identification -->
    <div class="flex items-center gap-3">
      <div class="w-8 h-8 rounded bg-sky-500/20 border border-sky-400 flex items-center justify-center text-lg shadow-[0_0_10px_rgba(56,189,248,0.5)]">
        ☁️
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-xs font-bold text-white tracking-wider">SALESFORCE ORG PIXEL CITY</h1>
          <span class="text-[9px] bg-sky-950 text-sky-400 px-1.5 py-0.5 rounded border border-sky-800">API v66.0</span>
          <span class="text-[9px] bg-emerald-950 text-emerald-400 px-1.5 py-0.5 rounded border border-emerald-800">PROD-SYNC</span>
        </div>
        <p class="text-[10px] text-slate-400">2.5D Metadata & Semantic Architecture Explorer</p>
      </div>
    </div>

    <!-- Semantic Layer Filter Pills -->
    <div class="hidden xl:flex items-center gap-1 bg-slate-950/70 p-1 rounded border border-slate-800 text-[11px]">
      <button data-filter="all" class="filter-btn px-2.5 py-1 rounded bg-sky-600 text-white font-bold border border-sky-400">All Layers</button>
      <button data-filter="metadata" class="filter-btn px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white border border-slate-700">🏢 Metadata</button>
      <button data-filter="automation" class="filter-btn px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white border border-slate-700">⚡ Automation</button>
      <button data-filter="semantic" class="filter-btn px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white border border-slate-700">🌊 Data Cloud</button>
      <button data-filter="headless" class="filter-btn px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white border border-slate-700">🚀 Headless 360</button>
      <button data-filter="agentforce" class="filter-btn px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white border border-slate-700">🤖 Agentforce</button>
      <button data-filter="claudeforce" class="filter-btn px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white border border-slate-700">🧠 Claudeforce</button>
      <button data-filter="mcp" class="filter-btn px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white border border-slate-700">🔌 Dual MCPs</button>
    </div>

    <!-- Action Tools -->
    <div class="flex items-center gap-2 text-xs">
      <button id="btn-open-academy" class="px-3 py-1.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold rounded shadow border border-purple-400 flex items-center gap-1.5">
        <span>🎓</span>
        <span>Concept Academy</span>
      </button>

      <button id="btn-run-simulation" class="px-3 py-1.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold rounded shadow border border-emerald-400 flex items-center gap-1.5">
        <span>🎬</span>
        <span>Run Rescue Demo</span>
      </button>

      <button id="btn-toggle-sound" class="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700">
        🔊 Sound FX
      </button>

      <button id="btn-toggle-night" class="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700">
        🌙 Cyber Night
      </button>

      <button id="btn-center-camera" class="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700" title="Center Camera (C)">
        🎯 Center
      </button>
    </div>
  </header>

  <!-- Live Simulation Toast Banner (floating top center) -->
  <div id="sim-banner" class="hidden absolute top-20 left-1/2 -translate-x-1/2 z-30 w-full max-w-xl p-3 bg-slate-900/95 border-2 border-emerald-500 rounded-lg shadow-2xl backdrop-blur-md">
    <div class="flex items-start gap-3">
      <div class="text-2xl animate-bounce">🚨</div>
      <div class="flex-1">
        <h3 id="sim-banner-title" class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Simulation Active</h3>
        <p id="sim-banner-detail" class="text-xs text-slate-200 mt-1 leading-relaxed">Processing operational event through Salesforce Org layers...</p>
      </div>
    </div>
  </div>

  <!-- Building Inspector Slide-out Drawer (Right side) -->
  <aside id="building-inspector" class="hidden absolute top-20 right-3 bottom-14 z-30 w-96 max-w-full rounded-lg shadow-2xl overflow-hidden border-2 border-slate-700"></aside>

  <!-- Bottom Quick-Jump District Toolbar -->
  <footer class="absolute bottom-3 left-3 right-3 z-20 flex items-center justify-between p-2 bg-slate-900/85 backdrop-blur-md border border-slate-800 rounded-lg text-xs">
    <div class="flex items-center gap-1.5 overflow-x-auto py-0.5">
      <span class="text-[10px] text-slate-500 uppercase mr-1">Jump to District:</span>
      <button data-target="b_standard_objects" class="district-jump-btn px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-400 border border-slate-700 font-bold">1. Metadata Citadel</button>
      <button data-target="b_apex_foundry" class="district-jump-btn px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-yellow-400 border border-slate-700 font-bold">2. Automation Grid</button>
      <button data-target="b_data_lake" class="district-jump-btn px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-cyan-400 border border-slate-700 font-bold">3. Semantic Harbor</button>
      <button data-target="b_headless_gateway" class="district-jump-btn px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-emerald-400 border border-slate-700 font-bold">4. Headless 360</button>
      <button data-target="b_agentforce_core" class="district-jump-btn px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-purple-400 border border-slate-700 font-bold">5. Agentforce Hub</button>
      <button data-target="b_claudeforce_lab" class="district-jump-btn px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-orange-400 border border-slate-700 font-bold">6. Claudeforce</button>
      <button data-target="b_mcp_context" class="district-jump-btn px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-pink-400 border border-slate-700 font-bold">7. MCP Interchange</button>
    </div>
    <div class="hidden md:flex items-center gap-2 text-[10px] text-slate-500">
      <span>Drag: Pan</span> • <span>Scroll: Zoom</span> • <span>Click: Inspect</span>
    </div>
  </footer>

  <!-- Fullscreen Interactive Concept Modal / Academy -->
  <div id="concept-modal" class="hidden"></div>

  <script>
    {combined_js}
  </script>
</body>
</html>
"""

with open(artifact_path, 'w') as f:
    f.write(standalone_html)

print(f"Successfully generated standalone artifact at: {artifact_path}")
