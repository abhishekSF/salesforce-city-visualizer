import { METADATA_CATALOG } from './data/metadataCatalog.js';
import { ParticleSystem } from './engine/ParticleSystem.js';
import { IsometricCanvas } from './engine/IsometricCanvas.js';
import { TopDownWorld } from './engine/TopDownWorld.js';
import { PlayerCharacter } from './engine/PlayerCharacter.js';
import { BuildingInspector } from './components/BuildingInspector.js';
import { ConceptModal } from './components/ConceptModal.js';
import { CommandPalette } from './components/CommandPalette.js';
import { GuidedTour } from './components/GuidedTour.js';
import { FieldGuide } from './components/FieldGuide.js';
import { AtlasCoordinator } from './components/Atlas.js';
import { SimulationController } from './components/SimulationController.js';
import { sfx } from './engine/SoundFx.js';

document.addEventListener('DOMContentLoaded', () => {
  const canvasEl = document.getElementById('city-canvas');
  const inspectorContainer = document.getElementById('building-inspector');
  const modalContainer = document.getElementById('concept-modal');
  const paletteContainer = document.getElementById('command-palette-modal');
  const tourContainer = document.getElementById('guided-tour-container');
  const guideContainer = document.getElementById('field-guide-modal');
  const simContainer = document.getElementById('simulation-controller-container');
  const shortcutsContainer = document.getElementById('shortcuts-modal');

  // Core Engines
  const particleSystem = new ParticleSystem();
  const isoCanvas = new IsometricCanvas(canvasEl, METADATA_CATALOG, particleSystem);
  const topDownWorld = new TopDownWorld(METADATA_CATALOG);
  const player = new PlayerCharacter(420, 420); // Central transit intersection // Starts at Agentforce Central Plaza

  // UI Components
  const inspector = new BuildingInspector(inspectorContainer, (building) => {
    handleBuildingAction(building, isoCanvas, particleSystem);
  });

  const conceptModal = new ConceptModal(modalContainer);

  const fieldGuide = new FieldGuide(
    guideContainer,
    METADATA_CATALOG,
    (building) => {
      atlasCoordinator.fastTravel(building);
    },
    (building) => {
      inspector.show(building);
    }
  );

  // Update initial guide badge count
  const updateGuideBadge = (count, total) => {
    const badge = document.getElementById('guide-badge');
    if (badge) badge.innerText = `Guide (${count}/${total})`;
  };
  fieldGuide.onDiscoveryChange = updateGuideBadge;
  updateGuideBadge(fieldGuide.discoveredIds.size, fieldGuide.totalLandmarks);

  // Dual-Mode Atlas Coordinator
  const atlasCoordinator = new AtlasCoordinator({
    canvas: canvasEl,
    topDownWorld,
    player,
    isoCanvas,
    inspector,
    fieldGuide,
    onModeChange: (mode) => {
      const btnExplore = document.getElementById('btn-mode-explore');
      const btnAtlas = document.getElementById('btn-mode-atlas');
      const draftingGrid = document.querySelector('.drafting-grid');
      const programSelector = document.querySelector('.program-selector');

      if (mode === 'explore') {
        btnExplore.classList.add('active');
        btnAtlas.classList.remove('active');
        if (draftingGrid) draftingGrid.style.display = 'none';
        if (programSelector) programSelector.style.display = 'none';
      } else {
        btnExplore.classList.remove('active');
        btnAtlas.classList.add('active');
        if (draftingGrid) draftingGrid.style.display = 'block';
        if (programSelector) programSelector.style.display = 'flex';
      }
    }
  });

  // Initial UI state setup for explore mode
  const draftingGrid = document.querySelector('.drafting-grid');
  const programSelector = document.querySelector('.program-selector');
  if (draftingGrid) draftingGrid.style.display = 'none';
  if (programSelector) programSelector.style.display = 'none';

  const commandPalette = new CommandPalette(
    paletteContainer,
    METADATA_CATALOG,
    (buildingId) => {
      const b = METADATA_CATALOG.buildings.find(item => item.id === buildingId);
      if (b) atlasCoordinator.fastTravel(b);
    },
    (conceptId) => {
      conceptModal.show(conceptId);
    }
  );

  const guidedTour = new GuidedTour(tourContainer, isoCanvas, (conceptId) => {
    conceptModal.show(conceptId);
  });

  const simController = new SimulationController(simContainer, isoCanvas, particleSystem);

  // Mode Switcher Buttons
  document.getElementById('btn-mode-explore').addEventListener('click', () => {
    atlasCoordinator.setMode('explore');
  });
  document.getElementById('btn-mode-atlas').addEventListener('click', () => {
    atlasCoordinator.setMode('atlas');
  });

  // Header Action Buttons
  document.getElementById('btn-open-guide').addEventListener('click', () => {
    fieldGuide.show();
  });

  document.getElementById('btn-open-search').addEventListener('click', () => {
    commandPalette.open();
  });

  document.getElementById('btn-start-tour').addEventListener('click', () => {
    atlasCoordinator.setMode('atlas');
    guidedTour.start(0);
  });

  document.getElementById('btn-open-academy').addEventListener('click', () => {
    conceptModal.show('headless360');
  });

  document.getElementById('btn-run-simulation').addEventListener('click', () => {
    simController.start();
  });

  document.getElementById('btn-shortcuts').addEventListener('click', () => {
    toggleShortcutsModal(shortcutsContainer);
  });

  document.getElementById('btn-toggle-sound').addEventListener('click', (e) => {
    const isMuted = sfx.toggleMute();
    e.target.innerHTML = isMuted ? '🔇' : '🔊';
  });

  // District Filter Buttons (Atlas Mode)
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      isoCanvas.activeFilter = btn.dataset.filter;
      sfx.districtSelect();
    });
  });

  // Fast Travel Dock Buttons
  document.querySelectorAll('.district-jump-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetBuildingId = btn.dataset.target;
      const b = METADATA_CATALOG.buildings.find(item => item.id === targetBuildingId);
      if (b) atlasCoordinator.fastTravel(b);
    });
  });

  // Mobile Virtual D-Pad Inputs
  const bindTouch = (id, direction) => {
    const el = document.getElementById(id);
    if (!el) return;
    const start = (e) => { e.preventDefault(); player.keys[direction] = true; };
    const end = (e) => { e.preventDefault(); player.keys[direction] = false; };
    el.addEventListener('touchstart', start, { passive: false });
    el.addEventListener('touchend', end, { passive: false });
    el.addEventListener('mousedown', start);
    el.addEventListener('mouseup', end);
  };
  bindTouch('dpad-up', 'up');
  bindTouch('dpad-down', 'down');
  bindTouch('dpad-left', 'left');
  bindTouch('dpad-right', 'right');

  const mobileActionBtn = document.getElementById('mobile-btn-action');
  if (mobileActionBtn) {
    const triggerAction = (e) => {
      e.preventDefault();
      const nearby = topDownWorld.getNearbyBuilding(player.x, player.y);
      if (nearby) {
        fieldGuide.discover(nearby);
        inspector.show(nearby);
      }
    };
    mobileActionBtn.addEventListener('touchstart', triggerAction, { passive: false });
    mobileActionBtn.addEventListener('click', triggerAction);
  }

  // Keyboard Navigation Shortcuts
  const districtJumps = {
    '1': 'b_standard_objects',
    '2': 'b_apex_foundry',
    '3': 'b_data_lake',
    '4': 'b_headless_gateway',
    '5': 'b_agentforce_core',
    '6': 'b_claudeforce_lab',
    '7': 'b_mcp_context'
  };

  window.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    if (e.key === 'g' || e.key === 'G') {
      fieldGuide.show();
    } else if (e.key === 'v' || e.key === 'V') {
      atlasCoordinator.toggleMode();
    } else if (e.key === 't' || e.key === 'T') {
      atlasCoordinator.setMode('atlas');
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
      const b = METADATA_CATALOG.buildings.find(item => item.id === bId);
      if (b) atlasCoordinator.fastTravel(b);
    } else if (e.key === 'm' || e.key === 'M') {
      const isMuted = sfx.toggleMute();
      const soundBtn = document.getElementById('btn-toggle-sound');
      if (soundBtn) soundBtn.innerHTML = isMuted ? '🔇' : '🔊';
    } else if (e.key === 'Escape') {
      if (guidedTour.isActive) guidedTour.stop();
      if (!shortcutsContainer.classList.contains('hidden')) shortcutsContainer.classList.add('hidden');
      if (!modalContainer.classList.contains('hidden')) conceptModal.hide();
      if (!inspectorContainer.classList.contains('hidden')) inspector.hide();
      if (!guideContainer.classList.contains('hidden')) fieldGuide.hide();
      if (!simContainer.classList.contains('hidden')) simController.stop();
    }
  });

  // Main Unified Animation Loop
  let lastTime = performance.now();
  function gameLoop(currentTime) {
    const dt = Math.min(0.1, (currentTime - lastTime) / 1000);
    lastTime = currentTime;

    // Update particles and dual-mode coordinator
    particleSystem.update(dt * 1000);
    atlasCoordinator.update(dt);

    // Render active mode
    atlasCoordinator.render(currentTime);

    requestAnimationFrame(gameLoop);
  }
  requestAnimationFrame(gameLoop);
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
      <div class="modal-window" style="max-width: 600px; height: auto;">
        <div style="padding: 16px 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: rgba(8, 12, 22, 0.9); display: flex; align-items: center; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 18px;">⌨️</span>
            <span style="font-size: 14px; font-weight: 700; color: #ffffff;">Keyboard Navigation & RPG Controls</span>
          </div>
          <button id="btn-close-shortcuts" class="action-btn-ghost" style="padding: 4px 8px; font-size: 12px;">✕</button>
        </div>

        <div style="padding: 20px; display: flex; flex-direction: column; gap: 12px; font-size: 12px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Move Explorer (Explore Mode)</span>
            <span class="datum-tag" style="color: #00f0ff; border-color: #00f0ff;">W A S D / Arrows</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Interact with Landmark / Open Dossier</span>
            <span class="datum-tag" style="color: #00f0ff; border-color: #00f0ff;">E</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Toggle Mode (Explore RPG ↔ Atlas Masterplan)</span>
            <span class="datum-tag" style="color: #38bdf8; border-color: #38bdf8;">V</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Open Architectural Field Guide</span>
            <span class="datum-tag" style="color: #38bdf8; border-color: #38bdf8;">G</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Universal Search & Command Palette</span>
            <span class="datum-tag" style="color: #00f0ff; border-color: #00f0ff;">⌘K / Ctrl+K</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Start / Stop Guided Tour</span>
            <span class="datum-tag" style="color: #10b981; border-color: #10b981;">T</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Play / Pause Simulation</span>
            <span class="datum-tag" style="color: #10b981; border-color: #10b981;">Space</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Fast Travel to Districts (1 to 7)</span>
            <span class="datum-tag" style="color: #a855f7; border-color: #a855f7;">1 - 7</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #cbd5e1;">Toggle Sound Effects</span>
            <span class="datum-tag" style="color: #f97316; border-color: #f97316;">M</span>
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
