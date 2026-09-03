import { sfx } from '../engine/SoundFx.js';

export const TOUR_STOPS = [
  {
    step: 1,
    title: 'The Relational Bedrock: Metadata Citadel',
    subtitle: 'Declarative Objects, Field-Level Security & Sharing Architecture',
    buildingId: 'b_standard_objects',
    districtId: 'metadata',
    narrative: 'Every Salesforce org begins here. Before writing a line of code or deploying an AI agent, declarative metadata defines the relational schema (Account, Contact, Custom SObjects), multi-tenant tenancy boundaries, Field-Level Security (FLS), and Organization-Wide Defaults (OWD). This layer guarantees deterministic data integrity and row-level enterprise authorization.',
    keyTakeaway: 'Metadata is not just a schema—it is the immutable security boundary of the enterprise.'
  },
  {
    step: 2,
    title: 'The Execution Grid: Logic & Event Automation',
    subtitle: 'Apex Runtime WITH USER_MODE, Record Flows & Kafka Platform Events',
    buildingId: 'b_apex_foundry',
    districtId: 'automation',
    narrative: 'When state changes occur, the Logic Grid takes command. Apex code executes with strict Governor Limits to prevent CPU/heap hogging, enforced WITH USER_MODE for compile-time permission verification. Asynchronous Kafka Platform Events decouple heavy processing, allowing sub-second real-time reaction across external fleets without blocking end users.',
    keyTakeaway: 'Deterministic transactional logic ensures automated guarantees at multi-tenant scale.'
  },
  {
    step: 3,
    title: 'The Semantic Harbor: Data Cloud & Context Lake',
    subtitle: 'Data Lake Ingestion (DLOs), DMO Harmonization & Golden Identity Graph',
    buildingId: 'b_data_lake',
    districtId: 'semantic',
    narrative: 'Relational databases only see fragmented transactions. The Semantic Harbor ingests millions of unstructured telemetry events and legacy silos into Data Lake Objects (DLOs), mapping them to Cloud Information Model (CIM) DMOs. Probabilistic Identity Resolution unifies disparate touchpoints into a single Golden Record, while Calculated Insights continuously derive real-time risk scores.',
    keyTakeaway: 'The Semantic Layer provides the unified meaning and context graph that grounds AI reasoning.'
  },
  {
    step: 4,
    title: 'The Decoupled Skyport: Headless 360',
    subtitle: 'The API is the UI. Decoupled HXL, GraphQL & Composite Graphs',
    buildingId: 'b_headless_gateway',
    districtId: 'headless',
    narrative: 'Traditional browser Lightning Experience (LEX) renders heavy 14.8MB DOM trees meant for human clicks. Headless 360 collapses this into pure, composable APIs: a single GraphQL HTTP/2 call returns 2.1KB of typed payload in 42ms. The Headless Experience Layer (HXL) projects CRM directly into Slack, mobile handhelds, and external agent runtimes.',
    keyTakeaway: 'Eliminate browser bloat: agents and automated workers consume pure headless APIs.'
  },
  {
    step: 5,
    title: 'The Cognitive Spire: Agentforce & Atlas Engine',
    subtitle: 'Autonomous Perception, Grounding, Topic Routing & Invocable Execution',
    buildingId: 'b_agentforce_core',
    districtId: 'agentforce',
    narrative: 'Agentforce is not a chatbot—it is an autonomous reasoning engine (Atlas) operating in a closed perception-planning-action-evaluation loop. When an operational signal arrives, Atlas masks PII through the Einstein Trust Layer, routes to a locked business topic, grounds in Data Cloud context, synthesizes an execution plan, and executes Invocable Apex tools.',
    keyTakeaway: 'Atlas replaces rigid if-then trees with dynamic, governed autonomous reasoning.'
  },
  {
    step: 6,
    title: 'Frontier Co-Architect: Claudeforce Intelligence',
    subtitle: 'Anthropic Claude 3.5 Sonnet: 200k Context & Multimodal Vision Ingestion',
    buildingId: 'b_claudeforce_lab',
    districtId: 'claudeforce',
    narrative: 'Anthropic Claude 3.5 Sonnet acts as the frontier cognitive partner. With its massive 200,000 token context window, Claude can ingest entire enterprise metadata catalogs, ERDs, and Apex classes simultaneously to audit architecture and synthesize governor-compliant code. Multimodal vision parses complex physical bills of lading and clinical charts directly into SObjects.',
    keyTakeaway: 'Frontier models bring deep multi-modal reasoning and whole-org architectural comprehension.'
  },
  {
    step: 7,
    title: 'The Connective Fabric: Dual-Plane Hosted MCP',
    subtitle: 'Model Context Protocol: Plane 1 (Context) vs Plane 2 (Action)',
    buildingId: 'b_mcp_context',
    districtId: 'mcp',
    narrative: 'Salesforce exposes its enterprise capabilities to AI agents via Anthropic’s Model Context Protocol across two strictly decoupled planes: Plane 1 (data360) is the System of Context (read-only queries), while Plane 2 (headless-360) is the System of Action (governed state mutations). Separating Context and Action is an enterprise security imperative to prevent privilege escalation.',
    keyTakeaway: 'Dual-plane isolation guarantees least privilege while empowering autonomous agentic workflows.'
  }
];

export class GuidedTour {
  constructor(container, isoCanvas, onOpenConcept) {
    this.container = container;
    this.isoCanvas = isoCanvas;
    this.onOpenConcept = onOpenConcept;
    this.currentIndex = 0;
    this.isActive = false;
  }

  start(stepIndex = 0) {
    this.isActive = true;
    this.currentIndex = stepIndex;
    this.container.classList.remove('hidden');
    this.goToStop(this.currentIndex);
    sfx.openModal();
  }

  stop() {
    this.isActive = false;
    this.container.classList.add('hidden');
    this.isoCanvas.activeFilter = 'all';
    this.isoCanvas.centerCamera();
    sfx.closeModal();
  }

  next() {
    if (this.currentIndex < TOUR_STOPS.length - 1) {
      this.goToStop(this.currentIndex + 1);
    } else {
      this.stop();
    }
  }

  prev() {
    if (this.currentIndex > 0) {
      this.goToStop(this.currentIndex - 1);
    }
  }

  goToStop(index) {
    this.currentIndex = index;
    const stop = TOUR_STOPS[this.currentIndex];

    // Filter canvas and focus building
    this.isoCanvas.activeFilter = stop.districtId;
    this.isoCanvas.focusBuilding(stop.buildingId);
    sfx.simulationStep();

    this.render();
  }

  render() {
    const stop = TOUR_STOPS[this.currentIndex];
    const total = TOUR_STOPS.length;

    this.container.innerHTML = `
      <div style="position: absolute; bottom: 76px; left: 50%; transform: translateX(-50%); z-index: 45; width: 92%; max-width: 720px; background: rgba(9, 14, 26, 0.96); backdrop-filter: blur(28px); border: 1px solid rgba(0, 240, 255, 0.4); border-radius: 12px; box-shadow: 0 24px 60px rgba(0, 0, 0, 0.85), 0 0 35px rgba(0, 240, 255, 0.2); overflow: hidden; animation: tour-slide-up 0.25s cubic-bezier(0.16, 1, 0.3, 1);">
        
        <!-- Header Bar -->
        <div style="padding: 12px 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: rgba(5, 8, 16, 0.7); display: flex; align-items: center; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span class="datum-tag" style="border-color: #00f0ff; color: #00f0ff;">
              CHAPTER ${stop.step} OF ${total}
            </span>
            <span style="font-size: 11px; color: #94a3b8; font-family: 'JetBrains Mono', monospace;">ARCHITECTURAL TOUR</span>
          </div>
          <button id="btn-exit-tour" class="action-btn-ghost" style="padding: 3px 8px; font-size: 11.5px;">
            ✕ Exit Tour
          </button>
        </div>

        <!-- Narrative Body -->
        <div style="padding: 18px 22px; display: flex; flex-direction: column; gap: 10px;">
          <div>
            <h2 style="margin: 0 0 4px; font-size: 15px; font-weight: 700; color: #ffffff;">${stop.title}</h2>
            <div style="font-size: 11.5px; color: #38bdf8; font-family: 'JetBrains Mono', monospace;">${stop.subtitle}</div>
          </div>

          <p style="margin: 0; color: #cbd5e1; font-size: 12.5px; line-height: 1.6;">${stop.narrative}</p>

          <div style="padding: 10px 14px; border-radius: 8px; background: rgba(0, 240, 255, 0.06); border-left: 3px solid #00f0ff; font-size: 11.5px; color: #f1f5f9;">
            <strong style="color: #00f0ff;">Architectural Key:</strong> ${stop.keyTakeaway}
          </div>
        </div>

        <!-- Progress Dots & Controls -->
        <div style="padding: 12px 20px; border-top: 1px solid rgba(255, 255, 255, 0.08); background: rgba(5, 8, 16, 0.85); display: flex; align-items: center; justify-content: space-between;">
          <!-- Progress Dots -->
          <div style="display: flex; align-items: center; gap: 6px;">
            ${TOUR_STOPS.map((s, idx) => `
              <div style="width: ${idx === this.currentIndex ? '20px' : '6px'}; height: 6px; border-radius: 3px; background: ${idx === this.currentIndex ? '#00f0ff' : 'rgba(255, 255, 255, 0.2)'}; transition: all 0.2s;"></div>
            `).join('')}
          </div>

          <!-- Buttons -->
          <div style="display: flex; align-items: center; gap: 8px;">
            <button id="btn-tour-prev" class="action-btn-ghost" style="padding: 6px 12px; font-size: 11.5px;" ${this.currentIndex === 0 ? 'disabled style="opacity: 0.3;"' : ''}>
              ← Previous
            </button>
            <button id="btn-tour-next" class="action-btn-primary" style="padding: 6px 16px; font-size: 11.5px;">
              ${this.currentIndex === total - 1 ? 'Finish Tour ✓' : 'Next Chapter →'}
            </button>
          </div>
        </div>

      </div>
    `;

    this.container.querySelector('#btn-exit-tour').onclick = () => this.stop();
    this.container.querySelector('#btn-tour-prev').onclick = () => this.prev();
    this.container.querySelector('#btn-tour-next').onclick = () => this.next();
  }
}
