modal_code = '''import { CONCEPT_GUIDES } from '../data/conceptGuides.js';
import { sfx } from '../engine/SoundFx.js';

export class ConceptModal {
  constructor(container) {
    this.container = container;
    this.activeTopic = 'headless360';
  }

  show(topicId = 'headless360') {
    this.activeTopic = topicId;
    this.container.classList.remove('hidden');
    this.render();
    sfx.openModal();
  }

  hide() {
    this.container.classList.add('hidden');
    sfx.closeModal();
  }

  setTopic(topicId) {
    this.activeTopic = topicId;
    sfx.click();
    this.render();
  }

  render() {
    const guide = CONCEPT_GUIDES[this.activeTopic];
    if (!guide) return;

    this.container.innerHTML = `
      <div class="modal-overlay">
        <div class="modal-window">
          
          <!-- Top Header -->
          <div style="padding: 18px 24px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: rgba(10, 16, 32, 0.9); display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 14px;">
              <span style="font-size: 26px;">${guide.icon}</span>
              <div>
                <h1 style="margin: 0; font-size: 17px; font-weight: 700; color: #ffffff; letter-spacing: -0.01em;">${guide.title}</h1>
                <p style="margin: 2px 0 0; font-size: 12px; color: #94a3b8;">${guide.subtitle}</p>
              </div>
            </div>
            <button id="btn-close-modal" class="btn-secondary" style="padding: 6px 12px; font-size: 13px;">
              ✕ Close
            </button>
          </div>

          <!-- Segmented Topic Tabs -->
          <div style="display: flex; gap: 4px; padding: 10px 24px; background: rgba(8, 12, 24, 0.6); border-bottom: 1px solid rgba(255, 255, 255, 0.06); overflow-x: auto;">
            <button data-topic="headless360" class="tab-btn segmented-btn ${this.activeTopic === 'headless360' ? 'active' : ''}">
              🚀 Headless 360
            </button>
            <button data-topic="agentforce" class="tab-btn segmented-btn ${this.activeTopic === 'agentforce' ? 'active' : ''}">
              🤖 Agentforce (Aiforce)
            </button>
            <button data-topic="claudeforce" class="tab-btn segmented-btn ${this.activeTopic === 'claudeforce' ? 'active' : ''}">
              🧠 Claudeforce (Claude 3.5)
            </button>
            <button data-topic="mcpApis" class="tab-btn segmented-btn ${this.activeTopic === 'mcpApis' ? 'active' : ''}">
              🔌 Dual-Plane MCPs & APIs
            </button>
            <button data-topic="semanticMatrix" class="tab-btn segmented-btn ${this.activeTopic === 'semanticMatrix' ? 'active' : ''}">
              🏢 Semantic Layer Matrix
            </button>
          </div>

          <!-- Content Body -->
          <div style="flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 24px; font-size: 13px; line-height: 1.6; color: #cbd5e1;">
            <!-- Tagline Pill -->
            <div style="padding: 12px 18px; border-radius: 10px; background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.2); display: flex; align-items: center; justify-content: space-between;">
              <span style="color: #7dd3fc; font-weight: 600; font-style: italic;">${guide.tagline}</span>
              <span class="badge-pill" style="background: rgba(56, 189, 248, 0.2); color: #38bdf8;">Enterprise Reference</span>
            </div>

            <!-- Topic Body -->
            ${this.renderTopicBody(guide)}
          </div>

          <!-- Footer -->
          <div style="padding: 14px 24px; border-top: 1px solid rgba(255, 255, 255, 0.08); background: rgba(10, 16, 32, 0.9); display: flex; align-items: center; justify-content: space-between; font-size: 12px; color: #64748b;">
            <span>Salesforce 2.5D Pixel City Architectural Academy</span>
            <button id="btn-close-modal-footer" class="btn-primary">
              Return to City Map
            </button>
          </div>
        </div>
      </div>
    `;

    this.container.querySelector('#btn-close-modal').onclick = () => this.hide();
    this.container.querySelector('#btn-close-modal-footer').onclick = () => this.hide();

    this.container.querySelectorAll('.tab-btn').forEach(btn => {
      btn.onclick = () => this.setTopic(btn.dataset.topic);
    });

    this.bindInteractiveWidgets();
  }

  renderTopicBody(guide) {
    if (this.activeTopic === 'headless360') {
      return `
        <p style="font-size: 14px; color: #f1f5f9; margin: 0;">${guide.summary}</p>

        <!-- Why It Matters Cards -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px;">
          ${guide.whyItMatters.map(item => `
            <div class="glass-card" style="padding: 16px;">
              <div style="font-weight: 700; color: #34d399; font-size: 13px; margin-bottom: 6px;">✓ ${item.title}</div>
              <div style="color: #94a3b8; font-size: 12px;">${item.description}</div>
            </div>
          `).join('')}
        </div>

        <!-- 4 Layers -->
        <div>
          <h2 style="font-size: 15px; font-weight: 700; color: #ffffff; margin: 0 0 12px;">The 4-Layer Headless 360 Architecture</h2>
          <div style="display: flex; flex-direction: column; gap: 10px;">
            ${guide.fourLayers.map(l => `
              <div style="padding: 14px; border-radius: 10px; border: 1px solid ${l.color}44; background: ${l.color}11;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <span style="font-weight: 700; color: ${l.color}; font-size: 13px;">${l.layer}</span>
                  <span style="font-size: 11px; color: #94a3b8; font-family: 'JetBrains Mono', monospace;">${l.components}</span>
                </div>
                <div style="color: #cbd5e1; font-size: 12px;">${l.description}</div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Comparison Table -->
        <div>
          <h2 style="font-size: 15px; font-weight: 700; color: #ffffff; margin: 0 0 12px;">Architectural Comparison: Monolith vs. Headless</h2>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
            <div class="glass-card" style="padding: 16px; border-color: rgba(239, 68, 68, 0.3); background: rgba(239, 68, 68, 0.05); display: flex; flex-direction: column; gap: 8px;">
              <div style="font-weight: 700; color: #f87171; font-size: 13px;">${guide.comparison.monolith.title}</div>
              <div style="display: flex; justify-content: space-between; font-size: 12px;"><span style="color: #94a3b8;">Bundle Transfer:</span> <span style="color: #fca5a5; font-weight: 700;">${guide.comparison.monolith.payloadSize}</span></div>
              <div style="display: flex; justify-content: space-between; font-size: 12px;"><span style="color: #94a3b8;">Initial Paint:</span> <span style="color: #fca5a5; font-weight: 700;">${guide.comparison.monolith.loadTime}</span></div>
              <div style="display: flex; justify-content: space-between; font-size: 12px;"><span style="color: #94a3b8;">Flexibility:</span> <span>${guide.comparison.monolith.flexibility}</span></div>
              <div style="display: flex; justify-content: space-between; font-size: 12px;"><span style="color: #94a3b8;">Agent Readiness:</span> <span style="color: #f87171;">${guide.comparison.monolith.agentUsability}</span></div>
            </div>

            <div class="glass-card" style="padding: 16px; border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.05); display: flex; flex-direction: column; gap: 8px;">
              <div style="font-weight: 700; color: #34d399; font-size: 13px;">${guide.comparison.headless.title}</div>
              <div style="display: flex; justify-content: space-between; font-size: 12px;"><span style="color: #94a3b8;">Payload Transfer:</span> <span style="color: #6ee7b7; font-weight: 700;">${guide.comparison.headless.payloadSize}</span></div>
              <div style="display: flex; justify-content: space-between; font-size: 12px;"><span style="color: #94a3b8;">API Roundtrip:</span> <span style="color: #6ee7b7; font-weight: 700;">${guide.comparison.headless.loadTime}</span></div>
              <div style="display: flex; justify-content: space-between; font-size: 12px;"><span style="color: #94a3b8;">Flexibility:</span> <span>${guide.comparison.headless.flexibility}</span></div>
              <div style="display: flex; justify-content: space-between; font-size: 12px;"><span style="color: #94a3b8;">Agent Readiness:</span> <span style="color: #34d399; font-weight: 700;">${guide.comparison.headless.agentUsability}</span></div>
            </div>
          </div>
        </div>

        <!-- Sample Code -->
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; color: #ffffff; font-size: 13px;">${guide.sampleCode.title}</span>
            <span class="badge-pill" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">Single Roundtrip</span>
          </div>
          <pre style="margin: 0; padding: 14px; background: rgba(5, 8, 17, 0.95); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; overflow-x: auto; color: #6ee7b7; font-family: 'JetBrains Mono', monospace; font-size: 11.5px;"><code>${escapeHtml(guide.sampleCode.code)}</code></pre>
        </div>
      `;
    } else if (this.activeTopic === 'agentforce') {
      return `
        <p style="font-size: 14px; color: #f1f5f9; margin: 0;">${guide.summary}</p>

        <!-- Atlas Reasoning Loop -->
        <div>
          <h2 style="font-size: 15px; font-weight: 700; color: #ffffff; margin: 0 0 12px;">The Atlas Reasoning Engine Loop</h2>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px;">
            ${guide.atlasCycle.map(s => `
              <div class="glass-card" style="padding: 14px; border-color: rgba(168, 85, 247, 0.25);">
                <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; color: #c084fc; font-size: 12.5px; margin-bottom: 6px;">
                  <span>${s.icon}</span>
                  <span>${s.step}</span>
                </div>
                <div style="color: #94a3b8; font-size: 11.5px;">${s.description}</div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Interactive Atlas Reasoning Simulator -->
        <div class="glass-panel" style="padding: 18px; border-color: rgba(168, 85, 247, 0.4); display: flex; flex-direction: column; gap: 12px;">
          <div style="display: flex; align-items: center; justify-content: space-between;">
            <h3 style="margin: 0; font-size: 14px; font-weight: 700; color: #d8b4fe;">⚡ Live Atlas Reasoning Loop Simulator</h3>
            <span class="badge-pill" style="background: rgba(168, 85, 247, 0.2); color: #c084fc;">Interactive Playground</span>
          </div>
          <p style="margin: 0; color: #94a3b8; font-size: 12px;">
            Select a real-world enterprise situation to watch the Atlas loop perceive intent, apply trust layer masking, classify topics, ground in Data Cloud, and dispatch invocable tools:
          </p>

          <div style="display: flex; gap: 10px;">
            <button id="sim-scenario-1" class="btn-secondary">
              Scenario A: Cold-Chain Waterlogging Crisis
            </button>
            <button id="sim-scenario-2" class="btn-secondary">
              Scenario B: VIP Churn Risk SLA
            </button>
          </div>

          <div id="atlas-sim-output" style="padding: 14px; background: rgba(5, 8, 17, 0.95); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 11.5px; min-height: 140px; display: flex; flex-direction: column; gap: 8px;">
            <div style="color: #64748b;">// Select a scenario above to run the Atlas perception loop...</div>
          </div>
        </div>

        <!-- Sample Code -->
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; color: #ffffff; font-size: 13px;">${guide.sampleCode.title}</span>
            <span class="badge-pill" style="background: rgba(168, 85, 247, 0.2); color: #c084fc;">WITH USER_MODE</span>
          </div>
          <pre style="margin: 0; padding: 14px; background: rgba(5, 8, 17, 0.95); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; overflow-x: auto; color: #c084fc; font-family: 'JetBrains Mono', monospace; font-size: 11.5px;"><code>${escapeHtml(guide.sampleCode.code)}</code></pre>
        </div>
      `;
    } else if (this.activeTopic === 'claudeforce') {
      return `
        <p style="font-size: 14px; color: #f1f5f9; margin: 0;">${guide.summary}</p>

        <!-- Core Powers -->
        <div>
          <h2 style="font-size: 15px; font-weight: 700; color: #ffffff; margin: 0 0 12px;">Claude 3.5 Sonnet: Enterprise Capabilities</h2>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px;">
            ${guide.corePowers.map(p => `
              <div class="glass-card" style="padding: 16px; border-color: rgba(249, 115, 22, 0.25);">
                <div style="font-weight: 700; color: #fb923c; font-size: 13px; margin-bottom: 6px;">⚡ ${p.title}</div>
                <div style="color: #94a3b8; font-size: 12px;">${p.description}</div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Workflow Walkthrough -->
        <div class="glass-panel" style="padding: 18px; border-color: rgba(249, 115, 22, 0.4); display: flex; flex-direction: column; gap: 10px;">
          <h3 style="margin: 0; font-size: 14px; font-weight: 700; color: #fdba74;">👁️ Multi-Modal Manifest Processing Pipeline</h3>
          ${guide.workflowExample.map(w => `
            <div style="display: flex; gap: 10px; font-size: 12.5px;">
              <span style="color: #fb923c; font-weight: 700; white-space: nowrap;">${w.step}:</span>
              <span style="color: #cbd5e1;">${w.text}</span>
            </div>
          `).join('')}
        </div>

        <!-- Sample Code -->
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; color: #ffffff; font-size: 13px;">${guide.sampleCode.title}</span>
            <span class="badge-pill" style="background: rgba(249, 115, 22, 0.2); color: #fb923c;">200k Context</span>
          </div>
          <pre style="margin: 0; padding: 14px; background: rgba(5, 8, 17, 0.95); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; overflow-x: auto; color: #fdba74; font-family: 'JetBrains Mono', monospace; font-size: 11.5px;"><code>${escapeHtml(guide.sampleCode.code)}</code></pre>
        </div>
      `;
    } else if (this.activeTopic === 'mcpApis') {
      return `
        <p style="font-size: 14px; color: #f1f5f9; margin: 0;">${guide.summary}</p>

        <!-- Dual Planes -->
        <div>
          <h2 style="font-size: 15px; font-weight: 700; color: #ffffff; margin: 0 0 12px;">The Dual-Plane Hosted MCP Architecture</h2>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
            ${guide.dualPlanes.map(p => `
              <div style="padding: 16px; border-radius: 12px; border: 1px solid ${p.color}55; background: ${p.color}11; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-weight: 700; font-size: 14px; color: ${p.color};">${p.plane}</span>
                    <span class="badge-pill" style="background: rgba(255, 255, 255, 0.1); color: #ffffff;">${p.status}</span>
                  </div>
                  <div style="font-size: 11px; color: #94a3b8; font-family: 'JetBrains Mono', monospace; margin-bottom: 10px;">${p.endpoint}</div>
                  
                  <div style="margin-bottom: 12px;">
                    <div style="font-size: 11px; font-weight: 700; color: #ffffff; margin-bottom: 4px; text-transform: uppercase;">Exposed Tools:</div>
                    <ul style="margin: 0; padding-left: 18px; font-family: 'JetBrains Mono', monospace; font-size: 11.5px; color: #cbd5e1; display: flex; flex-direction: column; gap: 4px;">
                      ${p.tools.map(t => `<li>${t}</li>`).join('')}
                    </ul>
                  </div>
                </div>

                <div style="padding-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.08); font-size: 11.5px; color: #94a3b8;">
                  <strong style="color: #ffffff;">Security:</strong> ${p.security}
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- API Landscape -->
        <div>
          <h2 style="font-size: 15px; font-weight: 700; color: #ffffff; margin: 0 0 12px;">Modern Salesforce API Landscape</h2>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
            ${guide.apiLandscape.map(api => `
              <div class="glass-card" style="padding: 12px;">
                <div style="font-weight: 700; color: #f472b6; font-size: 12.5px;">${api.name}</div>
                <div style="font-size: 10.5px; color: #94a3b8; font-weight: 600; text-transform: uppercase; margin-bottom: 4px;">${api.type}</div>
                <div style="font-size: 11.5px; color: #cbd5e1;">${api.bestFor}</div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Sample Code -->
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; color: #ffffff; font-size: 13px;">${guide.sampleCode.title}</span>
            <span class="badge-pill" style="background: rgba(236, 72, 153, 0.2); color: #f472b6;">JSON-RPC 2.0</span>
          </div>
          <pre style="margin: 0; padding: 14px; background: rgba(5, 8, 17, 0.95); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; overflow-x: auto; color: #f472b6; font-family: 'JetBrains Mono', monospace; font-size: 11.5px;"><code>${escapeHtml(guide.sampleCode.code)}</code></pre>
        </div>
      `;
    } else {
      return `
        <p style="font-size: 14px; color: #f1f5f9; margin: 0;">${guide.summary}</p>

        <div style="display: flex; flex-direction: column; gap: 14px;">
          ${guide.tiers.map(t => `
            <div class="glass-card" style="padding: 18px; border-color: rgba(56, 189, 248, 0.3);">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-weight: 700; font-size: 14px; color: #38bdf8;">${t.tier}</span>
                <span class="badge-pill" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8;">${t.metaphor}</span>
              </div>
              <div style="font-size: 12px; color: #94a3b8; margin-bottom: 6px;"><strong style="color: #ffffff;">Technology:</strong> ${t.technology}</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-bottom: 8px;">${t.content}</div>
              <div style="font-size: 11.5px; color: #34d399; font-weight: 600;">Access Layer: ${t.visibility}</div>
            </div>
          `).join('')}
        </div>
      `;
    }
  }

  bindInteractiveWidgets() {
    const simBtn1 = this.container.querySelector('#sim-scenario-1');
    const simBtn2 = this.container.querySelector('#sim-scenario-2');
    const simOutput = this.container.querySelector('#atlas-sim-output');

    if (simBtn1 && simOutput) {
      simBtn1.onclick = () => {
        sfx.simulationStep();
        simOutput.innerHTML = `
          <div style="color: #c084fc; font-weight: 700;">▶ Ingesting Telemetry: Sensor DC-HYD-04 records 9.2°C Excursion (Shipment SH-88392)...</div>
          <div style="color: #cbd5e1;">🛡️ Einstein Trust Layer: Masking PII and evaluating harm score (0.001 - Pass).</div>
          <div style="color: #cbd5e1;">🎯 Topic Matched: <span style="color: #facc15; font-weight: 700;">ColdChain_Rescue</span> (Confidence 0.992)</div>
          <div style="color: #cbd5e1;">🌐 Data 360 Grounding: Dr. Meera Reddy (Consignee) linked to VIP Household graph UID-88291.</div>
          <div style="color: #cbd5e1;">⚡ Action Planned: Invocable <span style="color: #34d399; font-weight: 700;">INDRA_UnifiedContextService.executeRescue</span></div>
          <div style="color: #34d399; font-weight: 700;">✓ P0 Case CASE-99120 inserted as user. Rescue drone dispatched to Banjara Hills!</div>
        `;
      };
    }

    if (simBtn2 && simOutput) {
      simBtn2.onclick = () => {
        sfx.simulationStep();
        simOutput.innerHTML = `
          <div style="color: #c084fc; font-weight: 700;">▶ Ingesting Inbound Signal: Consignee inquiry on delayed linehaul...</div>
          <div style="color: #cbd5e1;">🛡️ Einstein Trust Layer: De-identifying phone number to synthetic token.</div>
          <div style="color: #cbd5e1;">🎯 Topic Matched: <span style="color: #facc15; font-weight: 700;">VIP_Intervention</span> (Confidence 0.988)</div>
          <div style="color: #cbd5e1;">🌐 Data 360 Calculated Insights: Care Risk Score = 88.4 (High Severity).</div>
          <div style="color: #cbd5e1;">⚡ Action Planned: Trigger Autolaunched Rescue Flow + Post to Slack Concierge.</div>
          <div style="color: #34d399; font-weight: 700;">✓ Dedicated specialist Ananya Rao notified in Slack with pre-authorized waiver.</div>
        `;
      };
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

with open('/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer/src/components/ConceptModal.js', 'w') as f:
    f.write(modal_code)

print("Upgraded ConceptModal.js written successfully!")
