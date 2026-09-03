import { sfx } from '../engine/SoundFx.js';

export class CommandPalette {
  constructor(container, catalog, onSelectBuilding, onSelectConcept) {
    this.container = container;
    this.catalog = catalog;
    this.onSelectBuilding = onSelectBuilding;
    this.onSelectConcept = onSelectConcept;
    this.isOpen = false;
    this.selectedIndex = 0;
    this.filteredItems = [];

    this.initItems();
    this.bindGlobalKeys();
  }

  initItems() {
    this.allItems = [];

    // 1. Buildings
    this.catalog.buildings.forEach(b => {
      this.allItems.push({
        type: 'building',
        category: 'BUILDING / DISTRICT',
        id: b.id,
        title: b.name,
        subtitle: `${b.subtitle} • District: ${b.districtId}`,
        tags: b.tags || [],
        color: b.color || '#38bdf8',
        icon: '🏢',
        raw: b
      });
    });

    // 2. Concepts
    const concepts = [
      { id: 'headless360', title: 'Headless 360 Architecture', subtitle: 'The API is the UI. Decoupled HXL, GraphQL & Composite APIs', category: 'SYSTEM CONCEPT', icon: '🚀', color: '#10b981' },
      { id: 'agentforce', title: 'Agentforce & Atlas Reasoning Loop', subtitle: 'Autonomous Perception, Grounding & Invocable Execution', category: 'SYSTEM CONCEPT', icon: '🤖', color: '#a855f7' },
      { id: 'claudeforce', title: 'Claudeforce (Claude 3.5 Sonnet)', subtitle: '200k Context Auditing, Multi-modal Vision & Apex Synthesis', category: 'SYSTEM CONCEPT', icon: '🧠', color: '#f97316' },
      { id: 'mcpApis', title: 'Dual-Plane Hosted MCP Architecture', subtitle: 'Plane 1 (Context data360) vs Plane 2 (Action headless-360)', category: 'SYSTEM CONCEPT', icon: '🔌', color: '#ec4899' },
      { id: 'semanticMatrix', title: 'Semantic Layer vs Metadata Matrix', subtitle: 'Three Tiers: Relational DB -> Declarative Metadata -> Semantic Graph', category: 'SYSTEM CONCEPT', icon: '🏢', color: '#00f0ff' }
    ];

    concepts.forEach(c => {
      this.allItems.push({
        type: 'concept',
        category: 'ARCHITECTURE CONCEPT',
        id: c.id,
        title: c.title,
        subtitle: c.subtitle,
        tags: ['architecture', 'guide', 'deep-dive'],
        color: c.color,
        icon: c.icon
      });
    });

    // 3. Specific SObjects & Schemas
    const schemas = [
      { id: 'b_standard_objects', title: 'Account & Contact (Standard SObjects)', subtitle: 'Core relational entities with FLS & Record Types', category: 'METADATA SCHEMA', icon: '📦', color: '#38bdf8' },
      { id: 'b_custom_objects', title: 'Logistics_Depot__c (Custom SObject)', subtitle: 'Physical facility node with cold-chain capacity', category: 'METADATA SCHEMA', icon: '📦', color: '#38bdf8' },
      { id: 'b_flow_plant', title: 'INDRA_Autolaunched_Rescue (Flow)', subtitle: 'Declarative transactional orchestration engine', category: 'LOGIC & AUTOMATION', icon: '⚡', color: '#f59e0b' },
      { id: 'b_apex_foundry', title: 'INDRA_UnifiedContextService.cls (Apex)', subtitle: 'Invocable Apex executed WITH USER_MODE', category: 'LOGIC & AUTOMATION', icon: '⚡', color: '#f59e0b' },
      { id: 'b_data_refinery', title: 'UnifiedIndividual__dlm (Data Cloud DMO)', subtitle: 'Deterministic & probabilistic Golden Record entity', category: 'SEMANTIC GRAPH', icon: '🌊', color: '#06b6d4' },
      { id: 'b_calculated_insights', title: 'Care_Risk_Score__cio (Calculated Insight)', subtitle: 'Continuous SQL aggregations over streaming lakes', category: 'SEMANTIC GRAPH', icon: '🌊', color: '#06b6d4' },
      { id: 'b_mcp_action', title: 'headless360_dispatch (MCP Tool)', subtitle: 'Plane 2 Action dispatcher enforcing user context', category: 'MCP TOOLS', icon: '🔌', color: '#ec4899' }
    ];

    schemas.forEach(s => {
      this.allItems.push({
        type: 'building',
        category: s.category,
        id: s.id,
        title: s.title,
        subtitle: s.subtitle,
        tags: ['schema', 'code', 'metadata'],
        color: s.color,
        icon: s.icon
      });
    });
  }

  bindGlobalKeys() {
    window.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'K')) {
        e.preventDefault();
        this.toggle();
      } else if (e.key === 'Escape' && this.isOpen) {
        this.close();
      }
    });
  }

  toggle() {
    if (this.isOpen) {
      this.close();
    } else {
      this.open();
    }
  }

  open() {
    this.isOpen = true;
    this.selectedIndex = 0;
    this.container.classList.remove('hidden');
    this.render();
    sfx.openModal();

    setTimeout(() => {
      const input = this.container.querySelector('#command-search-input');
      if (input) input.focus();
    }, 50);
  }

  close() {
    this.isOpen = false;
    this.container.classList.add('hidden');
    sfx.closeModal();
  }

  filter(query) {
    const q = query.toLowerCase().trim();
    if (!q) {
      this.filteredItems = this.allItems.slice(0, 8);
    } else {
      this.filteredItems = this.allItems.filter(item => {
        const titleMatch = item.title.toLowerCase().includes(q);
        const subMatch = item.subtitle.toLowerCase().includes(q);
        const tagMatch = item.tags && item.tags.some(t => t.toLowerCase().includes(q));
        const catMatch = item.category.toLowerCase().includes(q);
        return titleMatch || subMatch || tagMatch || catMatch;
      });
    }
    this.selectedIndex = Math.min(this.selectedIndex, Math.max(0, this.filteredItems.length - 1));
    this.renderList();
  }

  selectItem(index) {
    const item = this.filteredItems[index];
    if (!item) return;

    this.close();
    sfx.click();

    if (item.type === 'building') {
      if (this.onSelectBuilding) {
        this.onSelectBuilding(item.id);
      }
    } else if (item.type === 'concept') {
      if (this.onSelectConcept) {
        this.onSelectConcept(item.id);
      }
    }
  }

  render() {
    this.container.innerHTML = `
      <div class="modal-overlay" style="align-items: flex-start; padding-top: 12vh;">
        <div class="palette-window" style="width: 100%; max-width: 640px; background: rgba(10, 15, 26, 0.96); backdrop-filter: blur(28px); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 12px; box-shadow: 0 30px 70px rgba(0, 0, 0, 0.9), 0 0 40px rgba(0, 240, 255, 0.2); overflow: hidden; display: flex; flex-direction: column;">
          
          <!-- Search Input Header -->
          <div style="padding: 14px 18px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); display: flex; align-items: center; gap: 12px; background: rgba(5, 8, 16, 0.6);">
            <span style="font-size: 16px; color: #38bdf8;">🔍</span>
            <input id="command-search-input" type="text" placeholder="Search SObjects, Flows, DMOs, Apex, or Concepts (e.g. Atlas, Golden Record, MCP)..." 
              style="flex: 1; background: transparent; border: none; outline: none; font-size: 13.5px; font-family: var(--font-sans); color: #ffffff; caret-color: #00f0ff;" />
            <span class="datum-tag" style="font-size: 9.5px; font-family: 'JetBrains Mono', monospace;">ESC TO EXIT</span>
          </div>

          <!-- Results List Container -->
          <div id="palette-results" style="max-height: 380px; overflow-y: auto; padding: 8px 0; display: flex; flex-direction: column;">
            <!-- Populated dynamically -->
          </div>

          <!-- Footer Tips -->
          <div style="padding: 10px 18px; border-top: 1px solid rgba(255, 255, 255, 0.08); background: rgba(5, 8, 16, 0.8); display: flex; align-items: center; justify-content: space-between; font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace;">
            <span>↑ ↓ TO NAVIGATE</span>
            <span>↵ TO SELECT & FLY CAMERA</span>
          </div>
        </div>
      </div>
    `;

    const input = this.container.querySelector('#command-search-input');
    input.addEventListener('input', (e) => this.filter(e.target.value));
    input.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        this.selectedIndex = (this.selectedIndex + 1) % Math.max(1, this.filteredItems.length);
        this.renderList();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        this.selectedIndex = (this.selectedIndex - 1 + this.filteredItems.length) % Math.max(1, this.filteredItems.length);
        this.renderList();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        this.selectItem(this.selectedIndex);
      }
    });

    this.container.querySelector('.modal-overlay').addEventListener('click', (e) => {
      if (e.target.classList.contains('modal-overlay')) {
        this.close();
      }
    });

    this.filter('');
  }

  renderList() {
    const listEl = this.container.querySelector('#palette-results');
    if (!listEl) return;

    if (this.filteredItems.length === 0) {
      listEl.innerHTML = `
        <div style="padding: 24px; text-align: center; color: #64748b; font-size: 12px; font-family: 'JetBrains Mono', monospace;">
          No matching architectural nodes or concepts found.
        </div>
      `;
      return;
    }

    listEl.innerHTML = this.filteredItems.map((item, idx) => {
      const isSelected = idx === this.selectedIndex;
      return `
        <div class="palette-item" data-index="${idx}" style="padding: 10px 18px; display: flex; align-items: center; justify-content: space-between; cursor: pointer; transition: all 0.1s; background: ${isSelected ? 'rgba(56, 189, 248, 0.12)' : 'transparent'}; border-left: 3px solid ${isSelected ? item.color : 'transparent'};">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 30px; height: 30px; border-radius: 6px; background: ${item.color}15; border: 1px solid ${item.color}44; display: flex; align-items: center; justify-content: center; font-size: 14px;">
              ${item.icon}
            </div>
            <div>
              <div style="font-size: 13px; font-weight: 600; color: ${isSelected ? '#ffffff' : '#cbd5e1'};">
                ${item.title}
              </div>
              <div style="font-size: 11px; color: #94a3b8;">
                ${item.subtitle}
              </div>
            </div>
          </div>
          <span class="datum-tag" style="font-size: 9px; color: ${item.color}; border-color: ${item.color}44;">
            ${item.category}
          </span>
        </div>
      `;
    }).join('');

    listEl.querySelectorAll('.palette-item').forEach(el => {
      el.addEventListener('mouseenter', () => {
        this.selectedIndex = parseInt(el.dataset.index, 10);
        this.renderList();
      });
      el.addEventListener('click', () => {
        this.selectItem(parseInt(el.dataset.index, 10));
      });
    });

    const activeEl = listEl.querySelector(`[data-index="${this.selectedIndex}"]`);
    if (activeEl) {
      activeEl.scrollIntoView({ block: 'nearest' });
    }
  }
}
