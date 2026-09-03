import { sfx } from '../engine/SoundFx.js';

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
        <!-- Architectural Header -->
        <div style="padding: 16px 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: rgba(8, 12, 22, 0.85); display: flex; align-items: flex-start; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 14px;">
            <div style="width: 40px; height: 40px; border-radius: 8px; background: ${b.color}18; border: 1px solid ${b.color}; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: 700; color: ${b.color}; box-shadow: 0 0 16px ${b.color}33;">
              ${b.districtId.substring(0, 2).toUpperCase()}
            </div>
            <div>
              <div style="display: flex; align-items: center; gap: 8px;">
                <h2 style="margin: 0; font-size: 15px; font-weight: 700; color: #ffffff; letter-spacing: -0.01em;">${b.name}</h2>
              </div>
              <p style="margin: 2px 0 0; font-size: 11px; color: #94a3b8; font-family: 'JetBrains Mono', monospace;">${b.subtitle}</p>
            </div>
          </div>
          <button id="btn-close-inspector" class="action-btn-ghost" style="padding: 4px 8px; font-size: 12px;">
            ✕
          </button>
        </div>

        <!-- Architectural Dimension Strips -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; padding: 12px 18px; background: rgba(5, 8, 16, 0.7); border-bottom: 1px solid rgba(255, 255, 255, 0.06); text-align: center;">
          <div class="arch-card" style="padding: 8px;">
            <div style="font-size: 10px; color: #64748b; font-family: 'JetBrains Mono', monospace; text-transform: uppercase;">Elevation</div>
            <div style="font-size: 12px; font-weight: 700; color: #38bdf8; font-family: 'JetBrains Mono', monospace;">EL +${b.floors * 3}m</div>
          </div>
          <div class="arch-card" style="padding: 8px;">
            <div style="font-size: 10px; color: #64748b; font-family: 'JetBrains Mono', monospace; text-transform: uppercase;">Grid Datum</div>
            <div style="font-size: 12px; font-weight: 700; color: #10b981; font-family: 'JetBrains Mono', monospace;">[${b.gridX}, ${b.gridY}]</div>
          </div>
          <div class="arch-card" style="padding: 8px;">
            <div style="font-size: 10px; color: #64748b; font-family: 'JetBrains Mono', monospace; text-transform: uppercase;">Topology</div>
            <div style="font-size: 12px; font-weight: 700; color: #a855f7; font-family: 'JetBrains Mono', monospace;">${b.relationships ? b.relationships.length : 0} Ports</div>
          </div>
        </div>

        <!-- Tab Selector -->
        <div style="display: flex; border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: rgba(8, 12, 22, 0.5);">
          <button id="tab-overview" class="program-btn ${this.activeTab === 'overview' ? 'active' : ''}" style="flex: 1; border-radius: 0; padding: 10px; font-size: 12px;">
            Architectural Role
          </button>
          <button id="tab-schema" class="program-btn ${this.activeTab === 'schema' ? 'active' : ''}" style="flex: 1; border-radius: 0; padding: 10px; font-size: 12px;">
            Schema & Contract
          </button>
          <button id="tab-action" class="program-btn ${this.activeTab === 'action' ? 'active' : ''}" style="flex: 1; border-radius: 0; padding: 10px; font-size: 12px;">
            Circulation Test
          </button>
        </div>

        <!-- Body Content -->
        <div style="flex: 1; overflow-y: auto; padding: 18px; display: flex; flex-direction: column; gap: 16px; font-size: 12.5px; line-height: 1.6;">
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
          <div style="font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; margin-bottom: 4px;">Structural Function</div>
          <p style="margin: 0; color: #f1f5f9; font-weight: 500;">${b.summary}</p>
        </div>

        <div class="arch-card" style="padding: 12px;">
          <div style="font-size: 10.5px; font-weight: 700; color: #38bdf8; text-transform: uppercase; margin-bottom: 4px;">Ecosystem Integration</div>
          <p style="margin: 0; color: #94a3b8; font-size: 11.5px;">${b.explanation}</p>
        </div>

        <div>
          <div style="font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; margin-bottom: 8px;">Architectural Classifications</div>
          <div style="display: flex; flex-wrap: wrap; gap: 6px;">
            ${b.tags.map(t => `<span class="datum-tag">${t}</span>`).join('')}
          </div>
        </div>

        ${b.metrics ? `
          <div>
            <div style="font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; margin-bottom: 8px;">Telemetry Specifications</div>
            <div class="arch-card" style="padding: 10px; display: flex; flex-direction: column; gap: 6px;">
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
            <span style="font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace; text-transform: uppercase;">Metadata Schema</span>
            <span class="datum-tag" style="color: #38bdf8;">XML / APEX / SOQL</span>
          </div>
          <pre><code>${escapeHtml(b.schemaSnippet || '// No schema definition')}</code></pre>
        </div>
      `;
    } else {
      return `
        <div style="display: flex; flex-direction: column; gap: 12px;">
          <div>
            <div style="font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; margin-bottom: 4px;">Circulation Simulation</div>
            <p style="margin: 0; color: #94a3b8; font-size: 11.5px;">
              Dispatch an operational data packet from <strong style="color: #38bdf8;">${b.name}</strong> along connected conduits to trigger downstream automation and cognitive reasoning.
            </p>
          </div>

          <button id="btn-trigger-action" class="action-btn-primary" style="justify-content: center; width: 100%; padding: 10px 16px;">
            ⚡ Broadcast Circulation Packet
          </button>

          <div id="action-console-log" style="padding: 12px; background: #050811; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 11px; min-height: 140px; display: flex; flex-direction: column; gap: 6px;">
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
