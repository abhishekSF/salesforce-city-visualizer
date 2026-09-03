import { sfx } from '../engine/SoundFx.js';

export const RESCUE_STAGES = [
  {
    step: 1,
    title: 'Stage 1: IoT Telemetry Ingestion',
    action: 'Sensor Telemetry Ingestion (IoT)',
    buildingId: 'b_data_lake',
    targetBuildingId: 'b_data_refinery',
    conduitColor: '#06b6d4',
    detail: 'Cold-chain IoT sensor DC-HYD-04 records 9.2°C excursion (Threshold: 8.0°C) for biologic consignment SH-88392 in transit corridor Jubilee Hills.',
    payload: {
      source: "INDRA_IoT_Gateway",
      timestamp: "2026-09-03T11:25:00Z",
      device_id: "DC-HYD-04",
      shipment_id: "SH-88392",
      metric: "internal_temp_celsius",
      value: 9.2,
      threshold: 8.0,
      excursion_severity: "CRITICAL",
      telemetry_payload_dlo: "IoT_Telemetry_Stream__dlo"
    }
  },
  {
    step: 2,
    title: 'Stage 2: Semantic Identity Resolution',
    action: 'Identity Resolution & Golden Record Linkage',
    buildingId: 'b_data_refinery',
    targetBuildingId: 'b_platform_events',
    conduitColor: '#06b6d4',
    detail: 'Data Cloud maps raw DLO into UnifiedIndividual__dlm via deterministic email and phone rule. Consignee identified as Dr. Meera Reddy (VIP Patient Household UID-88291).',
    payload: {
      data_cloud_dmo: "UnifiedIndividual__dlm",
      golden_record_id: "UID-88291",
      individual: {
        name: "Dr. Meera Reddy",
        phone_hash: "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        household_tier: "VIP_CRITICAL_CARE",
        lifetime_care_score: 94.8
      },
      calculated_insights: {
        care_risk_score: 88.4,
        sla_violation_probability: 0.942
      }
    }
  },
  {
    step: 3,
    title: 'Stage 3: Kafka Event Bus Broadcast',
    action: 'Platform Event Broadcast',
    buildingId: 'b_platform_events',
    targetBuildingId: 'b_agentforce_core',
    conduitColor: '#f59e0b',
    detail: 'INDRA_Care_Signal__e published to Salesforce asynchronous event bus with High Volume Kafka streaming. Atlas Reasoning Engine consumes event in 18ms.',
    payload: {
      event_type: "INDRA_Care_Signal__e",
      replay_id: 8829104,
      payload: {
        Consignment_Number__c: "SH-88392",
        Excursion_Delta__c: 1.2,
        Risk_Level__c: "P0",
        Unified_Customer_Id__c: "UID-88291"
      },
      headers: {
        schema_fingerprint: "apex:PlatformEvent:INDRA_Care_Signal:v1",
        created_date: "2026-09-03T11:25:01Z"
      }
    }
  },
  {
    step: 4,
    title: 'Stage 4: Agentforce Atlas Reasoning Loop',
    action: 'Autonomous Atlas Reasoning & Grounding',
    buildingId: 'b_agentforce_core',
    targetBuildingId: 'b_mcp_action',
    conduitColor: '#a855f7',
    detail: 'Atlas Engine screens payload through Einstein Trust Layer (masking PII), matches Topic ColdChain_Rescue (confidence 0.992), grounds in GHMC flood SOP vector, and plans Invocable Apex action.',
    payload: {
      atlas_reasoning_trace: {
        trust_layer: {
          pii_masked: true,
          toxicity_score: 0.001,
          harm_check: "PASSED"
        },
        topic_matching: {
          matched_topic: "ColdChain_Rescue",
          confidence: 0.992
        },
        grounding: {
          vector_index: "SOP_ColdChain_Contingency__dlm",
          matched_section: "Protocol 4B: Hyderabad Monsoonal Excursions"
        },
        synthesized_action_plan: [
          "INVOKE: headless360_dispatch(create_case)",
          "DISPATCH: drone_rescue_unit(Depot_04)",
          "NOTIFY_HXL: slack_block_kit(Operations_Concierge)"
        ]
      }
    }
  },
  {
    step: 5,
    title: 'Stage 5: Headless 360 MCP Tool Dispatch',
    action: 'Plane 2 Governed Action Execution',
    buildingId: 'b_mcp_action',
    targetBuildingId: 'b_headless_gateway',
    conduitColor: '#ec4899',
    detail: 'MCP Server invokes headless360_dispatch tool executing WITH USER_MODE. Creates P0 Care Case CASE-99120 and reserves backup cryogenic payload at EV Depot.',
    payload: {
      jsonrpc: "2.0",
      method: "tools/call",
      params: {
        name: "headless360_dispatch",
        arguments: {
          action: "create_case_and_reserve",
          record_type: "Cold_Chain_Emergency",
          fields: {
            Subject: "Urgent P0 Excursion - Dr. Meera Reddy Consignment",
            Priority: "Critical",
            Consignment__c: "SH-88392",
            Customer_Golden_Id__c: "UID-88291"
          }
        }
      },
      response: {
        status: "SUCCESS",
        case_id: "5008800000XyZ1A",
        case_number: "CASE-99120",
        fls_enforced: true,
        execution_time_ms: 38
      }
    }
  },
  {
    step: 6,
    title: 'Stage 6: Headless Experience Layer (Slack HXL)',
    action: 'Slack Concierge Interactive Dispatch',
    buildingId: 'b_headless_gateway',
    targetBuildingId: 'b_headless_gateway',
    conduitColor: '#10b981',
    detail: 'Headless 360 broadcasts interactive Slack Block Kit card to operations concierge Ananya Rao with 1-click rescue drone authorization. Mission dispatched in under 4 seconds.',
    payload: {
      hxl_surface: "Slack_Concierge_App",
      channel: "#indra-coldchain-ops",
      block_kit: [
        {
          type: "header",
          text: "🚨 P0 COLD-CHAIN RESCUE REQUIRED"
        },
        {
          type: "section",
          fields: [
            "Consignee: Dr. Meera Reddy (VIP)",
            "Excursion: 9.2°C (+1.2°C)",
            "Case: CASE-99120",
            "SLA Remaining: 14 Mins"
          ]
        },
        {
          type: "actions",
          elements: [
            {
              type: "button",
              style: "primary",
              text: "⚡ Authorize Autonomous EV Drone"
            }
          ]
        }
      ]
    }
  }
];

export class SimulationController {
  constructor(container, isoCanvas, particleSystem) {
    this.container = container;
    this.isoCanvas = isoCanvas;
    this.particleSystem = particleSystem;
    this.currentStep = 0;
    this.isPlaying = false;
    this.timer = null;
    this.isPayloadOpen = false;
  }

  start() {
    this.container.classList.remove('hidden');
    this.currentStep = 0;
    this.isPlaying = true;
    this.executeStep(0);
    this.scheduleNext();
    sfx.openModal();
  }

  stop() {
    this.isPlaying = false;
    if (this.timer) clearTimeout(this.timer);
    this.container.classList.add('hidden');
    sfx.closeModal();
  }

  togglePlay() {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.play();
    }
  }

  play() {
    this.isPlaying = true;
    sfx.click();
    this.scheduleNext();
    this.render();
  }

  pause() {
    this.isPlaying = false;
    if (this.timer) clearTimeout(this.timer);
    sfx.click();
    this.render();
  }

  next() {
    if (this.currentStep < RESCUE_STAGES.length - 1) {
      this.jumpToStep(this.currentStep + 1);
    }
  }

  prev() {
    if (this.currentStep > 0) {
      this.jumpToStep(this.currentStep - 1);
    }
  }

  reset() {
    this.jumpToStep(0);
  }

  jumpToStep(index) {
    if (this.timer) clearTimeout(this.timer);
    this.currentStep = index;
    this.executeStep(index);
    if (this.isPlaying) {
      this.scheduleNext();
    } else {
      this.render();
    }
  }

  scheduleNext() {
    if (this.timer) clearTimeout(this.timer);
    this.timer = setTimeout(() => {
      if (this.isPlaying) {
        if (this.currentStep < RESCUE_STAGES.length - 1) {
          this.jumpToStep(this.currentStep + 1);
        } else {
          this.pause();
        }
      }
    }, 3800);
  }

  executeStep(index) {
    const stage = RESCUE_STAGES[index];
    if (!stage) return;

    // Focus camera on source building
    this.isoCanvas.focusBuilding(stage.buildingId);
    sfx.pulse();

    // Spawn animated data packets along conduit
    const b1 = this.isoCanvas.buildings.find(b => b.id === stage.buildingId);
    const b2 = this.isoCanvas.buildings.find(b => b.id === stage.targetBuildingId);
    if (b1 && b2) {
      this.particleSystem.spawnPacket(b1, b2, stage.conduitColor, 0.025);
    }

    this.render();
  }

  render() {
    const stage = RESCUE_STAGES[this.currentStep];
    const total = RESCUE_STAGES.length;

    this.container.innerHTML = `
      <div style="position: absolute; top: 88px; left: 50%; transform: translateX(-50%); z-index: 45; width: 94%; max-width: 860px; background: rgba(8, 12, 22, 0.96); backdrop-filter: blur(28px); border: 1px solid rgba(16, 185, 129, 0.45); border-radius: 12px; box-shadow: 0 24px 60px rgba(0, 0, 0, 0.85), 0 0 35px rgba(16, 185, 129, 0.2); overflow: hidden; animation: sim-fade 0.2s ease;">
        
        <!-- Top Operational Stage Bar -->
        <div style="padding: 12px 18px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: rgba(5, 8, 16, 0.7); display: flex; align-items: center; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <span class="datum-tag" style="border-color: #10b981; color: #10b981;">
              STAGE ${stage.step} OF ${total}
            </span>
            <span style="font-size: 13px; font-weight: 700; color: #ffffff;">${stage.title}</span>
          </div>

          <div style="display: flex; align-items: center; gap: 8px;">
            <button id="btn-toggle-payload" class="action-btn-primary" style="padding: 4px 10px; font-size: 11px;">
              ${this.isPayloadOpen ? 'Hide Payload' : 'Inspect JSON Payload 📄'}
            </button>
            <button id="btn-close-sim" class="action-btn-ghost" style="padding: 4px 8px; font-size: 12px;">
              ✕ Close
            </button>
          </div>
        </div>

        <!-- Interactive Stage Breadcrumb Tabs -->
        <div style="display: flex; border-bottom: 1px solid rgba(255, 255, 255, 0.06); background: rgba(5, 8, 16, 0.5); overflow-x: auto;">
          ${RESCUE_STAGES.map((s, idx) => {
            const isActive = idx === this.currentStep;
            return `
              <button class="stage-tab-btn" data-step="${idx}" style="flex: 1; padding: 8px 10px; font-size: 11px; font-family: 'JetBrains Mono', monospace; font-weight: 600; border: none; border-bottom: 2px solid ${isActive ? '#10b981' : 'transparent'}; background: ${isActive ? 'rgba(16, 185, 129, 0.12)' : 'transparent'}; color: ${isActive ? '#10b981' : '#94a3b8'}; cursor: pointer; transition: all 0.15s; white-space: nowrap;">
                ${s.step}. ${s.action.split(' ')[0]}
              </button>
            `;
          }).join('')}
        </div>

        <!-- Stage Narrative Detail -->
        <div style="padding: 16px 20px; display: flex; flex-direction: column; gap: 10px;">
          <p style="margin: 0; font-size: 13px; color: #f1f5f9; line-height: 1.5;">${stage.detail}</p>

          <!-- Collapsible Payload Inspector -->
          ${this.isPayloadOpen ? `
            <div style="margin-top: 6px; padding: 14px; background: #050811; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 11px; font-family: 'JetBrains Mono', monospace; color: #10b981; font-weight: 700;">LIVE TELEMETRY / PROTOCOL PAYLOAD</span>
                <span class="datum-tag">JSON-RPC / REST GRAPHQL</span>
              </div>
              <pre style="margin: 0; max-height: 180px; overflow-y: auto; font-size: 11px; color: #6ee7b7; font-family: 'JetBrains Mono', monospace;"><code>${JSON.stringify(stage.payload, null, 2)}</code></pre>
            </div>
          ` : ''}
        </div>

        <!-- Bottom Playback Controls Bar -->
        <div style="padding: 10px 18px; border-top: 1px solid rgba(255, 255, 255, 0.08); background: rgba(5, 8, 16, 0.85); display: flex; align-items: center; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 6px;">
            <button id="btn-sim-reset" class="action-btn-ghost" title="Reset (0)" style="padding: 5px 10px; font-size: 11.5px;">
              ⟲ Reset
            </button>
            <button id="btn-sim-prev" class="action-btn-ghost" title="Previous Step" style="padding: 5px 10px; font-size: 11.5px;" ${this.currentStep === 0 ? 'disabled style="opacity: 0.3;"' : ''}>
              ◀ Back
            </button>
            <button id="btn-sim-play" class="action-btn-primary" style="padding: 5px 14px; font-size: 11.5px; background: #059669;">
              ${this.isPlaying ? '❚❚ Pause' : '▶ Play'}
            </button>
            <button id="btn-sim-next" class="action-btn-ghost" title="Next Step" style="padding: 5px 10px; font-size: 11.5px;" ${this.currentStep === total - 1 ? 'disabled style="opacity: 0.3;"' : ''}>
              Forward ▶
            </button>
          </div>

          <div style="font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace;">
            SPACEBAR: PLAY/PAUSE • CLICK STAGES TO SCRUB
          </div>
        </div>

      </div>
    `;

    this.container.querySelector('#btn-close-sim').onclick = () => this.stop();
    this.container.querySelector('#btn-sim-play').onclick = () => this.togglePlay();
    this.container.querySelector('#btn-sim-next').onclick = () => this.next();
    this.container.querySelector('#btn-sim-prev').onclick = () => this.prev();
    this.container.querySelector('#btn-sim-reset').onclick = () => this.reset();

    const payloadBtn = this.container.querySelector('#btn-toggle-payload');
    if (payloadBtn) {
      payloadBtn.onclick = () => {
        this.isPayloadOpen = !this.isPayloadOpen;
        this.render();
      };
    }

    this.container.querySelectorAll('.stage-tab-btn').forEach(btn => {
      btn.onclick = () => {
        const stepIdx = parseInt(btn.dataset.step, 10);
        this.jumpToStep(stepIdx);
      };
    });
  }
}
