particle_system_code = '''import { DRONE_PATHS, TILE_WIDTH, TILE_HEIGHT } from '../data/cityLayout.js';

export class ParticleSystem {
  constructor() {
    this.packets = [];
    this.drones = [];
    this.smokePuffs = [];
    this.waterRipples = [];
    this.radarAngle = 0;
    this.pulsePhase = 0;

    this.initDrones();
  }

  initDrones() {
    const droneColors = ['#06b6d4', '#f97316', '#ec4899'];
    const droneNames = ['Kaveri Autonomous SDR Drone', 'Claudeforce Co-Pilot Drone', 'Headless MCP Data Courier'];

    DRONE_PATHS.forEach((path, i) => {
      this.drones.push({
        name: droneNames[i] || `Drone-${i + 1}`,
        path: path,
        color: droneColors[i] || '#8b5cf6',
        segmentIndex: 0,
        progress: Math.random(),
        speed: 0.006 + Math.random() * 0.003,
        currentX: path[0].x,
        currentY: path[0].y,
        altitude: 40 + i * 15
      });
    });
  }

  spawnPacket(fromBuilding, toBuilding, color = '#38bdf8', speed = 0.015) {
    if (!fromBuilding || !toBuilding) return;
    this.packets.push({
      fromX: fromBuilding.gridX + fromBuilding.width / 2,
      fromY: fromBuilding.gridY + fromBuilding.height / 2,
      toX: toBuilding.gridX + toBuilding.width / 2,
      toY: toBuilding.gridY + toBuilding.height / 2,
      progress: 0,
      speed: speed,
      color: color,
      size: 4
    });
  }

  update(delta = 16) {
    // Update radar & pulses
    this.radarAngle = (this.radarAngle + 0.04) % (Math.PI * 2);
    this.pulsePhase = (this.pulsePhase + 0.05) % (Math.PI * 2);

    // Update data packets
    for (let i = this.packets.length - 1; i >= 0; i--) {
      const p = this.packets[i];
      p.progress += p.speed;
      if (p.progress >= 1) {
        this.packets.splice(i, 1);
      }
    }

    // Auto-replenish ambient packets if low
    if (this.packets.length < 8 && Math.random() < 0.06) {
      this.spawnAmbientPacket();
    }

    // Update drones
    this.drones.forEach(d => {
      d.progress += d.speed;
      if (d.progress >= 1) {
        d.progress = 0;
        d.segmentIndex = (d.segmentIndex + 1) % d.path.length;
      }
      const p1 = d.path[d.segmentIndex];
      const p2 = d.path[(d.segmentIndex + 1) % d.path.length];
      d.currentX = p1.x + (p2.x - p1.x) * d.progress;
      d.currentY = p1.y + (p2.y - p1.y) * d.progress;
    });

    // Update smoke puffs
    if (Math.random() < 0.08) {
      // Spawn puff from Custom Objects Works (grid: 2, 7)
      this.smokePuffs.push({
        x: 3.0,
        y: 8.0,
        heightOffset: 45,
        radius: 3,
        alpha: 0.7,
        vx: (Math.random() - 0.5) * 0.005,
        vy: -0.01,
        vz: 0.4
      });
    }

    for (let i = this.smokePuffs.length - 1; i >= 0; i--) {
      const sp = this.smokePuffs[i];
      sp.x += sp.vx;
      sp.y += sp.vy;
      sp.heightOffset += sp.vz;
      sp.radius += 0.08;
      sp.alpha -= 0.008;
      if (sp.alpha <= 0) {
        this.smokePuffs.splice(i, 1);
      }
    }
  }

  setBuildings(buildings) {
    this.buildings = buildings;
  }

  spawnAmbientPacket() {
    if (!this.buildings || this.buildings.length < 2) return;
    const b1 = this.buildings[Math.floor(Math.random() * this.buildings.length)];
    if (b1.relationships && b1.relationships.length > 0) {
      const targetId = b1.relationships[Math.floor(Math.random() * b1.relationships.length)];
      const b2 = this.buildings.find(b => b.id === targetId);
      if (b2) {
        this.spawnPacket(b1, b2, b1.color || '#38bdf8', 0.012 + Math.random() * 0.008);
      }
    }
  }
}
'''

with open('/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer/src/engine/ParticleSystem.js', 'w') as f:
    f.write(particle_system_code)

print("ParticleSystem.js written successfully!")
