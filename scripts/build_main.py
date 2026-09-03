main_code = '''import { METADATA_CATALOG } from './data/metadataCatalog.js';
import { ParticleSystem } from './engine/ParticleSystem.js';
import { IsometricCanvas } from './engine/IsometricCanvas.js';
import { BuildingInspector } from './components/BuildingInspector.js';
import { ConceptModal } from './components/ConceptModal.js';
import { sfx } from './engine/SoundFx.js';

document.addEventListener('DOMContentLoaded', () => {
  const canvasEl = document.getElementById('city-canvas');
  const inspectorContainer = document.getElementById('building-inspector');
  const modalContainer = document.getElementById('concept-modal');

  const particleSystem = new ParticleSystem();
  const isoCanvas = new IsometricCanvas(canvasEl, METADATA_CATALOG, particleSystem);

  const inspector = new BuildingInspector(inspectorContainer, (building) => {
    handleBuildingAction(building, isoCanvas, particleSystem);
  });

  const conceptModal = new ConceptModal(modalContainer);

  // Hook canvas building selection to inspector
  isoCanvas.onBuildingSelected = (building) => {
    inspector.show(building);
  };

  // Wire up Layer Filter buttons
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => {
        b.classList.remove('bg-sky-600', 'text-white', 'border-sky-400');
        b.classList.add('bg-slate-800', 'text-slate-300', 'border-slate-700');
      });
      btn.classList.remove('bg-slate-800', 'text-slate-300', 'border-slate-700');
      btn.classList.add('bg-sky-600', 'text-white', 'border-sky-400');

      const filter = btn.dataset.filter;
      isoCanvas.activeFilter = filter;
      sfx.districtSelect();
    });
  });

  // Wire up Top Bar Controls
  document.getElementById('btn-open-academy').addEventListener('click', () => {
    conceptModal.show('headless360');
  });

  document.getElementById('btn-run-simulation').addEventListener('click', () => {
    runFullSimulation(METADATA_CATALOG.simulations[0], isoCanvas, particleSystem);
  });

  document.getElementById('btn-toggle-sound').addEventListener('click', (e) => {
    const isMuted = sfx.toggleMute();
    e.target.innerHTML = isMuted ? '🔇 Muted' : '🔊 Sound FX';
  });

  document.getElementById('btn-toggle-night').addEventListener('click', (e) => {
    isoCanvas.isNightMode = !isoCanvas.isNightMode;
    e.target.innerHTML = isoCanvas.isNightMode ? '🌙 Cyber Night' : '☀️ Retro Day';
    sfx.click();
  });

  document.getElementById('btn-center-camera').addEventListener('click', () => {
    isoCanvas.centerCamera();
    sfx.click();
  });

  // Quick District Jump buttons in bottom bar
  document.querySelectorAll('.district-jump-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetBuildingId = btn.dataset.target;
      isoCanvas.focusBuilding(targetBuildingId);
      const b = METADATA_CATALOG.buildings.find(item => item.id === targetBuildingId);
      if (b) inspector.show(b);
    });
  });

  // Keyboard navigation
  window.addEventListener('keydown', (e) => {
    if (e.key === ' ' && !modalContainer.classList.contains('hidden')) {
      conceptModal.hide();
    } else if (e.key === 'c' || e.key === 'C') {
      isoCanvas.centerCamera();
    } else if (e.key === 'm' || e.key === 'M') {
      const isMuted = sfx.toggleMute();
      const soundBtn = document.getElementById('btn-toggle-sound');
      if (soundBtn) soundBtn.innerHTML = isMuted ? '🔇 Muted' : '🔊 Sound FX';
    }
  });

  // Main Render Loop
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

function handleBuildingAction(building, isoCanvas, particleSystem) {
  sfx.simulationStep();
  const consoleEl = document.getElementById('action-console-log');
  if (!consoleEl) return;

  consoleEl.innerHTML = `<div class=\"text-sky-400 font-bold\">⚡ Initiating action from ${building.name}...</div>`;

  // Spawn packets to all related buildings
  if (building.relationships && building.relationships.length > 0) {
    building.relationships.forEach((relId, idx) => {
      const targetB = isoCanvas.buildings.find(b => b.id === relId);
      if (targetB) {
        setTimeout(() => {
          particleSystem.spawnPacket(building, targetB, building.color || '#38bdf8', 0.02);
          sfx.pulse();
          consoleEl.innerHTML += `
            <div class=\"text-slate-300\">→ Dispatched packet to <span class=\"text-emerald-400 font-bold\">${targetB.name}</span></div>
          `;
        }, idx * 250);
      }
    });

    setTimeout(() => {
      consoleEl.innerHTML += `<div class=\"text-emerald-400 font-bold mt-1\">✓ Action completed: state synchronized across org!</div>`;
    }, building.relationships.length * 250 + 100);
  } else {
    consoleEl.innerHTML += `<div class=\"text-slate-400\">No outbound relationships configured.</div>`;
  }
}

function runFullSimulation(sim, isoCanvas, particleSystem) {
  sfx.simulationStep();
  const banner = document.getElementById('sim-banner');
  const bannerTitle = document.getElementById('sim-banner-title');
  const bannerDetail = document.getElementById('sim-banner-detail');

  if (!banner) return;
  banner.classList.remove('hidden');

  let currentStep = 0;

  function executeStep() {
    if (currentStep >= sim.steps.length) {
      bannerTitle.innerHTML = '🎉 SIMULATION COMPLETE: Rescue Protocol Governed & Dispatched!';
      bannerDetail.innerHTML = 'All steps verified across Data 360, Atlas Reasoning Engine, Headless 360, and Slack HXL.';
      setTimeout(() => {
        banner.classList.add('hidden');
      }, 5000);
      return;
    }

    const step = sim.steps[currentStep];
    bannerTitle.innerHTML = `[Step ${currentStep + 1}/${sim.steps.length}] ${step.action}`;
    bannerDetail.innerHTML = step.detail;

    const b = isoCanvas.buildings.find(item => item.id === step.buildingId);
    if (b) {
      isoCanvas.focusBuilding(b.id);
      sfx.pulse();

      // Trigger packet to next building in flow if available
      if (currentStep + 1 < sim.steps.length) {
        const nextB = isoCanvas.buildings.find(item => item.id === sim.steps[currentStep + 1].buildingId);
        if (nextB) {
          particleSystem.spawnPacket(b, nextB, '#facc15', 0.025);
        }
      }
    }

    currentStep++;
    setTimeout(executeStep, 2800);
  }

  executeStep();
}
'''

with open('/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer/src/main.js', 'w') as f:
    f.write(main_code)

print("main.js written successfully!")
