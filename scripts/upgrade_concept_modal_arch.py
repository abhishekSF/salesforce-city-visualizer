modal_code = '''import { CONCEPT_GUIDES } from '../data/conceptGuides.js';
import { sfx } from '../engine/SoundFx.js';

export class ConceptModal {
  constructor(container) {
    this.container = container;
    this.activeTopic = 'headless360';
    this.activeMcpPlane = 'plane1';
    this.rescueSimStep = 0;
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
          
          <!-- Top Architectural Title Bar -->
          <div style="padding: 16px 24px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: rgba(8, 12, 22, 0.95); display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 14px;">
              <div style="width: 38px; height: 38px; border-radius: 8px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.15); display: flex; align-items: center; justify-content: center; font-size: 20px;">
                ${guide.icon}
              </div>
              <div>
                <div style="display: flex; align-items: center; gap: 10px;">
                  <h1 style="margin: 0; font-size: 16px; font-weight: 700; color: #ffffff; letter-spacing: -0.01em;">${guide.title}</h1>
                  <span class="datum-tag">ARCH-SPEC 2026</span>
                </div>
                <p style="margin: 2px 0 0; font-size: 12px; color: #94a3b8; font-family: 'JetBrains Mono', monospace;">${guide.subtitle}</p>
              </div>
            </div>
            <button id="btn-close-modal" class="action-btn-ghost" style="padding: 6px 12px;">
              ✕ Close Studio
            </button>
          </div>

          <!-- Studio Navigation Tabs -->
          <div style="display: flex; gap: 4px; padding: 10px 24px; background: rgba(5, 8, 16, 0.7); border-bottom: 1px solid rgba(255, 255, 255, 0.06); overflow-x: auto;">
            <button data-topic="headless360" class="tab-btn program-btn ${this.activeTopic === 'headless360' ? 'active' : ''}">
              🚀 Headless 360 Architecture
            </button>
            <button data-topic="agentforce" class="tab-btn program-btn ${this.activeTopic === 'agentforce' ? 'active' : ''}">
              🤖 Agentforce Atlas Engine
            </button>
            <button data-topic="claudeforce" class="tab-btn program-btn ${this.activeTopic === 'claudeforce' ? 'active' : ''}">
              🧠 Claudeforce Intelligence
            </button>
            <button data-topic="mcpApis" class="tab-btn program-btn ${this.activeTopic === 'mcpApis' ? 'active' : ''}">
              🔌 Dual-Plane MCPs & APIs
            </button>
            <button data-topic="semanticMatrix" class="tab-btn program-btn ${this.activeTopic === 'semanticMatrix' ? 'active' : ''}">
              🏢 Semantic Layer Matrix
            </button>
          </div>

          <!-- Studio Main Viewport -->
          <div style="flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 24px; font-size: 13px; line-height: 1.6; color: #cbd5e1;">
            <!-- Architectural Thesis Banner -->
            <div style="padding: 14px 20px; border-radius: 8px; background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2); display: flex; align-items: center; justify-content: space-between;">
              <span style="color: #38bdf8; font-weight: 600; font-family: 'JetBrains Mono', monospace; font-size: 12.5px;">${guide.tagline}</span>
              <span class="datum-tag" style="border-color: rgba(0, 240, 255, 0.4); color: #00f0ff;">SYSTEM DESIGN</span>
            </div>

            <!-- Topic Body & Deep-Dive Interactive Lab -->
            ${this.renderTopicBody(guide)}
          </div>

          <!-- Footer Bar -->
          <div style="padding: 12px 24px; border-top: 1px solid rgba(255, 255, 255, 0.08); background: rgba(8, 12, 22, 0.95); display: flex; align-items: center; justify-content: space-between; font-size: 11.5px; color: #64748b; font-family: 'JetBrains Mono', monospace;">
            <span>SALESFORCE ORG AXONOMETRIC MASTERPLAN // ENTERPRISE REFERENCE ARCHITECTURE</span>
            <button id="btn-close-modal-footer" class="action-btn-primary" style="padding: 6px 14px; font-size: 11.5px;">
              Return to Masterplan
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
        <!-- Thesis & Core Architecture -->
        <div>
          <h2 style="font-size: 15px; font-weight: 700; color: #ffffff; margin: 0 0 8px;">The Architectural Shift: Why Browser CRM (LEX) Fails AI Agents</h2>
          <p style="margin: 0; color: #94a3b8; font-size: 13px;">
            Traditional Salesforce Lightning Experience (LEX) was built for human eyes rendering bloated DOM trees on desktop browsers. Autonomous AI agents and high-throughput microservices cannot and should not drive brittle browser DOMs. Headless 360 decouples the <strong>System of Context</strong> (Data Cloud) and <strong>System of Action</strong> (Apex, Flows) into pure, typed, composable APIs.
          </p>
        </div>

        <!-- 4 Layers of Headless 360 Architecture Section -->
        <div>
          <h3 style="font-size: 13px; font-weight: 700; color: #ffffff; margin: 0 0 12px; text-transform: uppercase; letter-spacing: 0.04em;">The 4-Layer Headless Architectural Section</h3>
          <div style="display: flex; flex-direction: column; gap: 8px;">
            ${guide.fourLayers.map((l, idx) => `
              <div class="arch-card" style="border-left: 4px solid ${l.color}; padding: 14px 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                  <span style="font-weight: 700; color: ${l.color}; font-size: 13px;">${l.layer}</span>
                  <span style="font-size: 11px; color: #94a3b8; font-family: 'JetBrains Mono', monospace;">${l.components}</span>
                </div>
                <div style="color: #cbd5e1; font-size: 12px;">${l.description}</div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Network Waterfall Profiler (Interactive) -->
        <div>
          <h3 style="font-size: 13px; font-weight: 700; color: #ffffff; margin: 0 0 10px; text-transform: uppercase; letter-spacing: 0.04em;">Network Latency & Payload Benchmark</h3>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
            <div class="arch-card" style="border-color: rgba(255, 69, 58, 0.3); background: rgba(255, 69, 58, 0.04);">
              <div style="font-weight: 700; color: #ff453a; font-size: 13px; margin-bottom: 8px;">Traditional Monolithic LEX Browser Session</div>
              <div style="display: flex; flex-direction: column; gap: 6px; font-size: 12px;">
                <div style="display: flex; justify-content: space-between;"><span style="color: #94a3b8;">Asset Transfer Size:</span> <span style="color: #ff453a; font-weight: 700; font-family: 'JetBrains Mono', monospace;">14.8 MB (Aura/LWC)</span></div>
                <div style="display: flex; justify-content: space-between;"><span style="color: #94a3b8;">HTTP Roundtrips:</span> <span style="color: #ff453a; font-weight: 700; font-family: 'JetBrains Mono', monospace;">142 Requests</span></div>
                <div style="display: flex; justify-content: space-between;"><span style="color: #94a3b8;">DOM Ready Time:</span> <span style="color: #ff453a; font-weight: 700; font-family: 'JetBrains Mono', monospace;">3,240 ms</span></div>
                <div style="display: flex; justify-content: space-between;"><span style="color: #94a3b8;">Agent Interface:</span> <span style="color: #94a3b8;">Brittle DOM Scrapers (Fails often)</span></div>
              </div>
            </div>

            <div class="arch-card" style="border-color: rgba(16, 185, 129, 0.35); background: rgba(16, 185, 129, 0.04);">
              <div style="font-weight: 700; color: #10b981; font-size: 13px; margin-bottom: 8px;">Headless 360 Composable Architecture</div>
              <div style="display: flex; flex-direction: column; gap: 6px; font-size: 12px;">
                <div style="display: flex; justify-content: space-between;"><span style="color: #94a3b8;">Payload Transfer Size:</span> <span style="color: #10b981; font-weight: 700; font-family: 'JetBrains Mono', monospace;">2.1 KB (GraphQL JSON)</span></div>
                <div style="display: flex; justify-content: space-between;"><span style="color: #94a3b8;">HTTP Roundtrips:</span> <span style="color: #10b981; font-weight: 700; font-family: 'JetBrains Mono', monospace;">1 Single HTTP/2 Call</span></div>
                <div style="display: flex; justify-content: space-between;"><span style="color: #94a3b8;">State Execution Time:</span> <span style="color: #10b981; font-weight: 700; font-family: 'JetBrains Mono', monospace;">42 ms</span></div>
                <div style="display: flex; justify-content: space-between;"><span style="color: #94a3b8;">Agent Interface:</span> <span style="color: #10b981; font-weight: 700;">Native Typed Model Context Protocol</span></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Live Headless GraphQL Workbench -->
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; color: #ffffff; font-size: 13px;">Live Headless GraphQL API Query</span>
            <span class="datum-tag" style="color: #10b981;">ENDPOINT: /services/data/v66.0/graphql</span>
          </div>
          <pre><code>${escapeHtml(guide.sampleCode.code)}</code></pre>
        </div>
      `;
    } else if (this.activeTopic === 'agentforce') {
      return `
        <!-- Autonomous Atlas Thesis -->
        <div>
          <h2 style="font-size: 15px; font-weight: 700; color: #ffffff; margin: 0 0 8px;">Autonomous Reasoning vs. Deterministic Scripting</h2>
          <p style="margin: 0; color: #94a3b8; font-size: 13px;">
            Agentforce is not a chatbot. It is Salesforce's autonomous agent framework governed by the <strong>Atlas Reasoning Engine</strong>. Unlike rigid if-then decision trees, Atlas runs a closed-loop architectural cycle: perceiving intent, screening through the Einstein Trust Layer, routing to scoped enterprise topics, grounding in Data Cloud's semantic graph, and planning deterministic invocable tool calls.
          </p>
        </div>

        <!-- 6-Stage Atlas State Machine -->
        <div>
          <h3 style="font-size: 13px; font-weight: 700; color: #ffffff; margin: 0 0 10px; text-transform: uppercase; letter-spacing: 0.04em;">The Atlas Reasoning State Machine</h3>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px;">
            ${guide.atlasCycle.map(s => `
              <div class="arch-card" style="border-color: rgba(168, 85, 247, 0.25);">
                <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; color: #c084fc; font-size: 12.5px; margin-bottom: 4px;">
                  <span>${s.icon}</span>
                  <span>${s.step}</span>
                </div>
                <div style="color: #94a3b8; font-size: 11.5px;">${s.description}</div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Interactive Simulation Workbench -->
        <div class="arch-card" style="border-color: rgba(168, 85, 247, 0.4); display: flex; flex-direction: column; gap: 14px;">
          <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
              <h3 style="margin: 0; font-size: 14px; font-weight: 700; color: #d8b4fe;">🧪 Interactive Atlas Reasoning Simulation Workbench</h3>
              <p style="margin: 2px 0 0; color: #94a3b8; font-size: 11.5px;">Select an operational scenario to step through the perception-reasoning-action state machine:</p>
            </div>
            <span class="datum-tag" style="border-color: #a855f7; color: #c084fc;">STATE TRANSITION SIMULATOR</span>
          </div>

          <div style="display: flex; gap: 10px;">
            <button id="sim-scenario-1" class="action-btn-primary" style="font-size: 12px; padding: 8px 14px;">
              Scenario A: Cold-Chain Telemetry Excursion (P0)
            </button>
            <button id="sim-scenario-2" class="action-btn-primary" style="font-size: 12px; padding: 8px 14px;">
              Scenario B: VIP Consignee Flood Infiltration
            </button>
          </div>

          <div id="atlas-sim-output" style="padding: 16px; background: #050811; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 11.5px; min-height: 150px; display: flex; flex-direction: column; gap: 8px;">
            <div style="color: #64748b;">// Select a scenario button above to initiate the Atlas perception loop...</div>
          </div>
        </div>

        <!-- Invocable Apex Action -->
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; color: #ffffff; font-size: 13px;">Invocable Apex Tool Contract (WITH USER_MODE)</span>
            <span class="datum-tag" style="color: #c084fc;">CATEGORY: AGENTFORCE</span>
          </div>
          <pre><code>${escapeHtml(guide.sampleCode.code)}</code></pre>
        </div>
      `;
    } else if (this.activeTopic === 'claudeforce') {
      return `
        <!-- Claudeforce Architectural Thesis -->
        <div>
          <h2 style="font-size: 15px; font-weight: 700; color: #ffffff; margin: 0 0 8px;">Claude 3.5 Sonnet: The Frontier Cognitive Co-Architect</h2>
          <p style="margin: 0; color: #94a3b8; font-size: 13px;">
            Claudeforce embodies the deep integration of Anthropic Claude 3.5 Sonnet into the Salesforce architectural fabric. With a <strong>200,000 token context window</strong>, Claude can ingest entire enterprise metadata catalogs, complex multi-object ERDs, and 50+ Apex classes in a single prompt to audit architecture, synthesize governor-limit compliant Apex (<code>WITH USER_MODE</code>), and parse messy physical paperwork via multi-modal vision.
          </p>
        </div>

        <!-- Core Architectural Pillars -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px;">
          ${guide.corePowers.map(p => `
            <div class="arch-card" style="border-color: rgba(249, 115, 22, 0.25);">
              <div style="font-weight: 700; color: #fb923c; font-size: 13px; margin-bottom: 4px;">⚡ ${p.title}</div>
              <div style="color: #94a3b8; font-size: 11.5px;">${p.description}</div>
            </div>
          `).join('')}
        </div>

        <!-- Multi-Modal Ingestion Pipeline Walkthrough -->
        <div class="arch-card" style="border-color: rgba(249, 115, 22, 0.4); display: flex; flex-direction: column; gap: 10px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="margin: 0; font-size: 14px; font-weight: 700; color: #fdba74;">👁️ Multi-Modal Bill of Lading (BOL) Extraction Pipeline</h3>
            <span class="datum-tag" style="border-color: #f97316; color: #fb923c;">VISION TO SOQL/DML</span>
          </div>
          ${guide.workflowExample.map(w => `
            <div style="display: flex; gap: 12px; font-size: 12px;">
              <span style="color: #fb923c; font-weight: 700; font-family: 'JetBrains Mono', monospace; white-space: nowrap;">${w.step}:</span>
              <span style="color: #cbd5e1;">${w.text}</span>
            </div>
          `).join('')}
        </div>

        <!-- System Prompt Code -->
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; color: #ffffff; font-size: 13px;">Claudeforce System Prompt & Architectural Guardrails</span>
            <span class="datum-tag" style="color: #fb923c;">ANTHROPIC SDK V1</span>
          </div>
          <pre><code>${escapeHtml(guide.sampleCode.code)}</code></pre>
        </div>
      `;
    } else if (this.activeTopic === 'mcpApis') {
      return `
        <!-- Dual Plane Thesis -->
        <div>
          <h2 style="font-size: 15px; font-weight: 700; color: #ffffff; margin: 0 0 8px;">The Dual-Plane Hosted Model Context Protocol (MCP) Architecture</h2>
          <p style="margin: 0; color: #94a3b8; font-size: 13px;">
            Salesforce implements the Model Context Protocol (MCP) across two strictly separated hosted planes. <strong>Collapsing the two planes is an architectural anti-pattern</strong>: Plane 1 acts as the System of Context (reading and searching the data lake and unified graph), while Plane 2 acts as the System of Action (executing governed state mutations under strict user mode security).
          </p>
        </div>

        <!-- Dual Planes Architectural Comparison Matrix -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
          ${guide.dualPlanes.map(p => `
            <div style="padding: 18px; border-radius: 12px; border: 1px solid ${p.color}55; background: ${p.color}08; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                  <span style="font-weight: 700; font-size: 14px; color: ${p.color};">${p.plane}</span>
                  <span class="datum-tag" style="color: #ffffff;">${p.status}</span>
                </div>
                <div style="font-size: 11px; color: #94a3b8; font-family: 'JetBrains Mono', monospace; margin-bottom: 12px;">${p.endpoint}</div>

                <div style="margin-bottom: 14px;">
                  <div style="font-size: 11px; font-weight: 700; color: #ffffff; margin-bottom: 6px; text-transform: uppercase;">Standardized Tools Interface:</div>
                  <ul style="margin: 0; padding-left: 18px; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #cbd5e1; display: flex; flex-direction: column; gap: 4px;">
                    ${p.tools.map(t => `<li>${t}</li>`).join('')}
                  </ul>
                </div>
              </div>

              <div style="padding-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.08); font-size: 11.5px; color: #94a3b8;">
                <strong style="color: #ffffff;">Trust Boundary:</strong> ${p.security}
              </div>
            </div>
          `).join('')}
        </div>

        <!-- Live MCP Terminal Emulator -->
        <div class="arch-card" style="border-color: rgba(236, 72, 153, 0.4); display: flex; flex-direction: column; gap: 12px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="margin: 0; font-size: 14px; font-weight: 700; color: #f472b6;">⚡ Live Model Context Protocol (MCP) Client Inspector</h3>
            <span class="datum-tag" style="border-color: #ec4899; color: #f472b6;">JSON-RPC 2.0 PROTOCOL</span>
          </div>
          
          <div style="display: flex; gap: 10px;">
            <button id="btn-mcp-plane1" class="action-btn-primary" style="font-size: 11.5px; padding: 7px 12px;">
              Query Plane 1 (Data 360 Context)
            </button>
            <button id="btn-mcp-plane2" class="action-btn-primary" style="font-size: 11.5px; padding: 7px 12px;">
              Dispatch Plane 2 (Headless 360 Action)
            </button>
          </div>

          <div id="mcp-terminal-output" style="padding: 14px; background: #050811; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 11.5px; min-height: 140px; display: flex; flex-direction: column; gap: 6px;">
            <div style="color: #64748b;">// Click an MCP plane query button above to inspect live JSON-RPC frames...</div>
          </div>
        </div>

        <!-- Modern API Landscape -->
        <div>
          <h3 style="font-size: 13px; font-weight: 700; color: #ffffff; margin: 0 0 10px; text-transform: uppercase; letter-spacing: 0.04em;">Salesforce Modern API Architecture</h3>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
            ${guide.apiLandscape.map(api => `
              <div class="arch-card" style="padding: 12px;">
                <div style="font-weight: 700; color: #f472b6; font-size: 12px;">${api.name}</div>
                <div style="font-size: 10px; color: #94a3b8; font-weight: 600; text-transform: uppercase; margin-bottom: 4px;">${api.type}</div>
                <div style="font-size: 11.5px; color: #cbd5e1;">${api.bestFor}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    } else {
      return `
        <!-- Semantic Layer Matrix -->
        <div>
          <h2 style="font-size: 15px; font-weight: 700; color: #ffffff; margin: 0 0 8px;">The Three Evolutionary Tiers of Salesforce Architecture</h2>
          <p style="margin: 0; color: #94a3b8; font-size: 13px;">
            To understand Salesforce as an architectural masterplan, one must distinguish between the <strong>physical relational tables</strong> (storage), the <strong>declarative metadata layer</strong> (schema, relationships, security), and the <strong>semantic layer</strong> (ontologies, identity graphs, and calculated insights that ground AI).
          </p>
        </div>

        <div style="display: flex; flex-direction: column; gap: 14px;">
          ${guide.tiers.map(t => `
            <div class="arch-card" style="border-left: 4px solid #38bdf8; padding: 18px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-weight: 700; font-size: 14px; color: #38bdf8;">${t.tier}</span>
                <span class="datum-tag">${t.metaphor}</span>
              </div>
              <div style="font-size: 12px; color: #94a3b8; margin-bottom: 6px; font-family: 'JetBrains Mono', monospace;"><strong style="color: #ffffff;">Underlying Engine:</strong> ${t.technology}</div>
              <div style="font-size: 12.5px; color: #cbd5e1; margin-bottom: 8px;">${t.content}</div>
              <div style="font-size: 11.5px; color: #34d399; font-weight: 600;">Audience & Surface: ${t.visibility}</div>
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
          <div style="color: #c084fc; font-weight: 700;">[STAGE 1: PERCEPTION] Inbound Telemetry: Sensor DC-HYD-04 records 9.2°C Excursion (Shipment SH-88392)</div>
          <div style="color: #94a3b8;">[STAGE 2: TRUST LAYER] De-identifying patient PII -> Synthetic token. Checking toxicity score (0.001 - PASS).</div>
          <div style="color: #facc15; font-weight: 700;">[STAGE 3: TOPIC ROUTING] Matched Topic: "ColdChain_Rescue" (Confidence: 0.992)</div>
          <div style="color: #38bdf8;">[STAGE 4: SEMANTIC GROUNDING] Data 360 Golden Record queried -> Linked to Dr. Meera Reddy (VIP Household UID-88291).</div>
          <div style="color: #10b981; font-weight: 700;">[STAGE 5: ACTION DISPATCH] Invoking Invocable Apex: INDRA_UnifiedContextService.executeRescue()</div>
          <div style="color: #34d399; font-weight: 700;">[STAGE 6: AUDIT & OUTPUT] P0 Care Case CASE-99120 inserted AS USER. Drone flight rerouted to Banjara Hills. Audit logged to BigObject.</div>
        `;
      };
    }

    if (simBtn2 && simOutput) {
      simBtn2.onclick = () => {
        sfx.simulationStep();
        simOutput.innerHTML = `
          <div style="color: #c084fc; font-weight: 700;">[STAGE 1: PERCEPTION] Inbound Signal: Waterlogging exception in Jubilee Hills grid transit zone.</div>
          <div style="color: #94a3b8;">[STAGE 2: TRUST LAYER] Evaluating harm and enterprise SLA compliance bounds.</div>
          <div style="color: #facc15; font-weight: 700;">[STAGE 3: TOPIC ROUTING] Matched Topic: "Monsoon_Flood_Reroute" (Confidence: 0.985)</div>
          <div style="color: #38bdf8;">[STAGE 4: SEMANTIC GROUNDING] Calculated Insights: Depot Stress Index = 94.2 kW. SOP Vector retrieved.</div>
          <div style="color: #10b981; font-weight: 700;">[STAGE 5: ACTION DISPATCH] Firing Autolaunched Flow + Headless Slack Block Kit message.</div>
          <div style="color: #34d399; font-weight: 700;">[STAGE 6: AUDIT & OUTPUT] Operations Concierge Ananya Rao notified in Slack with 1-click rescue authorization.</div>
        `;
      };
    }

    const mcpBtn1 = this.container.querySelector('#btn-mcp-plane1');
    const mcpBtn2 = this.container.querySelector('#btn-mcp-plane2');
    const mcpOutput = this.container.querySelector('#mcp-terminal-output');

    if (mcpBtn1 && mcpOutput) {
      mcpBtn1.onclick = () => {
        sfx.simulationStep();
        mcpOutput.innerHTML = `
          <div style="color: #06b6d4;">--> JSON-RPC POST /platform/mcp/v1/data/data360</div>
          <div style="color: #94a3b8;">{"jsonrpc":"2.0","method":"tools/call","params":{"name":"data360_search","arguments":{"query":"UnifiedIndividual__dlm WHERE CareRisk__c > 80"}},"id":"req-01"}</div>
          <div style="color: #38bdf8;"><-- HTTP/2 200 OK (18ms)</div>
          <div style="color: #6ee7b7;">{"jsonrpc":"2.0","result":{"matched_nodes":1,"golden_record":{"uid":"UID-88291","name":"Dr. Meera Reddy","risk_score":88.4}},"id":"req-01"}</div>
        `;
      };
    }

    if (mcpBtn2 && mcpOutput) {
      mcpBtn2.onclick = () => {
        sfx.simulationStep();
        mcpOutput.innerHTML = `
          <div style="color: #ec4899;">--> JSON-RPC POST /platform/mcp/v1/platform/headless-360</div>
          <div style="color: #94a3b8;">{"jsonrpc":"2.0","method":"tools/call","params":{"name":"headless360_dispatch","arguments":{"action":"create_case","fields":{"Subject":"Cold-Chain Excursion Rescue","Priority":"P0"}}},"id":"req-02"}</div>
          <div style="color: #f472b6;"><-- HTTP/2 200 OK (24ms) [Enforcing FLS & WITH USER_MODE]</div>
          <div style="color: #34d399; font-weight: 700;">{"jsonrpc":"2.0","result":{"status":"SUCCESS","recordId":"5008800000XyZ1A","audit_logged":true},"id":"req-02"}</div>
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

print("Architectural ConceptModal.js written successfully!")
