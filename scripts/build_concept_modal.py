modal_code = '''import { CONCEPT_GUIDES } from '../data/conceptGuides.js';
import { sfx } from '../engine/SoundFx.js';

export class ConceptModal {
  constructor(container) {
    this.container = container;
    this.activeTopic = 'headless360'; // 'headless360', 'agentforce', 'claudeforce', 'mcpApis', 'semanticMatrix'
    this.simStep = 0;
    this.simRunning = false;
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
    this.simStep = 0;
    this.simRunning = false;
    sfx.click();
    this.render();
  }

  render() {
    const guide = CONCEPT_GUIDES[this.activeTopic];
    if (!guide) return;

    this.container.innerHTML = `
      <div class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
        <div class="pixel-panel w-full max-w-5xl h-[85vh] flex flex-col bg-slate-900 border border-slate-700 rounded-lg shadow-2xl overflow-hidden font-mono">
          
          <!-- Top Header -->
          <div class="flex items-center justify-between p-4 border-b border-slate-700 bg-slate-950/90">
            <div class="flex items-center gap-3">
              <span class="text-2xl">${guide.icon}</span>
              <div>
                <h1 class="text-lg font-bold text-white tracking-wide">${guide.title}</h1>
                <p class="text-xs text-slate-400">${guide.subtitle}</p>
              </div>
            </div>
            <button id="btn-close-modal" class="text-slate-400 hover:text-white text-lg px-2.5 py-1 bg-slate-800 rounded border border-slate-700 hover:bg-slate-700">
              ✕
            </button>
          </div>

          <!-- Main Nav Tabs -->
          <div class="flex flex-wrap border-b border-slate-800 bg-slate-950/50 text-xs">
            <button data-topic="headless360" class="tab-btn px-4 py-3 font-bold border-b-2 transition-colors ${this.activeTopic === 'headless360' ? 'border-emerald-400 text-emerald-400 bg-emerald-950/20' : 'border-transparent text-slate-400 hover:text-slate-200'}">
              🚀 Headless 360
            </button>
            <button data-topic="agentforce" class="tab-btn px-4 py-3 font-bold border-b-2 transition-colors ${this.activeTopic === 'agentforce' ? 'border-purple-400 text-purple-400 bg-purple-950/20' : 'border-transparent text-slate-400 hover:text-slate-200'}">
              🤖 Agentforce (Aiforce)
            </button>
            <button data-topic="claudeforce" class="tab-btn px-4 py-3 font-bold border-b-2 transition-colors ${this.activeTopic === 'claudeforce' ? 'border-orange-400 text-orange-400 bg-orange-950/20' : 'border-transparent text-slate-400 hover:text-slate-200'}">
              🧠 Claudeforce (Claude 3.5)
            </button>
            <button data-topic="mcpApis" class="tab-btn px-4 py-3 font-bold border-b-2 transition-colors ${this.activeTopic === 'mcpApis' ? 'border-pink-400 text-pink-400 bg-pink-950/20' : 'border-transparent text-slate-400 hover:text-slate-200'}">
              🔌 Dual-Plane MCPs & APIs
            </button>
            <button data-topic="semanticMatrix" class="tab-btn px-4 py-3 font-bold border-b-2 transition-colors ${this.activeTopic === 'semanticMatrix' ? 'border-sky-400 text-sky-400 bg-sky-950/20' : 'border-transparent text-slate-400 hover:text-slate-200'}">
              🏢 Semantic Layer Matrix
            </button>
          </div>

          <!-- Modal Body Content -->
          <div class="flex-1 overflow-y-auto p-6 space-y-6 text-slate-300 text-xs leading-relaxed">
            <!-- Tagline banner -->
            <div class="p-3 bg-slate-950/80 rounded border border-slate-800 flex items-center justify-between">
              <span class="text-sky-300 font-bold italic">${guide.tagline}</span>
              <span class="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 uppercase">Enterprise Standard</span>
            </div>

            <!-- Main Topic Specific Body -->
            ${this.renderTopicBody(guide)}
          </div>

          <!-- Bottom Footer -->
          <div class="p-3 bg-slate-950/80 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
            <span>Salesforce 2.5D Pixel City Architectural Academy</span>
            <button id="btn-close-modal-footer" class="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded border border-slate-700 font-bold">
              Return to City Map
            </button>
          </div>
        </div>
      </div>
    `;

    // Bind listeners
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
        <!-- Summary -->
        <p class="text-sm text-slate-200">${guide.summary}</p>

        <!-- Why it matters -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          ${guide.whyItMatters.map(item => `
            <div class="p-3 bg-slate-950 rounded border border-slate-800">
              <h3 class="text-emerald-400 font-bold text-xs mb-1">✓ ${item.title}</h3>
              <p class="text-slate-400 text-[11px]">${item.description}</p>
            </div>
          `).join('')}
        </div>

        <!-- Four Layers of Headless 360 -->
        <div>
          <h2 class="text-sm font-bold text-white mb-2">The 4-Layer Headless 360 Architecture</h2>
          <div class="space-y-2">
            ${guide.fourLayers.map(l => `
              <div class="p-3 rounded border" style="border-color: ${l.color}44; background: ${l.color}11">
                <div class="flex items-center justify-between mb-1">
                  <span class="font-bold text-xs" style="color: ${l.color}">${l.layer}</span>
                  <span class="text-[10px] text-slate-400">${l.components}</span>
                </div>
                <p class="text-slate-300 text-[11px]">${l.description}</p>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Comparison Table -->
        <div>
          <h2 class="text-sm font-bold text-white mb-2">Architectural Comparison: Monolith vs. Headless</h2>
          <div class="grid grid-cols-2 gap-3 text-[11px]">
            <div class="p-3 bg-red-950/20 rounded border border-red-900/40 space-y-1.5">
              <div class="font-bold text-red-400">${guide.comparison.monolith.title}</div>
              <div class="flex justify-between"><span class="text-slate-400">Bundle Size:</span> <span class="text-red-300 font-bold">${guide.comparison.monolith.payloadSize}</span></div>
              <div class="flex justify-between"><span class="text-slate-400">Roundtrip Latency:</span> <span class="text-red-300 font-bold">${guide.comparison.monolith.loadTime}</span></div>
              <div class="flex justify-between"><span class="text-slate-400">Flexibility:</span> <span class="text-slate-300">${guide.comparison.monolith.flexibility}</span></div>
              <div class="flex justify-between"><span class="text-slate-400">Agent Readiness:</span> <span class="text-red-400">${guide.comparison.monolith.agentUsability}</span></div>
            </div>

            <div class="p-3 bg-emerald-950/20 rounded border border-emerald-900/40 space-y-1.5">
              <div class="font-bold text-emerald-400">${guide.comparison.headless.title}</div>
              <div class="flex justify-between"><span class="text-slate-400">Payload Size:</span> <span class="text-emerald-300 font-bold">${guide.comparison.headless.payloadSize}</span></div>
              <div class="flex justify-between"><span class="text-slate-400">API Response:</span> <span class="text-emerald-300 font-bold">${guide.comparison.headless.loadTime}</span></div>
              <div class="flex justify-between"><span class="text-slate-400">Flexibility:</span> <span class="text-slate-300">${guide.comparison.headless.flexibility}</span></div>
              <div class="flex justify-between"><span class="text-slate-400">Agent Readiness:</span> <span class="text-emerald-400 font-bold">${guide.comparison.headless.agentUsability}</span></div>
            </div>
          </div>
        </div>

        <!-- Sample Code -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="font-bold text-white text-xs">${guide.sampleCode.title}</span>
            <span class="text-[10px] text-emerald-400 uppercase">Single HTTP/2 Roundtrip</span>
          </div>
          <pre class="p-3 bg-slate-950 text-emerald-300 rounded border border-slate-800 overflow-x-auto text-[11px]"><code>${escapeHtml(guide.sampleCode.code)}</code></pre>
        </div>
      `;
    } else if (this.activeTopic === 'agentforce') {
      return `
        <!-- Summary -->
        <p class="text-sm text-slate-200">${guide.summary}</p>

        <!-- The Atlas Loop Steps -->
        <div>
          <h2 class="text-sm font-bold text-white mb-2">The Atlas Reasoning Engine Loop</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2.5">
            ${guide.atlasCycle.map(s => `
              <div class="p-3 bg-slate-950 rounded border border-purple-900/40 hover:border-purple-600 transition-colors">
                <div class="flex items-center gap-2 font-bold text-purple-300 mb-1">
                  <span>${s.icon}</span>
                  <span>${s.step}</span>
                </div>
                <p class="text-slate-400 text-[11px]">${s.description}</p>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Interactive Atlas Reasoning Simulator -->
        <div class="p-4 bg-purple-950/20 rounded border border-purple-800 space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="font-bold text-purple-300 text-sm">🧪 Interactive Atlas Loop Simulator</h3>
            <span class="text-[10px] bg-purple-900/60 px-2 py-0.5 rounded text-purple-200">Live Reasoning Playground</span>
          </div>
          <p class="text-slate-300 text-[11px]">Choose a customer scenario and watch Atlas process through intent, trust filtering, topic routing, context grounding, and invocable tool execution:</p>
          
          <div class="flex gap-2">
            <button id="sim-scenario-1" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded border border-slate-700 text-[11px] font-bold">
              Scenario A: Cold-Chain Waterlogging Crisis
            </button>
            <button id="sim-scenario-2" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded border border-slate-700 text-[11px] font-bold">
              Scenario B: VIP Churn Risk SLA
            </button>
          </div>

          <div id="atlas-sim-output" class="p-3 bg-slate-950 rounded border border-slate-800 min-h-[140px] text-[11px] font-mono space-y-1.5">
            <div class="text-slate-500">// Select a scenario above to run the Atlas perception loop...</div>
          </div>
        </div>

        <!-- Sample Code -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="font-bold text-white text-xs">${guide.sampleCode.title}</span>
            <span class="text-[10px] text-purple-400 uppercase">WITH USER_MODE</span>
          </div>
          <pre class="p-3 bg-slate-950 text-purple-300 rounded border border-slate-800 overflow-x-auto text-[11px]"><code>${escapeHtml(guide.sampleCode.code)}</code></pre>
        </div>
      `;
    } else if (this.activeTopic === 'claudeforce') {
      return `
        <!-- Summary -->
        <p class="text-sm text-slate-200">${guide.summary}</p>

        <!-- Core Powers -->
        <div>
          <h2 class="text-sm font-bold text-white mb-2">Claude 3.5 Sonnet: Enterprise Capabilities</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            ${guide.corePowers.map(p => `
              <div class="p-3 bg-slate-950 rounded border border-orange-900/40">
                <h3 class="text-orange-400 font-bold text-xs mb-1">⚡ ${p.title}</h3>
                <p class="text-slate-400 text-[11px]">${p.description}</p>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Multi-Modal Workflow Walkthrough -->
        <div class="p-4 bg-orange-950/20 rounded border border-orange-800 space-y-2">
          <h3 class="font-bold text-orange-300 text-sm">👁️ Multi-Modal Manifest Processing Workflow</h3>
          <div class="space-y-1.5">
            ${guide.workflowExample.map(w => `
              <div class="flex items-start gap-2 text-[11px]">
                <span class="text-orange-400 font-bold whitespace-nowrap">${w.step}:</span>
                <span class="text-slate-300">${w.text}</span>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Sample Code -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="font-bold text-white text-xs">${guide.sampleCode.title}</span>
            <span class="text-[10px] text-orange-400 uppercase">Sonnet 3.5 System Prompt</span>
          </div>
          <pre class="p-3 bg-slate-950 text-orange-300 rounded border border-slate-800 overflow-x-auto text-[11px]"><code>${escapeHtml(guide.sampleCode.code)}</code></pre>
        </div>
      `;
    } else if (this.activeTopic === 'mcpApis') {
      return `
        <!-- Summary -->
        <p class="text-sm text-slate-200">${guide.summary}</p>

        <!-- Dual Planes Comparison -->
        <div>
          <h2 class="text-sm font-bold text-white mb-2">The Dual-Plane Hosted MCP Architecture</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            ${guide.dualPlanes.map(p => `
              <div class="p-4 rounded border flex flex-col justify-between" style="border-color: ${p.color}55; background: ${p.color}11">
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-bold text-sm" style="color: ${p.color}">${p.plane}</span>
                    <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">${p.status}</span>
                  </div>
                  <div class="text-[11px] text-slate-400 font-mono mb-2">${p.endpoint}</div>
                  
                  <div class="mb-2">
                    <div class="text-[11px] font-bold text-slate-300 mb-1">Standardized Tools:</div>
                    <ul class="space-y-1 text-[11px] text-slate-400">
                      ${p.tools.map(t => `<li class="font-mono">• ${t}</li>`).join('')}
                    </ul>
                  </div>
                </div>

                <div class="mt-3 pt-2 border-t border-slate-800 text-[10px] text-slate-400">
                  <span class="font-bold text-slate-300">Security:</span> ${p.security}
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Complete Modern API Landscape -->
        <div>
          <h2 class="text-sm font-bold text-white mb-2">Salesforce Modern API Landscape</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
            ${guide.apiLandscape.map(api => `
              <div class="p-2.5 bg-slate-950 rounded border border-slate-800">
                <div class="font-bold text-pink-400 text-xs">${api.name}</div>
                <div class="text-[10px] text-slate-400 mb-1 uppercase font-bold">${api.type}</div>
                <p class="text-[11px] text-slate-300">${api.bestFor}</p>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Sample Code -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="font-bold text-white text-xs">${guide.sampleCode.title}</span>
            <span class="text-[10px] text-pink-400 uppercase">JSON-RPC 2.0</span>
          </div>
          <pre class="p-3 bg-slate-950 text-pink-300 rounded border border-slate-800 overflow-x-auto text-[11px]"><code>${escapeHtml(guide.sampleCode.code)}</code></pre>
        </div>
      `;
    } else {
      // Semantic Matrix
      return `
        <!-- Summary -->
        <p class="text-sm text-slate-200">${guide.summary}</p>

        <!-- 3 Tiers -->
        <div class="space-y-4">
          ${guide.tiers.map(t => `
            <div class="p-4 bg-slate-950 rounded border border-sky-900/40 space-y-1.5">
              <div class="flex items-center justify-between">
                <h3 class="text-sky-400 font-bold text-sm">${t.tier}</h3>
                <span class="text-[10px] px-2 py-0.5 rounded bg-sky-950 text-sky-300 border border-sky-800">${t.metaphor}</span>
              </div>
              <div class="text-[11px] text-slate-400"><span class="text-slate-300 font-bold">Technology:</span> ${t.technology}</div>
              <p class="text-slate-300 text-[11px]">${t.content}</p>
              <div class="text-[10px] text-emerald-400 font-bold pt-1">Audience: ${t.visibility}</div>
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
          <div class="text-purple-400 font-bold">▶ Ingesting Telemetry: Sensor DC-HYD-04 records 9.2°C Excursion (Shipment SH-88392)...</div>
          <div class="text-slate-300">🛡️ Einstein Trust Layer: Masking PII and checking harm score (0.001 - Pass).</div>
          <div class="text-slate-300">🎯 Topic Matched: <span class="text-yellow-400">ColdChain_Rescue</span> (Confidence 0.992)</div>
          <div class="text-slate-300">🌐 Data 360 Grounding: Dr. Meera Reddy (Consignee) linked to VIP Household graph UID-88291.</div>
          <div class="text-slate-300">⚡ Action Planned: Invocable <span class="text-emerald-400">INDRA_UnifiedContextService.executeRescue</span></div>
          <div class="text-emerald-400 font-bold">✓ P0 Case CASE-99120 inserted as user. Rescue drone dispatched to Banjara Hills!</div>
        `;
      };
    }

    if (simBtn2 && simOutput) {
      simBtn2.onclick = () => {
        sfx.simulationStep();
        simOutput.innerHTML = `
          <div class="text-purple-400 font-bold">▶ Ingesting Inbound Signal: Consignee inquiry on delayed linehaul...</div>
          <div class="text-slate-300">🛡️ Einstein Trust Layer: De-identifying phone number to synthetic token.</div>
          <div class="text-slate-300">🎯 Topic Matched: <span class="text-yellow-400">VIP_Intervention</span> (Confidence 0.988)</div>
          <div class="text-slate-300">🌐 Data 360 Calculated Insights: Care Risk Score = 88.4 (High Severity).</div>
          <div class="text-slate-300">⚡ Action Planned: Trigger Autolaunched Rescue Flow + Post to Slack Concierge.</div>
          <div class="text-emerald-400 font-bold">✓ Dedicated specialist Ananya Rao notified in Slack with pre-authorized waiver.</div>
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

print("ConceptModal.js written successfully!")
