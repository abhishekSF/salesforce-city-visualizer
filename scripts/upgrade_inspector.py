inspector_code = '''import { sfx } from '../engine/SoundFx.js';

export class BuildingInspector {
  constructor(container, onActionTriggered) {
    this.container = container;
    this.onActionTriggered = onActionTriggered;
    this.currentBuilding = null;
    this.activeTab = 'overview';
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
      <div class="flex flex-col h-full text-slate-200">
        <!-- Header -->
        <div style="padding: 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: rgba(15, 23, 42, 0.6); display: flex; align-items: flex-start; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 40px; height: 40px; border-radius: 10px; background: ${b.color}22; border: 1px solid ${b.color}; display: flex; align-items: center; justify-content: center; font-size: 20px; box-shadow: 0 0 12px ${b.color}44;">
              🏢
            </div>
            <div>
              <div style="display: flex; align-items: center; gap: 8px;">
                <h2 style="margin: 0; font-size: 15px; font-weight: 700; color: #ffffff;">${b.name}</h2>
                <span class="badge-pill" style="background: ${b.color}22; color: ${b.color}; border: 1px solid ${b.color}55;">
                  ${b.districtId}
                </span>
              </div>
              <p style="margin: 2px 0 0; font-size: 11px; color: #94a3b8;">${b.subtitle}</p>
            </div>
          </div>
          <button id="btn-close-inspector" style="background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.1); color: #94a3b8; border-radius: 8px; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s;">
            ✕
          </button>
        </div>

        <!-- Metrics Strip -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; padding: 12px 16px; background: rgba(8, 12, 24, 0.7); border-bottom: 1px solid rgba(255, 255, 255, 0.06); text-align: center;">
          <div class="glass-card" style="padding: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase; font-weight: 600;">Height</div>
            <div style="font-size: 13px; font-weight: 700; color: #38bdf8; font-family: 'JetBrains Mono', monospace;">${b.floors} Floors</div>
          </div>
          <div class="glass-card" style="padding: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase; font-weight: 600;">Grid Position</div>
            <div style="font-size: 13px; font-weight: 700; color: #10b981; font-family: 'JetBrains Mono', monospace;">${b.gridX}, ${b.gridY}</div>
          </div>
          <div class="glass-card" style="padding: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase; font-weight: 600;">Topology</div>
            <div style="font-size: 13px; font-weight: 700; color: #a855f7; font-family: 'JetBrains Mono', monospace;">${b.relationships ? b.relationships.length : 0} Nodes</div>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <div style="display: flex; border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: rgba(12, 18, 36, 0.5);">
          <button id="tab-overview" style="flex: 1; padding: 10px; text-align: center; font-size: 12px; font-weight: 600; cursor: pointer; border: none; border-bottom: 2px solid ${this.activeTab === 'overview' ? '#38bdf8' : 'transparent'}; color: ${this.activeTab === 'overview' ? '#38bdf8' : '#94a3b8'}; background: transparent; transition: all 0.2s;">
            Overview
          </button>
          <button id="tab-schema" style="flex: 1; padding: 10px; text-align: center; font-size: 12px; font-weight: 600; cursor: pointer; border: none; border-bottom: 2px solid ${this.activeTab === 'schema' ? '#38bdf8' : 'transparent'}; color: ${this.activeTab === 'schema' ? '#38bdf8' : '#94a3b8'}; background: transparent; transition: all 0.2s;">
            Metadata & Code
          </button>
          <button id="tab-action" style="flex: 1; padding: 10px; text-align: center; font-size: 12px; font-weight: 600; cursor: pointer; border: none; border-bottom: 2px solid ${this.activeTab === 'action' ? '#38bdf8' : 'transparent'}; color: ${this.activeTab === 'action' ? '#38bdf8' : '#94a3b8'}; background: transparent; transition: all 0.2s;">
            Live Dispatch
          </button>
        </div>

        <!-- Content Body -->
        <div style="flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 16px; font-size: 12.5px; line-height: 1.6;">
          ${this.renderBodyContent(b)}
        </div>
      </div>
    `;

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

  renderBodyContent(b) {
    if (this.activeTab === 'overview') {
      return `
        <div>
          <h3 style="margin: 0 0 6px; font-size: 13px; font-weight: 700; color: #ffffff;">Architectural Purpose</h3>
          <p style="margin: 0; color: #cbd5e1;">${b.summary}</p>
        </div>

        <div class="glass-card" style="padding: 12px;">
          <h4 style="margin: 0 0 6px; font-size: 11px; font-weight: 700; color: #38bdf8; text-transform: uppercase;">Role in Salesforce Ecosystem</h4>
          <p style="margin: 0; color: #94a3b8; font-size: 11.5px;">${b.explanation}</p>
        </div>

        <div>
          <h4 style="margin: 0 0 8px; font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase;">Metadata Classifications</h4>
          <div style="display: flex; flex-wrap: wrap; gap: 6px;">
            ${b.tags.map(t => `<span class="badge-pill" style="background: rgba(255, 255, 255, 0.05); color: #cbd5e1; border: 1px solid rgba(255, 255, 255, 0.08);">${t}</span>`).join('')}
          </div>
        </div>

        ${b.metrics ? `
          <div>
            <h4 style="margin: 0 0 8px; font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase;">Runtime Telemetry</h4>
            <div class="glass-card" style="padding: 10px; display: flex; flex-direction: column; gap: 6px;">
              ${Object.entries(b.metrics).map(([k, v]) => `
                <div style="display: flex; justify-content: space-between; font-size: 11.5px;">
                  <span style="color: #94a3b8;">${k}</span>
                  <span style="color: #10b981; font-weight: 600; font-family: 'JetBrains Mono', monospace;">${v}</span>
                </div>
              `).join('')}
            </div>
          </div>
        ` : ''}
      `;
    } else if (this.activeTab === 'schema') {
      return `
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 600;">Declarative Definition</span>
            <span class="badge-pill" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3);">XML / SOQL / Apex</span>
          </div>
          <pre style="margin: 0; padding: 14px; background: rgba(5, 8, 17, 0.95); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; overflow-x: auto; color: #6ee7b7; font-family: 'JetBrains Mono', monospace; font-size: 11px; line-height: 1.55;"><code>${escapeHtml(b.schemaSnippet || '// No schema definition')}</code></pre>
        </div>
      `;
    } else {
      return `
        <div style="display: flex; flex-direction: column; gap: 12px;">
          <div>
            <h3 style="margin: 0 0 4px; font-size: 13px; font-weight: 700; color: #ffffff;">Simulate Enterprise Event</h3>
            <p style="margin: 0; color: #94a3b8; font-size: 11.5px;">
              Broadcast a state change from <strong style="color: #38bdf8;">${b.name}</strong> along connected conduits to trigger automation and agent reasoning.
            </p>
          </div>

          <button id="btn-trigger-action" class="btn-primary" style="justify-content: center; width: 100%; padding: 10px 16px;">
            ⚡ Dispatch Event Packet
          </button>

          <div id="action-console-log" style="padding: 12px; background: rgba(5, 8, 17, 0.95); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 11px; min-height: 140px; display: flex; flex-direction: column; gap: 6px;">
            <div style="color: #64748b;">// Ready to dispatch packet...</div>
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

print("Upgraded BuildingInspector.js written successfully!")
