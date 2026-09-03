inspector_code = '''import { sfx } from '../engine/SoundFx.js';

export class BuildingInspector {
  constructor(container, onActionTriggered) {
    this.container = container;
    this.onActionTriggered = onActionTriggered;
    this.currentBuilding = null;
    this.activeTab = 'overview'; // 'overview', 'schema', 'action'
  }

  show(building) {
    this.currentBuilding = building;
    this.container.classList.remove('hidden');
    this.render();
    sfx.buildingSelect();
  }

  hide() {
    this.container.classList.add('hidden');
    this.currentBuilding = null;
    sfx.closeModal();
  }

  setTab(tab) {
    this.activeTab = tab;
    sfx.click();
    this.render();
  }

  render() {
    if (!this.currentBuilding) return;
    const b = this.currentBuilding;

    this.container.innerHTML = `
      <div class="pixel-panel flex flex-col h-full">
        <!-- Panel Header -->
        <div class="flex items-start justify-between p-4 border-b border-slate-700 bg-slate-900/80">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded flex items-center justify-center text-xl" style="background: ${b.color}22; border: 1px solid ${b.color}">
              🏢
            </div>
            <div>
              <div class="flex items-center gap-2">
                <h2 class="text-base font-bold text-white tracking-wide font-mono">${b.name}</h2>
                <span class="text-xs px-2 py-0.5 rounded font-mono uppercase" style="background: ${b.color}33; color: ${b.color}; border: 1px solid ${b.color}66">
                  ${b.districtId}
                </span>
              </div>
              <p class="text-xs text-slate-400 font-mono mt-0.5">${b.subtitle}</p>
            </div>
          </div>
          <button id="btn-close-inspector" class="text-slate-400 hover:text-white text-lg px-2 py-1 bg-slate-800 rounded border border-slate-700 hover:bg-slate-700">
            ✕
          </button>
        </div>

        <!-- Metric Badges -->
        <div class="grid grid-cols-3 gap-2 p-3 bg-slate-950/60 border-b border-slate-800 text-center font-mono">
          <div class="p-1.5 bg-slate-900/60 rounded border border-slate-800">
            <div class="text-[10px] text-slate-400 uppercase">Floors / Scale</div>
            <div class="text-sm font-bold text-sky-400">${b.floors} F</div>
          </div>
          <div class="p-1.5 bg-slate-900/60 rounded border border-slate-800">
            <div class="text-[10px] text-slate-400 uppercase">Grid Coord</div>
            <div class="text-sm font-bold text-emerald-400">${b.gridX}, ${b.gridY}</div>
          </div>
          <div class="p-1.5 bg-slate-900/60 rounded border border-slate-800">
            <div class="text-[10px] text-slate-400 uppercase">Relations</div>
            <div class="text-sm font-bold text-purple-400">${b.relationships ? b.relationships.length : 0}</div>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="flex border-b border-slate-800 bg-slate-900/40 text-xs font-mono">
          <button id="tab-overview" class="flex-1 py-2.5 px-3 text-center border-b-2 transition-colors ${this.activeTab === 'overview' ? 'border-sky-400 text-sky-400 bg-sky-950/30' : 'border-transparent text-slate-400 hover:text-slate-200'}">
            🏛️ Overview
          </button>
          <button id="tab-schema" class="flex-1 py-2.5 px-3 text-center border-b-2 transition-colors ${this.activeTab === 'schema' ? 'border-sky-400 text-sky-400 bg-sky-950/30' : 'border-transparent text-slate-400 hover:text-slate-200'}">
            📜 Schema / Code
          </button>
          <button id="tab-action" class="flex-1 py-2.5 px-3 text-center border-b-2 transition-colors ${this.activeTab === 'action' ? 'border-sky-400 text-sky-400 bg-sky-950/30' : 'border-transparent text-slate-400 hover:text-slate-200'}">
            🚀 Live Test
          </button>
        </div>

        <!-- Tab Content Body -->
        <div class="flex-1 overflow-y-auto p-4 space-y-4 font-mono text-xs leading-relaxed text-slate-300">
          ${this.renderTabContent(b)}
        </div>
      </div>
    `;

    // Bind event listeners
    this.container.querySelector('#btn-close-inspector').onclick = () => this.hide();
    this.container.querySelector('#tab-overview').onclick = () => this.setTab('overview');
    this.container.querySelector('#tab-schema').onclick = () => this.setTab('schema');
    this.container.querySelector('#tab-action').onclick = () => this.setTab('action');

    const triggerBtn = this.container.querySelector('#btn-trigger-action');
    if (triggerBtn) {
      triggerBtn.onclick = () => {
        if (this.onActionTriggered) {
          this.onActionTriggered(b);
        }
      };
    }
  }

  renderTabContent(b) {
    if (this.activeTab === 'overview') {
      return `
        <div>
          <h3 class="text-white font-bold text-sm mb-1">Architectural Role</h3>
          <p class="text-slate-300">${b.summary}</p>
        </div>

        <div class="p-3 bg-slate-900/80 rounded border border-slate-800">
          <h4 class="text-sky-400 font-bold mb-1.5 text-xs">Org Context & Integration</h4>
          <p class="text-slate-400 text-[11px]">${b.explanation}</p>
        </div>

        <div>
          <h4 class="text-slate-400 text-[11px] uppercase tracking-wider mb-2">Metadata Tags</h4>
          <div class="flex flex-wrap gap-1.5">
            ${b.tags.map(t => `<span class="px-2 py-0.5 bg-slate-800 text-slate-300 rounded text-[10px] border border-slate-700">${t}</span>`).join('')}
          </div>
        </div>

        ${b.metrics ? `
          <div>
            <h4 class="text-slate-400 text-[11px] uppercase tracking-wider mb-2">Live Production Metrics</h4>
            <div class="bg-slate-950 p-2.5 rounded border border-slate-800 space-y-1">
              ${Object.entries(b.metrics).map(([k, v]) => `
                <div class="flex justify-between text-[11px]">
                  <span class="text-slate-400">${k}:</span>
                  <span class="text-emerald-400 font-bold">${v}</span>
                </div>
              `).join('')}
            </div>
          </div>
        ` : ''}
      `;
    } else if (this.activeTab === 'schema') {
      return `
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="text-slate-400 text-[11px] uppercase">Metadata Representation</span>
            <span class="text-[10px] text-sky-400 bg-sky-950/40 px-1.5 py-0.5 rounded border border-sky-800">XML / Apex / SOQL</span>
          </div>
          <pre class="p-3 bg-slate-950 text-emerald-300 rounded border border-slate-800 overflow-x-auto text-[11px] leading-relaxed select-all"><code>${escapeHtml(b.schemaSnippet || '// No code definition available')}</code></pre>
        </div>
      `;
    } else {
      return `
        <div class="space-y-3">
          <h3 class="text-white font-bold text-sm">Interactive Action Dispatcher</h3>
          <p class="text-slate-400 text-[11px]">
            Trigger a simulated enterprise transaction from <span class="text-sky-400">${b.name}</span> across connected org nodes (Flows, Atlas Engine, and MCP Conduits).
          </p>

          <button id="btn-trigger-action" class="w-full py-2.5 px-4 bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-500 hover:to-indigo-500 text-white font-bold rounded shadow-lg transition-all flex items-center justify-center gap-2">
            <span>⚡ Dispatch Action from ${b.name}</span>
          </button>

          <div id="action-console-log" class="p-3 bg-slate-950 rounded border border-slate-800 text-[11px] font-mono space-y-1.5 min-h-[120px]">
            <div class="text-slate-500">// Ready to dispatch test packet...</div>
          </div>
        </div>
      `;
    }
  }
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
'''

with open('/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer/src/components/BuildingInspector.js', 'w') as f:
    f.write(inspector_code)

print("BuildingInspector.js written successfully!")
