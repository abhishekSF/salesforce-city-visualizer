import { METADATA_CATALOG } from './data/metadataCatalog.js';
import { ParticleSystem } from './engine/ParticleSystem.js';
import { IsometricCanvas } from './engine/IsometricCanvas.js';
import { BuildingInspector } from './components/BuildingInspector.js';
import { ConceptModal } from './components/ConceptModal.js';
import { CommandPalette } from './components/CommandPalette.js';
import { GuidedTour } from './components/GuidedTour.js';
import { SimulationController } from './components/SimulationController.js';
import { sfx } from './engine/SoundFx.js';

document.addEventListener('DOMContentLoaded', () => {
  const canvasEl = document.getElementById('city-canvas');
  const inspectorContainer = document.getElementById('building-inspector');
  const modalContainer = document.getElementById('concept-modal');
  const paletteContainer = document.getElementById('command-palette-modal');
  const tourContainer = document.getElementById('guided-tour-container');
  const simContainer = document.getElementById('simulation-controller-container');
  const shortcutsContainer = document.getElementById('shortcuts-modal');

  const particleSystem = new ParticleSystem();
  const isoCanvas = new IsometricCanvas(canvasEl, METADATA_CATALOG, particleSystem);

  const inspector = new BuildingInspector(inspectorContainer, (building) => {
    handleBuildingAction(building, isoCanvas, particleSystem);
  });

  const conceptModal = new ConceptModal(modalContainer);

  const commandPalette = new CommandPalette(
    paletteContainer,
    METADATA_CATALOG,
    (buildingId) => {
      isoCanvas.focusBuilding(buildingId);
      const b = METADATA_CATALOG.buildings.find(item => item.id === buildingId);
      if (b) inspector.show(b);
    },
    (conceptId) => {
      conceptModal.show(conceptId);
    }
  );

  const guidedTour = new GuidedTour(tourContainer, isoCanvas, (conceptId) => {
    conceptModal.show(conceptId);
  });

  const simController = new SimulationController(simContainer, isoCanvas, particleSystem);

  // Hook building selection on canvas click
  isoCanvas.onBuildingSelected = (building) => {
    inspector.show(building);
  };

  // Wire up Program / Layer Filter segmented buttons
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.dataset.filter;
      isoCanvas.activeFilter = filter;
      sfx.districtSelect();
    });
  });

  // Top Action Buttons
  document.getElementById('btn-open-search').addEventListener('click', () => {
    commandPalette.open();
  });

  document.getElementById('btn-start-tour').addEventListener('click', () => {
    guidedTour.start(0);
  });

  document.getElementById('btn-open-academy').addEventListener('click', () => {
    conceptModal.show('headless360');
  });

  document.getElementById('btn-run-simulation').addEventListener('click', () => {
    simController.start();
  });

  const calloutBtn = document.getElementById('btn-toggle-callouts');
  if (calloutBtn) {
    calloutBtn.addEventListener('click', () => {
      isoCanvas.showCallouts = !isoCanvas.showCallouts;
      calloutBtn.style.color = isoCanvas.showCallouts ? '#38bdf8' : '#64748b';
      sfx.click();
    });
  }

  document.getElementById('btn-shortcuts').addEventListener('click', () => {
    toggleShortcutsModal(shortcutsContainer);
  });

  document.getElementById('btn-toggle-sound').addEventListener('click', (e) => {
    const isMuted = sfx.toggleMute();
    e.target.innerHTML = isMuted ? '🔇' : '🔊';
  });

  document.getElementById('btn-center-camera').addEventListener('click', () => {
    isoCanvas.centerCamera();
    sfx.click();
  });

  // Quick Zone Jump buttons in bottom dock
  document.querySelectorAll('.district-jump-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetBuildingId = btn.dataset.target;
      isoCanvas.focusBuilding(targetBuildingId);
      const b = METADATA_CATALOG.buildings.find(item => item.id === targetBuildingId);
      if (b) inspector.show(b);
    });
  });

  // District Quick Jump Map
  const districtJumps = {
    '1': 'b_standard_objects',
    '2': 'b_apex_foundry',
    '3': 'b_data_lake',
    '4': 'b_headless_gateway',
    '5': 'b_agentforce_core',
    '6': 'b_claudeforce_lab',
    '7': 'b_mcp_context'
  };

  // Global Keyboard Shortcuts
  window.addEventListener('keydown', (e) => {
    // Ignore input focus
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    if (e.key === 't' || e.key === 'T') {
      e.preventDefault();
      if (guidedTour.isActive) {
        guidedTour.stop();
      } else {
        guidedTour.start(0);
      }
    } else if (e.key === ' ' && !simContainer.classList.contains('hidden')) {
      e.preventDefault();
      simController.togglePlay();
    } else if (e.key === '?') {
      e.preventDefault();
      toggleShortcutsModal(shortcutsContainer);
    } else if (districtJumps[e.key]) {
      const bId = districtJumps[e.key];
      isoCanvas.focusBuilding(bId);
      const b = METADATA_CATALOG.buildings.find(item => item.id === bId);
      if (b) inspector.show(b);
    } else if (e.key === 'c' || e.key === 'C') {
      isoCanvas.centerCamera();
    } else if (e.key === 'm' || e.key === 'M') {
      const isMuted = sfx.toggleMute();
      const soundBtn = document.getElementById('btn-toggle-sound');
      if (soundBtn) soundBtn.innerHTML = isMuted ? '🔇' : '🔊';
    } else if (e.key === 'Escape') {
      if (guidedTour.isActive) guidedTour.stop();
      if (!shortcutsContainer.classList.contains('hidden')) shortcutsContainer.classList.add('hidden');
      if (!modalContainer.classList.contains('hidden')) conceptModal.hide();
      if (!inspectorContainer.classList.contains('hidden')) inspector.hide();
      if (!simContainer.classList.contains('hidden')) simController.stop();
    }
  });

  // Animation Loop
  let lastTime = performance.now();
  function loop(currentTime) {
    const delta = currentTime - lastTime;
    lastTime = currentTime;

    particleSystem.update(delta);
    isoCanvas.render(currentTime);

    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
});

function toggleShortcutsModal(container) {
  if (!container.classList.contains('hidden')) {
    container.classList.add('hidden');
    sfx.closeModal();
    return;
  }

  container.classList.remove('hidden');
  sfx.openModal();

  container.innerHTML = `
    <div class="modal-overlay">
      <div class="modal-window" style="max-width: 580px; height: auto;">
        <div style="padding: 16px 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: rgba(8, 12, 22, 0.9); display: flex; align-items: center; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 18px;">⌨️</span>
            <span style="font-size: 14px; font-weight: 700; color: #ffffff;">Keyboard Shortcuts & Navigation</span>
          </div>
          <button id="btn-close-shortcuts" class="action-btn-ghost" style="padding: 4px 8px; font-size: 12px;">✕</button>
        </div>

        <div style="padding: 20px; display: flex; flex-direction: column; gap: 12px; font-size: 12.5px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Universal Search & Command Palette</span>
            <span class="datum-tag" style="color: #00f0ff; border-color: #00f0ff;">⌘K / Ctrl+K</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Start / Stop Guided Architectural Tour</span>
            <span class="datum-tag" style="color: #38bdf8; border-color: #38bdf8;">T</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Play / Pause Interactive Simulation</span>
            <span class="datum-tag" style="color: #10b981; border-color: #10b981;">Space</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Quick-Jump to Districts (1 to 7)</span>
            <span class="datum-tag" style="color: #a855f7; border-color: #a855f7;">1 - 7</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Center Camera on Masterplan</span>
            <span class="datum-tag" style="color: #f59e0b; border-color: #f59e0b;">C</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Toggle Procedural Audio FX</span>
            <span class="datum-tag" style="color: #f97316; border-color: #f97316;">M</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Close Any Modal / Panel</span>
            <span class="datum-tag">Esc</span>
          </div>
        </div>

        <div style="padding: 12px 20px; border-top: 1px solid rgba(255, 255, 255, 0.08); background: rgba(5, 8, 16, 0.85); display: flex; justify-content: flex-end;">
          <button id="btn-close-shortcuts-btn" class="action-btn-primary" style="padding: 6px 14px; font-size: 11.5px;">Close</button>
        </div>
      </div>
    </div>
  `;

  container.querySelector('#btn-close-shortcuts').onclick = () => container.classList.add('hidden');
  container.querySelector('#btn-close-shortcuts-btn').onclick = () => container.classList.add('hidden');
  container.querySelector('.modal-overlay').onclick = (e) => {
    if (e.target.classList.contains('modal-overlay')) container.classList.add('hidden');
  };
}

function handleBuildingAction(building, isoCanvas, particleSystem) {
  sfx.simulationStep();
  const consoleEl = document.getElementById('action-console-log');
  if (!consoleEl) return;

  consoleEl.innerHTML = `<div style="color: #38bdf8; font-family: 'JetBrains Mono', monospace; font-weight: 700;">⚡ DISPATCHING CIRCULATION FROM ${building.name.toUpperCase()}...</div>`;

  if (building.relationships && building.relationships.length > 0) {
    building.relationships.forEach((relId, idx) => {
      const targetB = isoCanvas.buildings.find(b => b.id === relId);
      if (targetB) {
        setTimeout(() => {
          particleSystem.spawnPacket(building, targetB, building.color || '#38bdf8', 0.025);
          sfx.pulse();
          consoleEl.innerHTML += `
            <div style="color: #cbd5e1; font-family: 'JetBrains Mono', monospace;">→ Vector routed to <strong style="color: #10b981;">${targetB.name}</strong></div>
          `;
        }, idx * 240);
      }
    });

    setTimeout(() => {
      consoleEl.innerHTML += `<div style="color: #10b981; font-family: 'JetBrains Mono', monospace; font-weight: 700; margin-top: 4px;">✓ CIRCULATION SYNCHRONIZED ACROSS ARCHITECTURAL FABRIC!</div>`;
    }, building.relationships.length * 240 + 100);
  } else {
    consoleEl.innerHTML += `<div style="color: #94a3b8; font-family: 'JetBrains Mono', monospace;">No outbound conduits configured for node.</div>`;
  }
}
