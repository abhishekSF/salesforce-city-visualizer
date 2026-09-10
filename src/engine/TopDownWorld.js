/**
 * TopDownWorld.js - Handcrafted Retro RPG Town World
 * Features 28x28 tile map, multi-biome terrain, animated water & shoreline,
 * depth-sorted Y-ordered entities (player, trees, props, landmarks),
 * and distinctive architectural artwork for all 17 Salesforce landmarks.
 */

import { GRID_SIZE, generateTileMap } from '../data/cityLayout.js';

export const TILE_SIZE = 40;
export const WORLD_WIDTH = GRID_SIZE * TILE_SIZE; // 1120px
export const WORLD_HEIGHT = GRID_SIZE * TILE_SIZE; // 1120px

export class TopDownWorld {
  constructor(catalog) {
    this.catalog = catalog;
    this.tileMap = generateTileMap();
    this.buildings = [];
    this.props = [];
    this.trees = [];

    this.initBuildings();
    this.initEnvironmentalProps();
  }

  initBuildings() {
    this.buildings = this.catalog.buildings.map(b => {
      const wx = b.gridX * TILE_SIZE;
      const wy = b.gridY * TILE_SIZE;
      const ww = b.width * TILE_SIZE;
      const wh = b.height * TILE_SIZE;

      return {
        ...b,
        worldX: wx,
        worldY: wy,
        worldW: ww,
        worldH: wh,
        // Collision box (occupies lower 60% of building footprint)
        solidX: wx + 4,
        solidY: wy + wh * 0.35,
        solidW: ww - 8,
        solidH: wh * 0.65,
        // Entrance anchor in front of building door
        entranceX: wx + ww / 2,
        entranceY: wy + wh + 12,
        // Y-sort anchor for depth sorting
        sortY: wy + wh
      };
    });
  }

  initEnvironmentalProps() {
    this.props = [];
    this.trees = [];

    // Handcrafted tree locations around districts, parks, and avenues
    const treeCoords = [
      // Metadata Citadel Gardens
      { x: 1, y: 1, type: 'oak' },
      { x: 8, y: 1, type: 'pine' },
      { x: 1, y: 4, type: 'oak' },
      { x: 1, y: 9, type: 'oak' },
      { x: 8, y: 5, type: 'pine' },

      // Automation Grid Industrial Yard
      { x: 9, y: 1, type: 'pine' },
      { x: 16, y: 1, type: 'pine' },
      { x: 16, y: 6, type: 'pine' },

      // Data Cloud Harbor Shoreline
      { x: 17, y: 1, type: 'willow' },
      { x: 17, y: 4, type: 'willow' },
      { x: 25, y: 1, type: 'pine' },
      { x: 26, y: 7, type: 'pine' },

      // Agentforce Central Park / Quad
      { x: 9, y: 10, type: 'cyber' },
      { x: 15, y: 10, type: 'cyber' },
      { x: 9, y: 16, type: 'cyber' },
      { x: 15, y: 16, type: 'cyber' },

      // Claudeforce Observatory Grounds
      { x: 17, y: 10, type: 'oak' },
      { x: 20, y: 12, type: 'oak' },
      { x: 20, y: 15, type: 'pine' },

      // Headless 360 Boulevard
      { x: 1, y: 14, type: 'palm' },
      { x: 8, y: 14, type: 'palm' },
      { x: 1, y: 20, type: 'palm' },
      { x: 8, y: 20, type: 'palm' },

      // MCP Transit Buffer
      { x: 14, y: 18, type: 'pine' },
      { x: 23, y: 18, type: 'pine' },
      { x: 25, y: 22, type: 'pine' },
      { x: 14, y: 24, type: 'pine' }
    ];

    treeCoords.forEach(t => {
      const wx = t.x * TILE_SIZE + 8;
      const wy = t.y * TILE_SIZE + 4;
      this.trees.push({
        type: t.type,
        x: wx,
        y: wy,
        w: 28,
        h: 36,
        sortY: wy + 32
      });
    });

    // Street Lamps & Directional Signposts
    const lampCoords = [
      { x: 4, y: 9 }, { x: 7, y: 9 }, { x: 10, y: 9 }, { x: 13, y: 9 },
      { x: 10, y: 4 }, { x: 10, y: 7 }, { x: 10, y: 14 }, { x: 10, y: 17 },
      { x: 18, y: 9 }, { x: 22, y: 9 }, { x: 4, y: 16 }, { x: 7, y: 16 }
    ];

    lampCoords.forEach(l => {
      const wx = l.x * TILE_SIZE + 16;
      const wy = l.y * TILE_SIZE + 8;
      this.props.push({
        type: 'lamp',
        x: wx,
        y: wy,
        sortY: wy + 26
      });
    });

    // Directional Signposts
    this.props.push({
      type: 'sign',
      x: 10 * TILE_SIZE + 24,
      y: 9 * TILE_SIZE + 12,
      label: 'Citadel / Forum',
      sortY: 9 * TILE_SIZE + 28
    });
    this.props.push({
      type: 'sign',
      x: 18 * TILE_SIZE + 8,
      y: 9 * TILE_SIZE + 12,
      label: 'Data Harbor →',
      sortY: 9 * TILE_SIZE + 28
    });
    this.props.push({
      type: 'sign',
      x: 10 * TILE_SIZE + 24,
      y: 16 * TILE_SIZE + 12,
      label: '← Headless / MCP →',
      sortY: 16 * TILE_SIZE + 28
    });
  }

  isColliding(boxX, boxY, boxW, boxH) {
    // 1. World Bounds
    if (boxX < 0 || boxX + boxW > WORLD_WIDTH || boxY < 0 || boxY + boxH > WORLD_HEIGHT) {
      return true;
    }

    // 2. Tile-based solid check (Water tiles without bridges)
    const startTileX = Math.floor(boxX / TILE_SIZE);
    const endTileX = Math.floor((boxX + boxW) / TILE_SIZE);
    const startTileY = Math.floor(boxY / TILE_SIZE);
    const endTileY = Math.floor((boxY + boxH) / TILE_SIZE);

    for (let ty = startTileY; ty <= endTileY; ty++) {
      for (let tx = startTileX; tx <= endTileX; tx++) {
        if (ty >= 0 && ty < GRID_SIZE && tx >= 0 && tx < GRID_SIZE) {
          const type = this.tileMap[ty][tx];
          // Water tile (type 3) is impassable unless on bridge (y == 5)
          if (type === 3) {
            // Harbor bridge crossing at y = 5
            if (ty === 5) continue;
            return true;
          }
        }
      }
    }

    // 3. Building Footprint Collisions
    for (const b of this.buildings) {
      if (boxX < b.solidX + b.solidW &&
          boxX + boxW > b.solidX &&
          boxY < b.solidY + b.solidH &&
          boxY + boxH > b.solidY) {
        return true;
      }
    }

    return false;
  }

  getNearbyBuilding(playerX, playerY, radius = 42) {
    for (const b of this.buildings) {
      const dist = Math.hypot(playerX - b.entranceX, playerY - b.entranceY);
      if (dist <= radius) {
        return b;
      }
    }
    return null;
  }

  render(ctx, player, viewport, timestamp = 0) {
    // 1. Render Terrain Tiles
    this.renderTerrain(ctx, viewport, timestamp);

    // 2. Collect All Y-Sorted Renderables
    const drawables = [];

    // Add buildings
    this.buildings.forEach(b => {
      drawables.push({
        sortY: b.sortY,
        render: () => this.renderLandmark(ctx, b, timestamp)
      });
    });

    // Add trees
    this.trees.forEach(t => {
      drawables.push({
        sortY: t.sortY,
        render: () => this.renderTree(ctx, t, timestamp)
      });
    });

    // Add street props
    this.props.forEach(p => {
      drawables.push({
        sortY: p.sortY,
        render: () => this.renderProp(ctx, p, timestamp)
      });
    });

    // Add player character
    if (player) {
      drawables.push({
        sortY: player.y,
        render: () => player.render(ctx)
      });
    }

    // 3. Sort Drawables by Y anchor (Depth Sorting!)
    drawables.sort((a, b) => a.sortY - b.sortY);

    // 4. Render Sorted Entities
    drawables.forEach(d => d.render());

    // 5. Render Environmental Overlays (Lamp glow cones & particles)
    this.renderAtmosphericLighting(ctx, viewport, timestamp);

    // 6. Interaction Prompt (if near entrance)
    if (player) {
      const nearby = this.getNearbyBuilding(player.x, player.y);
      if (nearby) {
        this.renderInteractionPrompt(ctx, nearby, timestamp);
      }
    }
  }

  renderTerrain(ctx, vp, timestamp) {
    const minTX = Math.max(0, Math.floor(vp.x / TILE_SIZE) - 1);
    const maxTX = Math.min(GRID_SIZE - 1, Math.ceil((vp.x + vp.width) / TILE_SIZE) + 1);
    const minTY = Math.max(0, Math.floor(vp.y / TILE_SIZE) - 1);
    const maxTY = Math.min(GRID_SIZE - 1, Math.ceil((vp.y + vp.height) / TILE_SIZE) + 1);

    for (let ty = minTY; ty <= maxTY; ty++) {
      for (let tx = minTX; tx <= maxTX; tx++) {
        const type = this.tileMap[ty][tx];
        const px = tx * TILE_SIZE;
        const py = ty * TILE_SIZE;

        if (type === 3) {
          // --- DATA CLOUD HARBOR WATER ---
          const wave = Math.sin(timestamp * 0.003 + (tx + ty) * 0.8) * 4;
          ctx.fillStyle = '#0369a1'; // Deep oceanic blue
          ctx.fillRect(px, py, TILE_SIZE, TILE_SIZE);

          // Lighter water ripples
          ctx.fillStyle = 'rgba(56, 189, 248, 0.4)';
          ctx.fillRect(px + 4, py + 8 + wave, 14, 2);
          ctx.fillRect(px + 20, py + 22 - wave, 12, 2);

          // Shoreline foam on edges bordering non-water
          if (tx > 0 && this.tileMap[ty][tx - 1] !== 3) {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
            ctx.fillRect(px, py, 3, TILE_SIZE);
          }
          if (ty < GRID_SIZE - 1 && this.tileMap[ty + 1][tx] !== 3) {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
            ctx.fillRect(px, py + TILE_SIZE - 3, TILE_SIZE, 3);
          }
        } else if (type === 1 || type === 2) {
          // --- PAVED TRANSIT AVENUE ---
          ctx.fillStyle = '#1e293b'; // Slate asphalt
          ctx.fillRect(px, py, TILE_SIZE, TILE_SIZE);

          // Curbs
          ctx.fillStyle = '#475569';
          ctx.fillRect(px, py, TILE_SIZE, 2);
          ctx.fillRect(px, py + TILE_SIZE - 2, TILE_SIZE, 2);

          // Road markings / Fiber-optic conduit strip
          if (type === 2) {
            const glow = (Math.sin(timestamp * 0.005 + tx) + 1) / 2;
            ctx.fillStyle = `rgba(56, 189, 248, ${0.4 + glow * 0.4})`;
            ctx.fillRect(px, py + TILE_SIZE / 2 - 1.5, TILE_SIZE, 3);
          } else {
            // Broken white centerline
            if (tx % 2 === 0 || ty % 2 === 0) {
              ctx.fillStyle = 'rgba(255, 255, 255, 0.25)';
              ctx.fillRect(px + 6, py + TILE_SIZE / 2 - 1, 14, 2);
            }
          }
        } else if (type === 5) {
          // --- AGENTFORCE CENTRAL PLAZA ---
          ctx.fillStyle = '#1e1b4b'; // Deep violet stone
          ctx.fillRect(px, py, TILE_SIZE, TILE_SIZE);

          // Geometric tile pattern
          ctx.strokeStyle = 'rgba(168, 85, 247, 0.25)';
          ctx.lineWidth = 1;
          ctx.strokeRect(px + 2, py + 2, TILE_SIZE - 4, TILE_SIZE - 4);
        } else if (type === 6) {
          // --- MAGLEV TRANSIT TRACK ---
          ctx.fillStyle = '#18181b';
          ctx.fillRect(px, py, TILE_SIZE, TILE_SIZE);

          // Sleepers
          ctx.fillStyle = '#3f3f46';
          ctx.fillRect(px + 4, py + 4, TILE_SIZE - 8, 3);
          ctx.fillRect(px + 4, py + 18, TILE_SIZE - 8, 3);
          ctx.fillRect(px + 4, py + 32, TILE_SIZE - 8, 3);

          // Glowing Magenta Power Rail
          ctx.fillStyle = '#ec4899';
          ctx.fillRect(px + 8, py, 3, TILE_SIZE);
          ctx.fillRect(px + TILE_SIZE - 11, py, 3, TILE_SIZE);
        } else {
          // --- LUSH COUNTRYSIDE / TOWN TURF ---
          // Varied grass tones based on coordinates
          const isLighter = (tx * 7 + ty * 13) % 5 === 0;
          ctx.fillStyle = isLighter ? '#14532d' : '#166534'; // Rich RPG green
          ctx.fillRect(px, py, TILE_SIZE, TILE_SIZE);

          // Subtle grass blade specks
          if ((tx + ty) % 3 === 0) {
            ctx.fillStyle = '#22c55e';
            ctx.fillRect(px + 8, py + 12, 2, 3);
            ctx.fillRect(px + 10, py + 11, 2, 4);
          }
          // Tiny wildflower dots
          if ((tx * 3 + ty * 7) % 11 === 0) {
            ctx.fillStyle = (tx % 2 === 0) ? '#fbbf24' : '#f472b6';
            ctx.fillRect(px + 24, py + 20, 2.5, 2.5);
          }
        }
      }
    }

    // Canal Bridge crossing water at y = 5, x in [18..27]
    const bridgeY = 5 * TILE_SIZE;
    ctx.fillStyle = '#334155'; // Stone bridge deck
    ctx.fillRect(18 * TILE_SIZE, bridgeY, 9 * TILE_SIZE, TILE_SIZE);
    // Stone balustrade railings
    ctx.fillStyle = '#64748b';
    ctx.fillRect(18 * TILE_SIZE, bridgeY, 9 * TILE_SIZE, 4);
    ctx.fillRect(18 * TILE_SIZE, bridgeY + TILE_SIZE - 4, 9 * TILE_SIZE, 4);
  }

  renderTree(ctx, t, timestamp) {
    const { x, y, type } = t;

    ctx.save();
    // Tree ground shadow
    ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
    ctx.beginPath();
    ctx.ellipse(x + 14, y + 30, 14, 6, 0, 0, Math.PI * 2);
    ctx.fill();

    // Trunk
    ctx.fillStyle = '#78350f';
    ctx.fillRect(x + 11, y + 16, 6, 16);

    if (type === 'pine') {
      // Pine Needle Triangles
      ctx.fillStyle = '#064e3b';
      ctx.beginPath();
      ctx.moveTo(x + 14, y - 10);
      ctx.lineTo(x + 28, y + 10);
      ctx.lineTo(x, y + 10);
      ctx.closePath();
      ctx.fill();

      ctx.fillStyle = '#047857';
      ctx.beginPath();
      ctx.moveTo(x + 14, y - 2);
      ctx.lineTo(x + 26, y + 18);
      ctx.lineTo(x + 2, y + 18);
      ctx.closePath();
      ctx.fill();
    } else if (type === 'cyber') {
      // Agentforce Glowing Hologram Tree
      const pulse = Math.sin(timestamp * 0.004 + x) * 2;
      ctx.fillStyle = 'rgba(168, 85, 247, 0.85)';
      ctx.beginPath();
      ctx.arc(x + 14, y + 6, 16 + pulse, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#f3e8ff';
      ctx.beginPath();
      ctx.arc(x + 14, y + 6, 8, 0, Math.PI * 2);
      ctx.fill();
    } else {
      // Oak Canopy
      ctx.fillStyle = '#15803d';
      ctx.beginPath();
      ctx.arc(x + 14, y + 8, 15, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#22c55e';
      ctx.beginPath();
      ctx.arc(x + 10, y + 4, 8, 0, Math.PI * 2);
      ctx.arc(x + 18, y + 6, 7, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }

  renderProp(ctx, p, timestamp) {
    if (p.type === 'lamp') {
      // Victorian Street Lamp Post
      ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
      ctx.beginPath();
      ctx.ellipse(p.x, p.y + 24, 6, 3, 0, 0, Math.PI * 2);
      ctx.fill();

      // Iron Post
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(p.x - 1.5, p.y, 3, 24);
      // Lamp Head
      ctx.fillStyle = '#f59e0b';
      ctx.fillRect(p.x - 4, p.y - 4, 8, 6);
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(p.x - 2, p.y - 2, 4, 3);
    } else if (p.type === 'sign') {
      // Wooden Signpost
      ctx.fillStyle = '#78350f';
      ctx.fillRect(p.x - 2, p.y, 4, 20);
      ctx.fillStyle = '#b45309';
      ctx.fillRect(p.x - 18, p.y - 8, 36, 12);
      ctx.strokeStyle = '#451a03';
      ctx.lineWidth = 1;
      ctx.strokeRect(p.x - 18, p.y - 8, 36, 12);

      ctx.fillStyle = '#fef3c7';
      ctx.font = '600 7px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(p.label, p.x, p.y);
    }
  }

  renderLandmark(ctx, b, timestamp) {
    const { worldX: x, worldY: y, worldW: w, worldH: h } = b;

    ctx.save();

    // 1. Building Drop Shadow
    ctx.fillStyle = 'rgba(0, 0, 0, 0.45)';
    ctx.beginPath();
    ctx.roundRect(x + 6, y + h - 8, w - 4, 14, 4);
    ctx.fill();

    // 2. Custom Handcrafted Silhouette by Building ID
    if (b.id === 'b_standard_objects') {
      // === STANDARD OBJECTS TOWER (Grand Civic Archive) ===
      // Main Stone Wall
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(x, y + 16, w, h - 16);

      // Pitched Slate Mansard Roof
      ctx.fillStyle = '#0f172a';
      ctx.beginPath();
      ctx.moveTo(x - 4, y + 18);
      ctx.lineTo(x + w / 2, y - 12);
      ctx.lineTo(x + w + 4, y + 18);
      ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Arched Library Windows with warm interior light
      ctx.fillStyle = '#fef08a';
      ctx.fillRect(x + 10, y + 26, 12, 16);
      ctx.fillRect(x + w - 22, y + 26, 12, 16);

      // Grand Brass Double Doors
      ctx.fillStyle = '#b45309';
      ctx.fillRect(x + w / 2 - 10, y + h - 22, 20, 22);
      ctx.strokeStyle = '#f59e0b';
      ctx.strokeRect(x + w / 2 - 10, y + h - 22, 20, 22);

      // Bronze Plaque
      ctx.fillStyle = '#38bdf8';
      ctx.font = '700 8px JetBrains Mono, monospace';
      ctx.textAlign = 'center';
      ctx.fillText('METADATA', x + w / 2, y + 12);

    } else if (b.id === 'b_security_fortress') {
      // === SECURITY CITADEL (Fortress Keep) ===
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(x, y + 10, w, h - 10);

      // Crenellated Battlements
      for (let cx = x; cx < x + w; cx += 16) {
        ctx.fillRect(cx, y + 2, 10, 8);
      }
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 1.5;
      ctx.strokeRect(x, y + 10, w, h - 10);

      // Iron Portcullis Gate
      ctx.fillStyle = '#0284c7';
      ctx.fillRect(x + w / 2 - 12, y + h - 24, 24, 24);
      // Gate Grates
      ctx.strokeStyle = '#0369a1';
      ctx.lineWidth = 1.5;
      ctx.strokeRect(x + w / 2 - 12, y + h - 24, 24, 24);

      // Guard Lights
      ctx.fillStyle = '#38bdf8';
      ctx.beginPath();
      ctx.arc(x + 10, y + 18, 3, 0, Math.PI * 2);
      ctx.arc(x + w - 10, y + 18, 3, 0, Math.PI * 2);
      ctx.fill();

    } else if (b.id === 'b_apex_foundry') {
      // === APEX FOUNDRY (Industrial Forge) ===
      ctx.fillStyle = '#7f1d1d'; // Deep Foundry Brick
      ctx.fillRect(x, y + 12, w, h - 12);

      // Corrugated Metal Roof
      ctx.fillStyle = '#450a0a';
      ctx.fillRect(x - 2, y + 6, w + 4, 10);

      // Brick Smokestack Chimney with animated smoke puffs
      ctx.fillStyle = '#991b1b';
      ctx.fillRect(x + w - 16, y - 18, 12, 28);
      // Smoke puff
      const puffY = (timestamp * 0.02) % 20;
      ctx.fillStyle = 'rgba(203, 213, 225, 0.4)';
      ctx.beginPath();
      ctx.arc(x + w - 10, y - 22 - puffY, 5 + puffY * 0.3, 0, Math.PI * 2);
      ctx.fill();

      // Glowing Blast Furnace Aperture
      const glow = Math.sin(timestamp * 0.006) * 0.2;
      ctx.fillStyle = `rgba(249, 115, 22, ${0.8 + glow})`;
      ctx.fillRect(x + 12, y + 26, 18, 14);

      // Heavy Iron Double Doors
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(x + w / 2 - 10, y + h - 20, 20, 20);

    } else if (b.id === 'b_flow_powerhouse') {
      // === FLOW HYDRO-AUTOMATION PLANT ===
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(x, y + 14, w, h - 14);

      // Turning Hydro Paddle Wheel on side
      const angle = timestamp * 0.003;
      const wx = x - 6;
      const wy = y + h - 16;
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(wx, wy, 10, 0, Math.PI * 2);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(wx + Math.cos(angle) * 10, wy + Math.sin(angle) * 10);
      ctx.lineTo(wx - Math.cos(angle) * 10, wy - Math.sin(angle) * 10);
      ctx.stroke();

      // Copper Steam Pipes across facade
      ctx.fillStyle = '#b45309';
      ctx.fillRect(x + 8, y + 10, w - 16, 4);

      // Entrance
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(x + w / 2 - 9, y + h - 18, 18, 18);

    } else if (b.id === 'b_calculated_insights') {
      // === CALCULATED INSIGHTS LIGHTHOUSE ===
      // Tapered Lighthouse Tower
      ctx.fillStyle = '#f1f5f9';
      ctx.beginPath();
      ctx.moveTo(x + 16, y + h);
      ctx.lineTo(x + w - 16, y + h);
      ctx.lineTo(x + w - 20, y);
      ctx.lineTo(x + 20, y);
      ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = '#06b6d4';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Red Nautical Stripes
      ctx.fillStyle = '#06b6d4';
      ctx.fillRect(x + 18, y + 20, w - 36, 12);
      ctx.fillRect(x + 19, y + 42, w - 38, 12);

      // Lantern Room on top
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(x + w / 2 - 12, y - 10, 24, 12);
      ctx.fillStyle = '#38bdf8';
      ctx.fillRect(x + w / 2 - 8, y - 8, 16, 8);

      // Rotating 360° Searchlight Beam
      const beamAngle = timestamp * 0.0025;
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(x + w / 2, y - 4);
      ctx.arc(x + w / 2, y - 4, 100, beamAngle - 0.2, beamAngle + 0.2);
      ctx.closePath();
      ctx.fillStyle = 'rgba(6, 182, 212, 0.18)';
      ctx.fill();
      ctx.restore();

      // Door
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(x + w / 2 - 6, y + h - 14, 12, 14);

    } else if (b.id === 'b_data_lake') {
      // === DATA LAKE RESERVOIR (Stone Embankment & Floodgate) ===
      ctx.fillStyle = '#0e7490';
      ctx.fillRect(x, y + 8, w, h - 8);

      // Churning water in reservoir pool
      ctx.fillStyle = '#06b6d4';
      ctx.fillRect(x + 6, y + 14, w - 12, h - 24);

      // Sluice gates
      ctx.fillStyle = '#155e75';
      ctx.fillRect(x + 14, y + h - 14, 14, 14);
      ctx.fillRect(x + w - 28, y + h - 14, 14, 14);

    } else if (b.id === 'b_agentforce_core') {
      // === ATLAS REASONING ENGINE SPIRE ===
      // Futuristic Cylindrical Rotunda
      ctx.fillStyle = '#2e1065'; // Dark Imperial Violet
      ctx.fillRect(x, y + 16, w, h - 16);
      ctx.strokeStyle = '#c084fc';
      ctx.lineWidth = 2;
      ctx.strokeRect(x, y + 16, w, h - 16);

      // Glass Dome
      ctx.fillStyle = 'rgba(168, 85, 247, 0.3)';
      ctx.beginPath();
      ctx.arc(x + w / 2, y + 16, w / 2 - 4, Math.PI, 0);
      ctx.fill();
      ctx.strokeStyle = '#a855f7';
      ctx.stroke();

      // Floating Pulsing Violet Atlas Core
      const coreBob = Math.sin(timestamp * 0.005) * 3;
      const corePulse = Math.sin(timestamp * 0.008) * 3;
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(x + w / 2, y - 4 + coreBob, 10 + corePulse, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#a855f7';
      ctx.beginPath();
      ctx.arc(x + w / 2, y - 4 + coreBob, 6, 0, Math.PI * 2);
      ctx.fill();

      // Orbital Rings
      ctx.beginPath();
      ctx.ellipse(x + w / 2, y - 4 + coreBob, 20, 7, timestamp * 0.002, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(0, 240, 255, 0.8)';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Entrance Portico
      ctx.fillStyle = '#581c87';
      ctx.fillRect(x + w / 2 - 12, y + h - 22, 24, 22);

    } else if (b.id === 'b_claudeforce_lab') {
      // === CLAUDE 3.5 COGNITIVE OBSERVATORY ===
      ctx.fillStyle = '#1c1917'; // Rich scholarly granite
      ctx.fillRect(x, y + 14, w, h - 14);

      // Classical Copper Observatory Dome (patinated green-copper)
      ctx.fillStyle = '#059669';
      ctx.beginPath();
      ctx.arc(x + w / 2, y + 14, w / 2 - 6, Math.PI, 0);
      ctx.fill();
      ctx.strokeStyle = '#f97316';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Brass Telescope extending from dome slot
      const tAngle = timestamp * 0.025;
      ctx.strokeStyle = '#d97706';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(x + w / 2, y + 14);
      ctx.lineTo(x + w / 2 + Math.cos(tAngle) * 22, y + 14 + Math.sin(tAngle) * 10 - 10);
      ctx.stroke();

      // Arched Entrance & Library Windows
      ctx.fillStyle = '#fb923c';
      ctx.fillRect(x + 8, y + 24, 10, 14);
      ctx.fillRect(x + w - 18, y + 24, 10, 14);
      ctx.fillStyle = '#292524';
      ctx.fillRect(x + w / 2 - 10, y + h - 18, 20, 18);

    } else if (b.id === 'b_headless_gateway') {
      // === HEADLESS 360 SKYPORT GATEWAY ===
      ctx.fillStyle = '#064e3b';
      ctx.fillRect(x, y + 12, w, h - 12);

      // Cantilevered Aerospace Departure Deck
      ctx.fillStyle = '#10b981';
      ctx.fillRect(x - 4, y + 4, w + 8, 10);

      // Labeled 'HXL' on canopy
      ctx.fillStyle = '#ffffff';
      ctx.font = '700 8px JetBrains Mono, monospace';
      ctx.textAlign = 'center';
      ctx.fillText('HEADLESS 360', x + w / 2, y + 12);

      // Runway Guidance Strobes
      const strobe = Math.sin(timestamp * 0.01) > 0;
      ctx.fillStyle = strobe ? '#34d399' : '#047857';
      ctx.fillRect(x + 4, y + h - 4, 6, 4);
      ctx.fillRect(x + w - 10, y + h - 4, 6, 4);

      // Glass Sliding Doors
      ctx.fillStyle = 'rgba(56, 189, 248, 0.6)';
      ctx.fillRect(x + w / 2 - 12, y + h - 20, 24, 20);

    } else if (b.id.startsWith('b_mcp')) {
      // === DUAL-PLANE MCP SERVERS ===
      const isPlane1 = b.id === 'b_mcp_context';
      ctx.fillStyle = '#18181b';
      ctx.fillRect(x, y + 10, w, h - 10);

      // Terminal Antenna & Switching Box
      ctx.fillStyle = isPlane1 ? '#0284c7' : '#db2777';
      ctx.fillRect(x + 4, y + 4, w - 8, 8);

      // Glowing Server Rack Bank Windows
      ctx.fillStyle = isPlane1 ? '#38bdf8' : '#ec4899';
      ctx.fillRect(x + 8, y + 18, 12, 10);
      ctx.fillRect(x + w - 20, y + 18, 12, 10);

      // Protocol Label
      ctx.fillStyle = '#ffffff';
      ctx.font = '700 7px JetBrains Mono, monospace';
      ctx.textAlign = 'center';
      ctx.fillText(isPlane1 ? 'MCP: CONTEXT' : 'MCP: ACTION', x + w / 2, y + 10);

      // Transit Access Door
      ctx.fillStyle = '#27272a';
      ctx.fillRect(x + w / 2 - 9, y + h - 16, 18, 16);

    } else {
      // Default High-Quality Modular Landmark
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(x, y + 12, w, h - 12);
      ctx.fillStyle = b.color || '#38bdf8';
      ctx.fillRect(x + 2, y + 4, w - 4, 10);
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1;
      ctx.strokeRect(x, y + 12, w, h - 12);

      // Door
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(x + w / 2 - 8, y + h - 16, 16, 16);
    }

    // 3. Entrance Indicator (Door Mat)
    ctx.fillStyle = 'rgba(56, 189, 248, 0.4)';
    ctx.fillRect(b.entranceX - 8, b.entranceY - 6, 16, 4);

    // 4. District Pill Badge
    ctx.fillStyle = 'rgba(10, 15, 26, 0.85)';
    ctx.strokeStyle = b.color || '#38bdf8';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(x + 4, y - 8, w - 8, 14, 4);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#ffffff';
    ctx.font = '600 8px Plus Jakarta Sans, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(b.name.split(' ')[0], x + w / 2, y - 1);

    ctx.restore();
  }

  renderAtmosphericLighting(ctx, vp, timestamp) {
    // Warm light pools under street lamps
    this.props.filter(p => p.type === 'lamp').forEach(p => {
      const grad = ctx.createRadialGradient(p.x, p.y + 20, 2, p.x, p.y + 20, 36);
      grad.addColorStop(0, 'rgba(251, 191, 36, 0.15)');
      grad.addColorStop(1, 'rgba(251, 191, 36, 0)');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(p.x, p.y + 20, 36, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  renderInteractionPrompt(ctx, b, timestamp) {
    const bob = Math.sin(timestamp * 0.008) * 3;
    const px = b.entranceX;
    const py = b.entranceY - 26 + bob;

    ctx.save();
    ctx.fillStyle = 'rgba(10, 15, 26, 0.95)';
    ctx.strokeStyle = '#00f0ff';
    ctx.lineWidth = 1.5;

    const w = 90;
    const h = 20;
    ctx.beginPath();
    ctx.roundRect(px - w / 2, py - h / 2, w, h, 6);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#ffffff';
    ctx.font = '700 9px JetBrains Mono, monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('[E] INSPECT', px, py);
    ctx.restore();
  }
}
