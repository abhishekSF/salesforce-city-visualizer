/**
 * FieldGuide.js - Discovery Tracker & Architectural Field Guide
 * Records landmarks discovered by the explorer in localStorage,
 * provides celebratory discovery popups, district completion stats,
 * and fast-travel coordinates for discovered landmarks.
 */

import { sfx } from '../engine/SoundFx.js';

const STORAGE_KEY = 'salesforce_rpg_discovery_v1';

export class FieldGuide {
  constructor(container, catalog, onFastTravel, onOpenDossier) {
    this.container = container;
    this.catalog = catalog;
    this.onFastTravel = onFastTravel;
    this.onOpenDossier = onOpenDossier;

    this.discoveredIds = new Set();
    this.totalLandmarks = catalog.buildings.length;
    this.toastTimer = null;

    this.loadState();
  }

  loadState() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const arr = JSON.parse(saved);
        arr.forEach(id => this.discoveredIds.add(id));
      }
    } catch (e) {
      console.warn('Could not read discovery state from localStorage', e);
    }
  }

  saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify([...this.discoveredIds]));
    } catch (e) {
      console.warn('Could not save discovery state to localStorage', e);
    }
  }

  isDiscovered(id) {
    return this.discoveredIds.has(id);
  }

  discover(building) {
    if (this.discoveredIds.has(building.id)) return false;

    this.discoveredIds.add(building.id);
    this.saveState();
    sfx.simulationStep();

    this.showDiscoveryToast(building);

    if (this.onDiscoveryChange) {
      this.onDiscoveryChange(this.discoveredIds.size, this.totalLandmarks);
    }
    return true;
  }

  showDiscoveryToast(building) {
    let toast = document.getElementById('rpg-discovery-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'rpg-discovery-toast';
      document.body.appendChild(toast);
    }

    const count = this.discoveredIds.size;
    toast.innerHTML = `
      <div style="position: fixed; top: 88px; left: 50%; transform: translateX(-50%); z-index: 55; width: 92%; max-width: 540px; background: rgba(8, 12, 22, 0.96); backdrop-filter: blur(28px); border: 1.5px solid #00f0ff; border-radius: 12px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9), 0 0 30px rgba(0, 240, 255, 0.3); padding: 14px 18px; display: flex; align-items: flex-start; gap: 14px; animation: toast-drop 0.3s cubic-bezier(0.16, 1, 0.3, 1);">
        <div style="width: 42px; height: 42px; border-radius: 10px; background: rgba(0, 240, 255, 0.15); border: 1px solid #00f0ff; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0;">
          ✨
        </div>
        <div style="flex: 1;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 2px;">
            <span style="font-size: 10px; font-weight: 700; color: #00f0ff; letter-spacing: 0.05em; font-family: 'JetBrains Mono', monospace;">LANDMARK DISCOVERED</span>
            <span class="datum-tag" style="border-color: #00f0ff; color: #00f0ff;">${count} / ${this.totalLandmarks}</span>
          </div>
          <div style="font-size: 14px; font-weight: 700; color: #ffffff;">${building.name}</div>
          <div style="font-size: 11.5px; color: #94a3b8; margin-top: 2px;">${building.summary}</div>
          <div style="margin-top: 10px; display: flex; align-items: center; gap: 8px;">
            <button id="toast-view-dossier" class="action-btn-primary" style="padding: 4px 10px; font-size: 11px;">
              Open Technical Dossier
            </button>
            <span style="font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace;">Press [E] anytime</span>
          </div>
        </div>
      </div>
    `;

    const btn = toast.querySelector('#toast-view-dossier');
    if (btn) {
      btn.onclick = () => {
        toast.remove();
        if (this.onOpenDossier) this.onOpenDossier(building);
      };
    }

    if (this.toastTimer) clearTimeout(this.toastTimer);
    this.toastTimer = setTimeout(() => {
      if (toast && toast.parentNode) toast.remove();
    }, 5500);
  }

  show() {
    this.container.classList.remove('hidden');
    this.render();
    sfx.openModal();
  }

  hide() {
    this.container.classList.add('hidden');
    sfx.closeModal();
  }

  render() {
    const total = this.totalLandmarks;
    const discovered = this.discoveredIds.size;
    const pct = Math.round((discovered / total) * 100);

    // Group buildings by district
    const districts = [
      { id: 'metadata', name: '1. Metadata Citadel', color: '#38bdf8' },
      { id: 'automation', name: '2. Logic & Automation Grid', color: '#f59e0b' },
      { id: 'semantic', name: '3. Data Cloud & Semantic Harbor', color: '#06b6d4' },
      { id: 'headless', name: '4. Headless 360 Skyport', color: '#10b981' },
      { id: 'agentforce', name: '5. Agentforce Autonomous Forum', color: '#a855f7' },
      { id: 'claudeforce', name: '6. Claudeforce Research Complex', color: '#f97316' },
      { id: 'mcp', name: '7. Dual-Plane MCP Interchange', color: '#ec4899' }
    ];

    this.container.innerHTML = `
      <div class="modal-overlay">
        <div class="modal-window" style="max-width: 960px; height: 86vh;">
          
          <!-- Header -->
          <div style="padding: 16px 24px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: rgba(8, 12, 22, 0.95); display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 12px;">
              <span style="font-size: 24px;">📖</span>
              <div>
                <h1 style="margin: 0; font-size: 16px; font-weight: 700; color: #ffffff;">SALESFORCE ARCHITECTURAL FIELD GUIDE</h1>
                <p style="margin: 2px 0 0; font-size: 12px; color: #94a3b8; font-family: 'JetBrains Mono', monospace;">
                  DISCOVERED ${discovered} OF ${total} LANDMARKS (${pct}%)
                </p>
              </div>
            </div>
            <button id="btn-close-guide" class="action-btn-ghost" style="padding: 6px 12px;">✕ Close</button>
          </div>

          <!-- Overall Progress Bar -->
          <div style="padding: 12px 24px; background: rgba(5, 8, 16, 0.6); border-bottom: 1px solid rgba(255, 255, 255, 0.06);">
            <div style="height: 6px; border-radius: 3px; background: rgba(255, 255, 255, 0.1); overflow: hidden;">
              <div style="height: 100%; width: ${pct}%; background: linear-gradient(90deg, #0284c7 0%, #00f0ff 100%); transition: width 0.4s ease;"></div>
            </div>
          </div>

          <!-- District Entries Grid -->
          <div style="flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 20px;">
            ${districts.map(d => {
              const districtBuildings = this.catalog.buildings.filter(b => b.districtId === d.id);
              const districtDiscovered = districtBuildings.filter(b => this.discoveredIds.has(b.id)).length;

              return `
                <div class="arch-card" style="border-left: 4px solid ${d.color};">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-weight: 700; font-size: 14px; color: ${d.color};">${d.name}</span>
                    <span class="datum-tag">${districtDiscovered} / ${districtBuildings.length} Discovered</span>
                  </div>

                  <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 10px;">
                    ${districtBuildings.map(b => {
                      const isFound = this.discoveredIds.has(b.id);
                      if (isFound) {
                        return `
                          <div style="padding: 10px 12px; border-radius: 8px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); display: flex; flex-direction: column; justify-content: space-between; gap: 8px;">
                            <div>
                              <div style="font-weight: 600; font-size: 12.5px; color: #ffffff;">✓ ${b.name}</div>
                              <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">${b.subtitle}</div>
                            </div>
                            <div style="display: flex; gap: 6px; margin-top: 4px;">
                              <button class="btn-dossier action-btn-ghost" data-id="${b.id}" style="padding: 3px 8px; font-size: 10px;">
                                Dossier
                              </button>
                              <button class="btn-fast-travel action-btn-primary" data-id="${b.id}" style="padding: 3px 8px; font-size: 10px;">
                                ✈️ Travel
                              </button>
                            </div>
                          </div>
                        `;
                      } else {
                        return `
                          <div style="padding: 10px 12px; border-radius: 8px; background: rgba(0, 0, 0, 0.25); border: 1px dashed rgba(255, 255, 255, 0.1); display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 18px; opacity: 0.3;">❓</span>
                            <div>
                              <div style="font-size: 12px; font-weight: 600; color: #64748b;">??? (Undiscovered)</div>
                              <div style="font-size: 10.5px; color: #475569;">Explore the ${d.name.split(' ')[1]} zone</div>
                            </div>
                          </div>
                        `;
                      }
                    }).join('')}
                  </div>
                </div>
              `;
            }).join('')}
          </div>

          <!-- Footer -->
          <div style="padding: 12px 24px; border-top: 1px solid rgba(255, 255, 255, 0.08); background: rgba(8, 12, 22, 0.95); display: flex; justify-content: flex-end;">
            <button id="btn-close-guide-footer" class="action-btn-primary" style="padding: 6px 14px; font-size: 11.5px;">Return to World</button>
          </div>
        </div>
      </div>
    `;

    this.container.querySelector('#btn-close-guide').onclick = () => this.hide();
    this.container.querySelector('#btn-close-guide-footer').onclick = () => this.hide();
    this.container.querySelector('.modal-overlay').onclick = (e) => {
      if (e.target.classList.contains('modal-overlay')) this.hide();
    };

    this.container.querySelectorAll('.btn-fast-travel').forEach(btn => {
      btn.onclick = () => {
        const id = btn.dataset.id;
        const b = this.catalog.buildings.find(item => item.id === id);
        this.hide();
        if (b && this.onFastTravel) {
          this.onFastTravel(b);
        }
      };
    });

    this.container.querySelectorAll('.btn-dossier').forEach(btn => {
      btn.onclick = () => {
        const id = btn.dataset.id;
        const b = this.catalog.buildings.find(item => item.id === id);
        this.hide();
        if (b && this.onOpenDossier) {
          this.onOpenDossier(b);
        }
      };
    });
  }
}
