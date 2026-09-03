canvas_code = '''import { TILE_WIDTH, TILE_HEIGHT, GRID_SIZE, generateTileMap } from '../data/cityLayout.js';
import { sfx } from './SoundFx.js';

export class IsometricCanvas {
  constructor(canvas, catalog, particleSystem) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.catalog = catalog;
    this.particleSystem = particleSystem;
    this.particleSystem.setBuildings(catalog.buildings);

    this.tileMap = generateTileMap();
    this.buildings = catalog.buildings;
    this.conduits = catalog.conduits;

    // Camera state with smooth lerping
    this.camera = {
      x: 0,
      y: 0,
      targetX: 0,
      targetY: 0,
      zoom: 1.0,
      targetZoom: 1.0,
      isDragging: false,
      dragStartX: 0,
      dragStartY: 0,
      camStartX: 0,
      camStartY: 0
    };

    // Interaction & animation state
    this.hoveredBuilding = null;
    this.selectedBuilding = null;
    this.activeFilter = 'all';
    this.isNightMode = true;
    this.vehicles = [];

    this.initVehicles();
    this.initCanvasSize();
    this.centerCamera(true);
    this.bindEvents();
  }

  initVehicles() {
    // Road vehicles (hovercars moving along roads)
    const roadCoords = [
      { startX: 0, startY: 10, endX: 27, endY: 10, color: '#38bdf8' },
      { startX: 27, startY: 11, endX: 0, endY: 11, color: '#f59e0b' },
      { startX: 10, startY: 0, endX: 10, endY: 27, color: '#10b981' },
      { startX: 11, startY: 27, endX: 11, endY: 0, color: '#ec4899' },
      { startX: 0, startY: 5, endX: 17, endY: 5, color: '#38bdf8' },
      { startX: 5, startY: 0, endX: 5, endY: 27, color: '#a855f7' }
    ];

    roadCoords.forEach((r, idx) => {
      this.vehicles.push({
        ...r,
        progress: (idx * 0.22) % 1,
        speed: 0.0018 + Math.random() * 0.001
      });
    });
  }

  initCanvasSize() {
    const dpr = window.devicePixelRatio || 1;
    const rect = this.canvas.getBoundingClientRect();
    const w = rect.width > 50 ? rect.width : (window.innerWidth || 1200);
    const h = rect.height > 50 ? rect.height : (window.innerHeight || 800);
    this.canvas.width = w * dpr;
    this.canvas.height = h * dpr;
    this.ctx.setTransform(1, 0, 0, 1, 0, 0);
    this.ctx.scale(dpr, dpr);
    this.width = w;
    this.height = h;
  }

  centerCamera(immediate = false) {
    const centerScreen = this.gridToScreen(13, 13);
    const targetX = this.width / 2 - centerScreen.x * this.camera.targetZoom;
    const targetY = this.height / 2 - (centerScreen.y - 120) * this.camera.targetZoom;

    this.camera.targetX = targetX;
    this.camera.targetY = targetY;

    if (immediate) {
      this.camera.x = targetX;
      this.camera.y = targetY;
      this.camera.zoom = this.camera.targetZoom;
    }
  }

  focusBuilding(buildingId) {
    const b = this.buildings.find(item => item.id === buildingId);
    if (!b) return;
    this.selectedBuilding = b;
    const pos = this.gridToScreen(b.gridX + b.width / 2, b.gridY + b.height / 2);
    this.camera.targetX = this.width / 2 - pos.x * this.camera.targetZoom;
    this.camera.targetY = this.height / 2 - (pos.y - b.floors * 1.4) * this.camera.targetZoom;
    sfx.buildingSelect();
  }

  gridToScreen(gx, gy) {
    return {
      x: (gx - gy) * (TILE_WIDTH / 2),
      y: (gx + gy) * (TILE_HEIGHT / 2)
    };
  }

  screenToGrid(sx, sy) {
    const worldX = (sx - this.camera.x) / this.camera.zoom;
    const worldY = (sy - this.camera.y) / this.camera.zoom;
    const gx = (worldX / (TILE_WIDTH / 2) + worldY / (TILE_HEIGHT / 2)) / 2;
    const gy = (worldY / (TILE_HEIGHT / 2) - worldX / (TILE_WIDTH / 2)) / 2;
    return { gx, gy };
  }

  bindEvents() {
    window.addEventListener('resize', () => this.initCanvasSize());

    this.canvas.addEventListener('mousedown', (e) => {
      this.camera.isDragging = true;
      this.camera.dragStartX = e.clientX;
      this.camera.dragStartY = e.clientY;
      this.camera.camStartX = this.camera.x;
      this.camera.camStartY = this.camera.y;
    });

    window.addEventListener('mousemove', (e) => {
      if (this.camera.isDragging) {
        const dx = e.clientX - this.camera.dragStartX;
        const dy = e.clientY - this.camera.dragStartY;
        this.camera.x = this.camera.camStartX + dx;
        this.camera.y = this.camera.camStartY + dy;
        this.camera.targetX = this.camera.x;
        this.camera.targetY = this.camera.y;
      } else {
        const rect = this.canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        this.checkHover(mx, my);
      }
    });

    window.addEventListener('mouseup', (e) => {
      if (this.camera.isDragging) {
        const dist = Math.hypot(e.clientX - this.camera.dragStartX, e.clientY - this.camera.dragStartY);
        this.camera.isDragging = false;
        if (dist < 5) {
          const rect = this.canvas.getBoundingClientRect();
          const mx = e.clientX - rect.left;
          const my = e.clientY - rect.top;
          this.handleClick(mx, my);
        }
      }
    });

    this.canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
      const newZoom = Math.max(0.45, Math.min(2.4, this.camera.targetZoom * zoomFactor));

      const rect = this.canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;

      this.camera.targetX = mx - (mx - this.camera.x) * (newZoom / this.camera.zoom);
      this.camera.targetY = my - (my - this.camera.y) * (newZoom / this.camera.zoom);
      this.camera.targetZoom = newZoom;
    }, { passive: false });
  }

  checkHover(mx, my) {
    let found = null;
    const sorted = [...this.buildings].sort((a, b) => {
      return (b.gridX + b.width + b.gridY + b.height) - (a.gridX + a.width + a.gridY + a.height);
    });

    for (const b of sorted) {
      const p = this.gridToScreen(b.gridX + b.width / 2, b.gridY + b.height / 2);
      const sx = this.camera.x + p.x * this.camera.zoom;
      const sy = this.camera.y + (p.y - b.floors * 1.2) * this.camera.zoom;
      const bW = (b.width * TILE_WIDTH) * this.camera.zoom * 0.9;
      const bH = (b.height * TILE_HEIGHT + b.floors * 2.2) * this.camera.zoom;

      if (mx >= sx - bW / 2 && mx <= sx + bW / 2 && my >= sy - bH * 0.4 && my <= sy + bH * 0.7) {
        found = b;
        break;
      }
    }

    if (found !== this.hoveredBuilding) {
      this.hoveredBuilding = found;
      this.canvas.style.cursor = found ? 'pointer' : 'grab';
      if (found) sfx.click();
    }
  }

  handleClick(mx, my) {
    if (this.hoveredBuilding) {
      this.selectedBuilding = this.hoveredBuilding;
      sfx.buildingSelect();
      if (this.onBuildingSelected) {
        this.onBuildingSelected(this.hoveredBuilding);
      }
    }
  }

  update(delta) {
    // Camera smooth lerp
    this.camera.x += (this.camera.targetX - this.camera.x) * 0.12;
    this.camera.y += (this.camera.targetY - this.camera.y) * 0.12;
    this.camera.zoom += (this.camera.targetZoom - this.camera.zoom) * 0.12;

    // Update road vehicles
    this.vehicles.forEach(v => {
      v.progress = (v.progress + v.speed) % 1;
    });
  }

  render(timestamp = 0) {
    const ctx = this.ctx;
    this.update(16);

    // Clean background fill
    ctx.fillStyle = this.isNightMode ? '#050811' : '#f1f5f9';
    ctx.fillRect(0, 0, this.width, this.height);

    ctx.save();
    ctx.translate(this.camera.x, this.camera.y);
    ctx.scale(this.camera.zoom, this.camera.zoom);

    // 1. Render Ground Terrain Tiles
    this.renderGround(ctx, timestamp);

    // 2. Render Road Traffic & Conduits
    this.renderRoadTraffic(ctx, timestamp);
    this.renderConduits(ctx, timestamp);

    // 3. Render 2.5D Buildings (Depth-Sorted)
    this.renderBuildings(ctx, timestamp);

    // 4. Render Airborne Particles, Drones & Beams
    this.renderParticlesAndDrones(ctx, timestamp);

    // 5. Render 3D Floating District Badges
    this.renderDistrictHolograms(ctx, timestamp);

    ctx.restore();

    // 6. On-screen Hover Badge
    if (this.hoveredBuilding) {
      this.renderFloatingBadge(ctx, this.hoveredBuilding);
    }
  }

  renderGround(ctx, timestamp) {
    for (let y = 0; y < GRID_SIZE; y++) {
      for (let x = 0; x < GRID_SIZE; x++) {
        const type = this.tileMap[y][x];
        const { x: sx, y: sy } = this.gridToScreen(x, y);

        // Viewport culling
        const screenPx = this.camera.x + sx * this.camera.zoom;
        const screenPy = this.camera.y + sy * this.camera.zoom;
        if (screenPx < -120 || screenPx > this.width + 120 || screenPy < -120 || screenPy > this.height + 120) {
          continue;
        }

        ctx.save();
        ctx.translate(sx, sy);

        ctx.beginPath();
        ctx.moveTo(0, -TILE_HEIGHT / 2);
        ctx.lineTo(TILE_WIDTH / 2, 0);
        ctx.lineTo(0, TILE_HEIGHT / 2);
        ctx.lineTo(-TILE_WIDTH / 2, 0);
        ctx.closePath();

        if (type === 3) {
          // Data Lake Reservoir (Harmonized Context Lake)
          const wave = Math.sin(timestamp * 0.003 + x * 0.4 + y * 0.4) * 8;
          ctx.fillStyle = this.isNightMode ? `rgb(6, ${50 + wave}, 90)` : `rgb(186, 230, 253)`;
          ctx.fill();
          ctx.strokeStyle = this.isNightMode ? 'rgba(6, 182, 212, 0.4)' : '#38bdf8';
          ctx.lineWidth = 0.5;
          ctx.stroke();

          // Subtle water glint
          if ((x + y) % 3 === 0 && Math.sin(timestamp * 0.005 + x) > 0.6) {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
            ctx.fillRect(-2, -1, 4, 2);
          }
        } else if (type === 1 || type === 2) {
          // Paved Asphalt Road & Fiber Highway
          ctx.fillStyle = this.isNightMode ? '#0f172a' : '#94a3b8';
          ctx.fill();
          ctx.strokeStyle = type === 2 ? '#38bdf8' : 'rgba(255, 255, 255, 0.08)';
          ctx.lineWidth = type === 2 ? 1.5 : 0.5;
          ctx.stroke();

          if (type === 2) {
            // Neon data circuit pulse
            const pulse = (Math.sin(timestamp * 0.004 + (x + y) * 0.7) + 1) / 2;
            ctx.fillStyle = `rgba(56, 189, 248, ${0.15 + pulse * 0.35})`;
            ctx.fill();
          }
        } else if (type === 5) {
          // Tech Plaza (Agentforce Central Commons)
          ctx.fillStyle = this.isNightMode ? '#1e1b4b' : '#ede9fe';
          ctx.fill();
          ctx.strokeStyle = 'rgba(168, 85, 247, 0.4)';
          ctx.lineWidth = 1;
          ctx.stroke();
        } else if (type === 6) {
          // Maglev Railway Track
          ctx.fillStyle = this.isNightMode ? '#280d38' : '#fce7f3';
          ctx.fill();
          ctx.strokeStyle = '#ec4899';
          ctx.lineWidth = 1.2;
          ctx.stroke();
        } else {
          // Default Cyber Turf / Green Commons
          ctx.fillStyle = this.isNightMode ? '#080d1a' : '#f8fafc';
          ctx.fill();
          ctx.strokeStyle = this.isNightMode ? 'rgba(255, 255, 255, 0.04)' : 'rgba(0, 0, 0, 0.06)';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }

        ctx.restore();
      }
    }
  }

  renderRoadTraffic(ctx, timestamp) {
    this.vehicles.forEach(v => {
      const curX = v.startX + (v.endX - v.startX) * v.progress;
      const curY = v.startY + (v.endY - v.startY) * v.progress;
      const pos = this.gridToScreen(curX, curY);

      ctx.save();
      // Vehicle shadow
      ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
      ctx.beginPath();
      ctx.ellipse(pos.x, pos.y + 1, 5, 2.5, 0, 0, Math.PI * 2);
      ctx.fill();

      // Vehicle hovercraft body
      ctx.fillStyle = v.color;
      ctx.fillRect(pos.x - 3, pos.y - 4, 6, 3);

      // Headlight glow
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(pos.x + 2, pos.y - 3, 2, 2);
      ctx.restore();
    });
  }

  renderConduits(ctx, timestamp) {
    ctx.save();
    this.conduits.forEach(conduit => {
      const b1 = this.buildings.find(b => b.id === conduit.from);
      const b2 = this.buildings.find(b => b.id === conduit.to);
      if (!b1 || !b2) return;

      const p1 = this.gridToScreen(b1.gridX + b1.width / 2, b1.gridY + b1.height / 2);
      const p2 = this.gridToScreen(b2.gridX + b2.width / 2, b2.gridY + b2.height / 2);

      let strokeColor = 'rgba(56, 189, 248, 0.5)';
      if (conduit.type === 'automation') strokeColor = 'rgba(245, 158, 11, 0.6)';
      if (conduit.type === 'semantic') strokeColor = 'rgba(6, 182, 212, 0.6)';
      if (conduit.type === 'agentforce') strokeColor = 'rgba(168, 85, 247, 0.65)';
      if (conduit.type === 'claudeforce') strokeColor = 'rgba(249, 115, 22, 0.65)';
      if (conduit.type === 'mcp') strokeColor = 'rgba(236, 72, 153, 0.65)';
      if (conduit.type === 'headless') strokeColor = 'rgba(16, 185, 129, 0.65)';

      if (this.activeFilter !== 'all' && this.activeFilter !== conduit.type) {
        strokeColor = 'rgba(100, 116, 139, 0.1)';
      }

      // Glowing underlay
      ctx.beginPath();
      ctx.moveTo(p1.x, p1.y);
      ctx.lineTo(p2.x, p2.y);
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Moving energy pulses
      ctx.setLineDash([5, 12]);
      ctx.lineDashOffset = -timestamp * 0.04;
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.setLineDash([]);
    });
    ctx.restore();
  }

  renderBuildings(ctx, timestamp) {
    // Sort buildings for isometric depth
    const sorted = [...this.buildings].sort((a, b) => {
      const depthA = (a.gridX + a.width) + (a.gridY + a.height);
      const depthB = (b.gridX + b.width) + (b.gridY + b.height);
      return depthA - depthB;
    });

    sorted.forEach(b => {
      this.renderBuildingVoxel(ctx, b, timestamp);
    });
  }

  renderBuildingVoxel(ctx, b, timestamp) {
    const { x: sx, y: sy } = this.gridToScreen(b.gridX, b.gridY);
    const widthPx = b.width * (TILE_WIDTH / 2);
    const heightPx = b.height * (TILE_HEIGHT / 2);
    const buildingHeight = b.floors * 2.8;

    const isHovered = this.hoveredBuilding && this.hoveredBuilding.id === b.id;
    const isSelected = this.selectedBuilding && this.selectedBuilding.id === b.id;
    const isDimmed = this.activeFilter !== 'all' && this.activeFilter !== b.districtId;

    ctx.save();
    ctx.translate(sx, sy);

    if (isDimmed) {
      ctx.globalAlpha = 0.2;
    }

    // 1. Ground Drop Shadow
    ctx.fillStyle = 'rgba(0, 0, 0, 0.55)';
    ctx.beginPath();
    ctx.moveTo(0, heightPx * 0.5);
    ctx.lineTo(widthPx * 1.5, heightPx * 1.8);
    ctx.lineTo(widthPx * 0.8, heightPx * 2.2);
    ctx.lineTo(-widthPx * 0.2, heightPx * 1.2);
    ctx.closePath();
    ctx.fill();

    // 2. Base Podium / Ground Foundation
    ctx.fillStyle = '#0b1324';
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(-widthPx, heightPx);
    ctx.lineTo(0, heightPx * 2);
    ctx.lineTo(widthPx, heightPx);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // 3. Multi-tier Tower Body Colors
    const baseColor = b.color || '#38bdf8';
    const leftWallColor = this.isNightMode ? '#131b2e' : '#475569';
    const rightWallColor = this.isNightMode ? '#0a101d' : '#334155';
    const roofColor = this.isNightMode ? '#1e293b' : '#64748b';

    // Left Facade
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(-widthPx, heightPx);
    ctx.lineTo(-widthPx, heightPx - buildingHeight);
    ctx.lineTo(0, -buildingHeight);
    ctx.closePath();
    ctx.fillStyle = leftWallColor;
    ctx.fill();
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.4)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Right Facade
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(widthPx, heightPx);
    ctx.lineTo(widthPx, heightPx - buildingHeight);
    ctx.lineTo(0, -buildingHeight);
    ctx.closePath();
    ctx.fillStyle = rightWallColor;
    ctx.fill();
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.6)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Architectural Vertical Mullions & Windows
    this.renderArchitecturalFacade(ctx, b, widthPx, heightPx, buildingHeight, timestamp);

    // Roof Surface
    ctx.beginPath();
    ctx.moveTo(0, -buildingHeight);
    ctx.lineTo(-widthPx, heightPx - buildingHeight);
    ctx.lineTo(0, heightPx * 2 - buildingHeight);
    ctx.lineTo(widthPx, heightPx - buildingHeight);
    ctx.closePath();
    ctx.fillStyle = roofColor;
    ctx.fill();
    ctx.strokeStyle = baseColor;
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Inset Roof Cap / Penthouse tier
    const insetW = widthPx * 0.7;
    const insetH = heightPx * 0.7;
    const insetLift = buildingHeight + 10;
    ctx.beginPath();
    ctx.moveTo(0, -insetLift);
    ctx.lineTo(-insetW, insetH - insetLift);
    ctx.lineTo(0, insetH * 2 - insetLift);
    ctx.lineTo(insetW, insetH - insetLift);
    ctx.closePath();
    ctx.fillStyle = baseColor;
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Custom Rooftop Assemblies
    this.renderRooftopAssembly(ctx, b, widthPx, heightPx, insetLift, timestamp);

    // Selection & Hover Hologram Bracket
    if (isHovered || isSelected) {
      ctx.lineWidth = isSelected ? 3 : 2;
      ctx.strokeStyle = isSelected ? '#facc15' : '#38bdf8';
      ctx.stroke();

      // Pulsing Ground Bracket
      ctx.beginPath();
      ctx.moveTo(0, -2);
      ctx.lineTo(-widthPx - 3, heightPx);
      ctx.lineTo(0, heightPx * 2 + 3);
      ctx.lineTo(widthPx + 3, heightPx);
      ctx.closePath();
      ctx.strokeStyle = isSelected ? 'rgba(250, 204, 21, 0.8)' : 'rgba(56, 189, 248, 0.8)';
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    ctx.restore();
  }

  renderArchitecturalFacade(ctx, b, w, h, bh, timestamp) {
    const floorsCount = Math.min(14, Math.floor(b.floors / 3.5));
    const columns = 3;

    // Window Lights
    for (let f = 1; f <= floorsCount; f++) {
      const yL = (bh / (floorsCount + 1)) * f;
      // Left Wall
      for (let c = 1; c <= columns; c++) {
        const illuminated = Math.sin(timestamp * 0.001 + f * 9 + c * 5 + b.floors) > -0.2;
        if (illuminated) {
          ctx.fillStyle = this.isNightMode ? 'rgba(254, 240, 138, 0.85)' : 'rgba(255, 255, 255, 0.9)';
          const wx = -w * (c / (columns + 1));
          const wy = h * (c / (columns + 1)) - yL;
          ctx.fillRect(wx - 2, wy - 3, 3, 5);
        }
      }

      // Right Wall
      for (let c = 1; c <= columns; c++) {
        const illuminated = Math.cos(timestamp * 0.001 + f * 11 + c * 7 + b.floors) > 0.0;
        if (illuminated) {
          ctx.fillStyle = this.isNightMode ? 'rgba(56, 189, 248, 0.85)' : 'rgba(203, 213, 225, 0.8)';
          const wx = w * (c / (columns + 1));
          const wy = h * (c / (columns + 1)) - yL;
          ctx.fillRect(wx - 1, wy - 3, 3, 5);
        }
      }
    }
  }

  renderRooftopAssembly(ctx, b, w, h, lift, timestamp) {
    const cx = 0;
    const cy = h * 0.7 - lift;

    if (b.roofType === 'pulsing_orb') {
      // Agentforce Atlas Core Spire
      const pulse = Math.sin(timestamp * 0.005) * 5;
      const gradient = ctx.createRadialGradient(cx, cy - 24, 2, cx, cy - 24, 22 + pulse);
      gradient.addColorStop(0, '#ffffff');
      gradient.addColorStop(0.3, '#c084fc');
      gradient.addColorStop(0.7, 'rgba(168, 85, 247, 0.4)');
      gradient.addColorStop(1, 'rgba(168, 85, 247, 0)');

      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(cx, cy - 24, 22 + pulse, 0, Math.PI * 2);
      ctx.fill();

      // Crystalline Core
      ctx.fillStyle = '#9333ea';
      ctx.beginPath();
      ctx.arc(cx, cy - 24, 8, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#f3e8ff';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Energy Orbit Ring
      ctx.beginPath();
      ctx.ellipse(cx, cy - 24, 18, 7, timestamp * 0.003, 0, Math.PI * 2);
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    } else if (b.roofType === 'beacon') {
      // Calculated Insights Rotating Searchlight
      const angle = timestamp * 0.003;
      ctx.fillStyle = '#06b6d4';
      ctx.beginPath();
      ctx.arc(cx, cy - 14, 7, 0, Math.PI * 2);
      ctx.fill();

      ctx.save();
      ctx.beginPath();
      ctx.moveTo(cx, cy - 14);
      ctx.arc(cx, cy - 14, 140, angle - 0.28, angle + 0.28);
      ctx.closePath();
      ctx.fillStyle = 'rgba(6, 182, 212, 0.16)';
      ctx.fill();
      ctx.restore();
    } else if (b.roofType === 'rotating_dome' || b.roofType === 'radar') {
      // Claudeforce Observatory Dome & Radar Array
      ctx.beginPath();
      ctx.arc(cx, cy - 8, 10, 0, Math.PI, true);
      ctx.fillStyle = '#e2e8f0';
      ctx.fill();
      ctx.strokeStyle = '#334155';
      ctx.stroke();

      const angle = timestamp * 0.04;
      ctx.beginPath();
      ctx.moveTo(cx, cy - 8);
      ctx.lineTo(cx + Math.cos(angle) * 16, cy - 8 + Math.sin(angle) * 8);
      ctx.strokeStyle = '#f97316';
      ctx.lineWidth = 2;
      ctx.stroke();
    } else if (b.roofType === 'antenna') {
      // Telecom Mast with Strobe Hazard Light
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx, cy - 32);
      ctx.strokeStyle = '#cbd5e1';
      ctx.lineWidth = 2;
      ctx.stroke();

      const strobe = Math.sin(timestamp * 0.008) > 0.2;
      ctx.fillStyle = strobe ? '#ef4444' : '#581c1c';
      ctx.beginPath();
      ctx.arc(cx, cy - 32, 3.5, 0, Math.PI * 2);
      ctx.fill();
      if (strobe) {
        ctx.shadowColor = '#ef4444';
        ctx.shadowBlur = 8;
        ctx.stroke();
      }
    } else if (b.roofType === 'helipad') {
      // Headless Skyport Launch Pad
      ctx.fillStyle = '#059669';
      ctx.beginPath();
      ctx.arc(cx, cy, 14, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#34d399';
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 11px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('H', cx, cy);
    } else if (b.roofType === 'crystal') {
      // Vector RAG Monolith
      const bob = Math.sin(timestamp * 0.005) * 4;
      ctx.fillStyle = '#22d3ee';
      ctx.beginPath();
      ctx.moveTo(cx, cy - 26 + bob);
      ctx.lineTo(cx + 7, cy - 14 + bob);
      ctx.lineTo(cx, cy - 2 + bob);
      ctx.lineTo(cx - 7, cy - 14 + bob);
      ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  }

  renderParticlesAndDrones(ctx, timestamp) {
    // 1. Data Packets
    this.particleSystem.packets.forEach(p => {
      const curX = p.fromX + (p.toX - p.fromX) * p.progress;
      const curY = p.fromY + (p.toY - p.fromY) * p.progress;
      const screenPos = this.gridToScreen(curX, curY);
      const arc = Math.sin(p.progress * Math.PI) * 25;

      ctx.save();
      ctx.fillStyle = p.color;
      ctx.shadowColor = p.color;
      ctx.shadowBlur = 10;
      ctx.beginPath();
      ctx.arc(screenPos.x, screenPos.y - arc, p.size || 4.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });

    // 2. Drones
    this.particleSystem.drones.forEach((d, i) => {
      const screenPos = this.gridToScreen(d.currentX, d.currentY);
      const bob = Math.sin(timestamp * 0.006 + i) * 3;
      const droneY = screenPos.y - d.altitude + bob;

      ctx.save();
      // Ground Shadow
      ctx.fillStyle = 'rgba(0, 0, 0, 0.35)';
      ctx.beginPath();
      ctx.ellipse(screenPos.x, screenPos.y, 7, 3.5, 0, 0, Math.PI * 2);
      ctx.fill();

      // Drone Body
      ctx.fillStyle = d.color;
      ctx.fillRect(screenPos.x - 5, droneY - 3, 10, 5);

      // Spinning Rotors
      const angle = timestamp * 0.06;
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(screenPos.x - 9 + Math.cos(angle) * 5, droneY - 5);
      ctx.lineTo(screenPos.x - 9 - Math.cos(angle) * 5, droneY - 5);
      ctx.moveTo(screenPos.x + 9 + Math.cos(angle) * 5, droneY - 5);
      ctx.lineTo(screenPos.x + 9 - Math.cos(angle) * 5, droneY - 5);
      ctx.stroke();

      // Status Beacon
      ctx.fillStyle = '#22c55e';
      ctx.beginPath();
      ctx.arc(screenPos.x, droneY, 2, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });
  }

  renderDistrictHolograms(ctx, timestamp) {
    const districts = [
      { name: '1. Metadata Citadel', gx: 4, gy: 4, color: '#38bdf8' },
      { name: '2. Automation Grid', gx: 12, gy: 4, color: '#f59e0b' },
      { name: '3. Data Cloud Harbor', gx: 20, gy: 5, color: '#06b6d4' },
      { name: '4. Headless 360 Skyport', gx: 4, gy: 16, color: '#10b981' },
      { name: '5. Agentforce Hub', gx: 13, gy: 13, color: '#a855f7' },
      { name: '6. Claudeforce Labs', gx: 18, gy: 13, color: '#f97316' },
      { name: '7. Dual MCP Interchange', gx: 18, gy: 19, color: '#ec4899' }
    ];

    ctx.save();
    districts.forEach(d => {
      const pos = this.gridToScreen(d.gx, d.gy);
      const bob = Math.sin(timestamp * 0.003 + d.gx) * 3;

      ctx.font = '600 10px Inter, sans-serif';
      const textW = ctx.measureText(d.name).width;

      ctx.fillStyle = 'rgba(10, 16, 32, 0.75)';
      ctx.strokeStyle = d.color;
      ctx.lineWidth = 1;

      const px = pos.x - textW / 2 - 8;
      const py = pos.y - 180 + bob;

      // Hologram Pill
      ctx.beginPath();
      ctx.roundRect(px, py, textW + 16, 20, 10);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(d.name, pos.x, py + 10);
    });
    ctx.restore();
  }

  renderFloatingBadge(ctx, b) {
    const pos = this.gridToScreen(b.gridX + b.width / 2, b.gridY + b.height / 2);
    const sx = this.camera.x + pos.x * this.camera.zoom;
    const sy = this.camera.y + (pos.y - b.floors * 2.8 - 25) * this.camera.zoom;

    ctx.save();
    ctx.font = '600 12px Inter, sans-serif';
    const nameWidth = ctx.measureText(b.name).width;

    ctx.fillStyle = 'rgba(13, 20, 39, 0.95)';
    ctx.strokeStyle = b.color || '#38bdf8';
    ctx.lineWidth = 1.5;

    const w = nameWidth + 24;
    const h = 28;
    const rx = sx - w / 2;
    const ry = sy - h / 2;

    ctx.beginPath();
    ctx.roundRect(rx, ry, w, h, 8);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(b.name, sx, sy);
    ctx.restore();
  }
}
'''

with open('/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer/src/engine/IsometricCanvas.js', 'w') as f:
    f.write(canvas_code)

print("Upgraded IsometricCanvas.js written successfully!")
