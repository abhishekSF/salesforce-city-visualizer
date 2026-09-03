iso_canvas_code = '''import { TILE_WIDTH, TILE_HEIGHT, GRID_SIZE, generateTileMap } from '../data/cityLayout.js';
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

    // Camera state
    this.camera = {
      x: 0,
      y: 0,
      zoom: 1.0,
      targetZoom: 1.0,
      isDragging: false,
      dragStartX: 0,
      dragStartY: 0,
      camStartX: 0,
      camStartY: 0
    };

    // Interaction state
    this.hoveredBuilding = null;
    this.selectedBuilding = null;
    this.activeFilter = 'all'; // 'all', 'metadata', 'automation', 'semantic', 'headless', 'agentforce', 'claudeforce', 'mcp'
    this.isNightMode = true;

    this.initCanvasSize();
    this.centerCamera();
    this.bindEvents();
  }

  initCanvasSize() {
    const dpr = window.devicePixelRatio || 1;
    const rect = this.canvas.getBoundingClientRect();
    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;
    this.ctx.scale(dpr, dpr);
    this.width = rect.width;
    this.height = rect.height;
  }

  centerCamera() {
    // Center on central Agentforce plaza (grid x: 12, y: 12)
    const centerScreen = this.gridToScreen(12, 12);
    this.camera.x = this.width / 2 - centerScreen.x * this.camera.zoom;
    this.camera.y = this.height / 2 - (centerScreen.y - 120) * this.camera.zoom;
  }

  focusBuilding(buildingId) {
    const b = this.buildings.find(item => item.id === buildingId);
    if (!b) return;
    this.selectedBuilding = b;
    const pos = this.gridToScreen(b.gridX + b.width / 2, b.gridY + b.height / 2);
    this.camera.x = this.width / 2 - pos.x * this.camera.zoom;
    this.camera.y = this.height / 2 - (pos.y - b.floors * 0.7) * this.camera.zoom;
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
        // If minimal movement, treat as click
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
      const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9;
      const newZoom = Math.max(0.4, Math.min(2.2, this.camera.zoom * zoomFactor));

      const rect = this.canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;

      this.camera.x = mx - (mx - this.camera.x) * (newZoom / this.camera.zoom);
      this.camera.y = my - (my - this.camera.y) * (newZoom / this.camera.zoom);
      this.camera.zoom = newZoom;
    }, { passive: false });
  }

  checkHover(mx, my) {
    const { gx, gy } = this.screenToGrid(mx, my);
    let found = null;

    // Check buildings in reverse depth order
    const sorted = [...this.buildings].sort((a, b) => {
      return (b.gridX + b.width + b.gridY + b.height) - (a.gridX + a.width + a.gridY + a.height);
    });

    for (const b of sorted) {
      // Approximate bounding box on screen
      const p = this.gridToScreen(b.gridX + b.width / 2, b.gridY + b.height / 2);
      const sx = this.camera.x + p.x * this.camera.zoom;
      const sy = this.camera.y + (p.y - b.floors * 0.8) * this.camera.zoom;
      const bW = (b.width * TILE_WIDTH) * this.camera.zoom * 0.8;
      const bH = (b.height * TILE_HEIGHT + b.floors * 1.6) * this.camera.zoom;

      if (mx >= sx - bW / 2 && mx <= sx + bW / 2 && my >= sy - bH * 0.3 && my <= sy + bH * 0.8) {
        found = b;
        break;
      }
    }

    if (found !== this.hoveredBuilding) {
      this.hoveredBuilding = found;
      this.canvas.style.cursor = found ? 'pointer' : 'default';
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

  render(timestamp = 0) {
    const ctx = this.ctx;
    ctx.imageSmoothingEnabled = false;

    // Clear background
    ctx.fillStyle = this.isNightMode ? '#070b14' : '#e2e8f0';
    ctx.fillRect(0, 0, this.width, this.height);

    ctx.save();
    ctx.translate(this.camera.x, this.camera.y);
    ctx.scale(this.camera.zoom, this.camera.zoom);

    // 1. Draw Base Ground Grid
    this.renderGround(ctx, timestamp);

    // 2. Draw Conduits and Data Highways
    this.renderConduits(ctx, timestamp);

    // 3. Draw Buildings (depth-sorted)
    this.renderBuildings(ctx, timestamp);

    // 4. Draw Particles & Drones
    this.renderParticlesAndDrones(ctx, timestamp);

    ctx.restore();

    // 5. Draw Mini-Map HUD
    this.renderMiniMap(ctx);

    // 6. Draw Selected / Hovered Floating Badge
    if (this.hoveredBuilding) {
      this.renderFloatingBadge(ctx, this.hoveredBuilding);
    }
  }

  renderGround(ctx, timestamp) {
    for (let y = 0; y < GRID_SIZE; y++) {
      for (let x = 0; x < GRID_SIZE; x++) {
        const type = this.tileMap[y][x];
        const { x: sx, y: sy } = this.gridToScreen(x, y);

        // Cull offscreen tiles
        const screenPx = this.camera.x + sx * this.camera.zoom;
        const screenPy = this.camera.y + sy * this.camera.zoom;
        if (screenPx < -100 || screenPx > this.width + 100 || screenPy < -100 || screenPy > this.height + 100) {
          continue;
        }

        ctx.save();
        ctx.translate(sx, sy);

        // Draw diamond tile
        ctx.beginPath();
        ctx.moveTo(0, -TILE_HEIGHT / 2);
        ctx.lineTo(TILE_WIDTH / 2, 0);
        ctx.lineTo(0, TILE_HEIGHT / 2);
        ctx.lineTo(-TILE_WIDTH / 2, 0);
        ctx.closePath();

        // Color based on type and night mode
        if (type === 3) {
          // Water (Data Lake)
          const wave = Math.sin(timestamp * 0.003 + x * 0.5 + y * 0.5) * 15;
          ctx.fillStyle = this.isNightMode ? `rgb(6, ${80 + wave}, 140)` : `rgb(56, ${180 + wave}, 240)`;
          ctx.fill();
          ctx.strokeStyle = this.isNightMode ? '#0891b2' : '#7dd3fc';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        } else if (type === 1) {
          // Paved Road
          ctx.fillStyle = this.isNightMode ? '#1e293b' : '#94a3b8';
          ctx.fill();
          ctx.strokeStyle = this.isNightMode ? '#0f172a' : '#cbd5e1';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        } else if (type === 2) {
          // Fiber-Optic Highway
          const pulse = (Math.sin(timestamp * 0.005 + (x + y) * 0.8) + 1) / 2;
          ctx.fillStyle = this.isNightMode ? '#0f172a' : '#cbd5e1';
          ctx.fill();
          ctx.strokeStyle = this.isNightMode ? `rgba(56, 189, 248, ${0.4 + pulse * 0.6})` : '#0284c7';
          ctx.lineWidth = 1.5;
          ctx.stroke();
        } else if (type === 5) {
          // Tech Plaza
          ctx.fillStyle = this.isNightMode ? '#1e1b4b' : '#f1f5f9';
          ctx.fill();
          ctx.strokeStyle = this.isNightMode ? '#4338ca' : '#cbd5e1';
          ctx.lineWidth = 1;
          ctx.stroke();
        } else if (type === 6) {
          // Maglev Track
          ctx.fillStyle = this.isNightMode ? '#31103f' : '#fce7f3';
          ctx.fill();
          ctx.strokeStyle = '#ec4899';
          ctx.lineWidth = 1;
          ctx.stroke();
        } else {
          // Grass / Cyber Turf
          ctx.fillStyle = this.isNightMode ? '#0b1329' : '#f8fafc';
          ctx.fill();
          ctx.strokeStyle = this.isNightMode ? '#132042' : '#e2e8f0';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }

        ctx.restore();
      }
    }
  }

  renderConduits(ctx, timestamp) {
    ctx.save();
    this.conduits.forEach(conduit => {
      const b1 = this.buildings.find(b => b.id === conduit.from);
      const b2 = this.buildings.find(b => b.id === conduit.to);
      if (!b1 || !b2) return;

      const p1 = this.gridToScreen(b1.gridX + b1.width / 2, b1.gridY + b1.height / 2);
      const p2 = this.gridToScreen(b2.gridX + b2.width / 2, b2.gridY + b2.height / 2);

      let strokeColor = 'rgba(56, 189, 248, 0.4)';
      if (conduit.type === 'automation') strokeColor = 'rgba(234, 179, 8, 0.4)';
      if (conduit.type === 'semantic') strokeColor = 'rgba(6, 182, 212, 0.5)';
      if (conduit.type === 'agentforce') strokeColor = 'rgba(139, 92, 246, 0.5)';
      if (conduit.type === 'claudeforce') strokeColor = 'rgba(249, 115, 22, 0.5)';
      if (conduit.type === 'mcp') strokeColor = 'rgba(236, 72, 153, 0.5)';
      if (conduit.type === 'headless') strokeColor = 'rgba(16, 185, 129, 0.5)';

      // Filter check
      if (this.activeFilter !== 'all' && this.activeFilter !== conduit.type) {
        strokeColor = 'rgba(100, 116, 139, 0.15)';
      }

      ctx.beginPath();
      ctx.setLineDash([4, 4]);
      ctx.lineDashOffset = -timestamp * 0.03;
      ctx.moveTo(p1.x, p1.y);
      ctx.lineTo(p2.x, p2.y);
      ctx.strokeStyle = strokeColor;
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
      this.renderSingleBuilding(ctx, b, timestamp);
    });
  }

  renderSingleBuilding(ctx, b, timestamp) {
    const { x: sx, y: sy } = this.gridToScreen(b.gridX, b.gridY);
    const widthPx = b.width * (TILE_WIDTH / 2);
    const heightPx = b.height * (TILE_HEIGHT / 2);
    const buildingHeight = b.floors * 2.2;

    const isHovered = this.hoveredBuilding && this.hoveredBuilding.id === b.id;
    const isSelected = this.selectedBuilding && this.selectedBuilding.id === b.id;
    const isDimmed = this.activeFilter !== 'all' && this.activeFilter !== b.districtId;

    ctx.save();
    ctx.translate(sx, sy);

    if (isDimmed) {
      ctx.globalAlpha = 0.25;
    }

    // Base color tones
    const baseColor = b.color || '#3b82f6';
    const leftFaceColor = this.isNightMode ? '#1e293b' : '#475569';
    const rightFaceColor = this.isNightMode ? '#0f172a' : '#334155';
    const topFaceColor = baseColor;

    // Draw Left Wall
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(-widthPx, heightPx);
    ctx.lineTo(-widthPx, heightPx - buildingHeight);
    ctx.lineTo(0, -buildingHeight);
    ctx.closePath();
    ctx.fillStyle = leftFaceColor;
    ctx.fill();
    ctx.strokeStyle = '#020617';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Draw Right Wall
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(widthPx, heightPx);
    ctx.lineTo(widthPx, heightPx - buildingHeight);
    ctx.lineTo(0, -buildingHeight);
    ctx.closePath();
    ctx.fillStyle = rightFaceColor;
    ctx.fill();
    ctx.strokeStyle = '#020617';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Draw Windows (Pixelated Light Grid)
    this.renderBuildingWindows(ctx, b, widthPx, heightPx, buildingHeight, timestamp);

    // Draw Roof / Top Face
    ctx.beginPath();
    ctx.moveTo(0, -buildingHeight);
    ctx.lineTo(-widthPx, heightPx - buildingHeight);
    ctx.lineTo(0, heightPx * 2 - buildingHeight);
    ctx.lineTo(widthPx, heightPx - buildingHeight);
    ctx.closePath();
    ctx.fillStyle = topFaceColor;
    ctx.fill();
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Draw Custom Roof Feature
    this.renderRoofFeature(ctx, b, widthPx, heightPx, buildingHeight, timestamp);

    // Draw Selection / Hover Aura
    if (isHovered || isSelected) {
      ctx.lineWidth = 2.5;
      ctx.strokeStyle = isSelected ? '#facc15' : '#38bdf8';
      ctx.stroke();

      // Pulsing ground bracket
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(-widthPx, heightPx);
      ctx.lineTo(0, heightPx * 2);
      ctx.lineTo(widthPx, heightPx);
      ctx.closePath();
      ctx.strokeStyle = isSelected ? 'rgba(250, 204, 21, 0.8)' : 'rgba(56, 189, 248, 0.8)';
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    ctx.restore();
  }

  renderBuildingWindows(ctx, b, w, h, bh, timestamp) {
    const rows = Math.min(12, Math.floor(b.floors / 4));
    const cols = 3;

    ctx.fillStyle = this.isNightMode ? '#fef08a' : '#f8fafc';

    // Left Wall Windows
    for (let r = 1; r <= rows; r++) {
      const yOffset = (bh / (rows + 1)) * r;
      for (let c = 1; c <= cols; c++) {
        // Blinking window effect
        const blink = Math.sin(timestamp * 0.002 + r * 11 + c * 7 + b.floors) > 0.3;
        if (blink) {
          const wx = -w * (c / (cols + 1));
          const wy = h * (c / (cols + 1)) - yOffset;
          ctx.fillRect(wx - 2, wy - 3, 3, 5);
        }
      }
    }

    // Right Wall Windows
    for (let r = 1; r <= rows; r++) {
      const yOffset = (bh / (rows + 1)) * r;
      for (let c = 1; c <= cols; c++) {
        const blink = Math.cos(timestamp * 0.002 + r * 13 + c * 5 + b.floors) > 0.2;
        if (blink) {
          const wx = w * (c / (cols + 1));
          const wy = h * (c / (cols + 1)) - yOffset;
          ctx.fillRect(wx - 1, wy - 3, 3, 5);
        }
      }
    }
  }

  renderRoofFeature(ctx, b, w, h, bh, timestamp) {
    const centerX = 0;
    const centerY = heightPx => heightPx - bh; // center of roof is (0, h - bh)
    const roofCenterY = h - bh;

    if (b.roofType === 'antenna') {
      // Radio Antenna mast with blinking red warning light
      ctx.beginPath();
      ctx.moveTo(centerX, roofCenterY);
      ctx.lineTo(centerX, roofCenterY - 28);
      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Blinking red aviation hazard light
      const flash = Math.sin(timestamp * 0.006) > 0;
      ctx.fillStyle = flash ? '#ef4444' : '#7f1d1d';
      ctx.beginPath();
      ctx.arc(centerX, roofCenterY - 28, 3, 0, Math.PI * 2);
      ctx.fill();
    } else if (b.roofType === 'smokestack') {
      // Industrial smokestack
      ctx.fillStyle = '#64748b';
      ctx.fillRect(centerX - 4, roofCenterY - 14, 8, 14);
      ctx.fillStyle = '#f97316';
      ctx.fillRect(centerX - 5, roofCenterY - 16, 10, 3);
    } else if (b.roofType === 'rotating_dome' || b.roofType === 'radar') {
      // Rotating Radar dish
      ctx.beginPath();
      ctx.arc(centerX, roofCenterY - 8, 8, 0, Math.PI, true);
      ctx.fillStyle = '#cbd5e1';
      ctx.fill();
      ctx.strokeStyle = '#475569';
      ctx.stroke();

      // Radar beam line
      const angle = this.particleSystem.radarAngle;
      ctx.beginPath();
      ctx.moveTo(centerX, roofCenterY - 8);
      ctx.lineTo(centerX + Math.cos(angle) * 14, roofCenterY - 8 + Math.sin(angle) * 7);
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2;
      ctx.stroke();
    } else if (b.roofType === 'pulsing_orb') {
      // Agentforce Atlas Core Spire
      const pulse = Math.sin(timestamp * 0.005) * 4;
      const gradient = ctx.createRadialGradient(centerX, roofCenterY - 20, 2, centerX, roofCenterY - 20, 16 + pulse);
      gradient.addColorStop(0, '#ffffff');
      gradient.addColorStop(0.4, '#c084fc');
      gradient.addColorStop(1, 'rgba(139, 92, 246, 0)');

      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(centerX, roofCenterY - 20, 16 + pulse, 0, Math.PI * 2);
      ctx.fill();

      // Core sphere
      ctx.fillStyle = '#a855f7';
      ctx.beginPath();
      ctx.arc(centerX, roofCenterY - 20, 7, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#f3e8ff';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    } else if (b.roofType === 'beacon') {
      // Calculated Insights Lighthouse rotating searchlight
      const angle = timestamp * 0.003;
      ctx.fillStyle = '#06b6d4';
      ctx.beginPath();
      ctx.arc(centerX, roofCenterY - 12, 6, 0, Math.PI * 2);
      ctx.fill();

      // Sweeping cone of light
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(centerX, roofCenterY - 12);
      ctx.arc(centerX, roofCenterY - 12, 90, angle - 0.35, angle + 0.35);
      ctx.closePath();
      ctx.fillStyle = 'rgba(6, 182, 212, 0.12)';
      ctx.fill();
      ctx.restore();
    } else if (b.roofType === 'helipad') {
      // Headless Skyport Helipad with "H"
      ctx.fillStyle = '#059669';
      ctx.beginPath();
      ctx.arc(centerX, roofCenterY, 12, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#34d399';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 9px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('H', centerX, roofCenterY);
    } else if (b.roofType === 'crystal') {
      // Vector RAG Crystal Monolith
      const hover = Math.sin(timestamp * 0.004) * 3;
      ctx.fillStyle = '#22d3ee';
      ctx.beginPath();
      ctx.moveTo(centerX, roofCenterY - 22 + hover);
      ctx.lineTo(centerX + 6, roofCenterY - 12 + hover);
      ctx.lineTo(centerX, roofCenterY - 2 + hover);
      ctx.lineTo(centerX - 6, roofCenterY - 12 + hover);
      ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = '#e0f2fe';
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  }

  renderParticlesAndDrones(ctx, timestamp) {
    // 1. Render data packets
    this.particleSystem.packets.forEach(p => {
      const curX = p.fromX + (p.toX - p.fromX) * p.progress;
      const curY = p.fromY + (p.toY - p.fromY) * p.progress;
      const screenPos = this.gridToScreen(curX, curY);

      // Height arc
      const arc = Math.sin(p.progress * Math.PI) * 20;

      ctx.save();
      ctx.fillStyle = p.color;
      ctx.shadowColor = p.color;
      ctx.shadowBlur = 8;
      ctx.beginPath();
      ctx.arc(screenPos.x, screenPos.y - arc, p.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });

    // 2. Render smoke puffs
    this.particleSystem.smokePuffs.forEach(sp => {
      const screenPos = this.gridToScreen(sp.x, sp.y);
      ctx.save();
      ctx.fillStyle = `rgba(203, 213, 225, ${sp.alpha})`;
      ctx.beginPath();
      ctx.arc(screenPos.x, screenPos.y - sp.heightOffset, sp.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });

    // 3. Render autonomous drones
    this.particleSystem.drones.forEach((d, i) => {
      const screenPos = this.gridToScreen(d.currentX, d.currentY);
      const bob = Math.sin(timestamp * 0.006 + i) * 3;
      const droneY = screenPos.y - d.altitude + bob;

      ctx.save();
      // Drone shadow on ground
      ctx.fillStyle = 'rgba(0, 0, 0, 0.25)';
      ctx.beginPath();
      ctx.ellipse(screenPos.x, screenPos.y, 6, 3, 0, 0, Math.PI * 2);
      ctx.fill();

      // Drone body
      ctx.fillStyle = d.color;
      ctx.fillRect(screenPos.x - 4, droneY - 2, 8, 4);

      // Drone rotors (spinning line)
      const rotAngle = timestamp * 0.05;
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(screenPos.x - 8 + Math.cos(rotAngle) * 4, droneY - 4);
      ctx.lineTo(screenPos.x - 8 - Math.cos(rotAngle) * 4, droneY - 4);
      ctx.moveTo(screenPos.x + 8 + Math.cos(rotAngle) * 4, droneY - 4);
      ctx.lineTo(screenPos.x + 8 - Math.cos(rotAngle) * 4, droneY - 4);
      ctx.stroke();

      // Drone status LED
      ctx.fillStyle = '#22c55e';
      ctx.beginPath();
      ctx.arc(screenPos.x, droneY, 1.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });
  }

  renderMiniMap(ctx) {
    const mapW = 140;
    const mapH = 90;
    const mapX = this.width - mapW - 16;
    const mapY = this.height - mapH - 16;

    ctx.save();
    // Mini-map background
    ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
    ctx.fillRect(mapX, mapY, mapW, mapH);
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 1;
    ctx.strokeRect(mapX, mapY, mapW, mapH);

    // Mini-map title
    ctx.fillStyle = '#94a3b8';
    ctx.font = '9px monospace';
    ctx.fillText('ORG RADAR', mapX + 8, mapY + 14);

    // Plot buildings
    this.buildings.forEach(b => {
      const bx = mapX + (b.gridX / GRID_SIZE) * mapW;
      const by = mapY + (b.gridY / GRID_SIZE) * mapH;
      ctx.fillStyle = b.color || '#38bdf8';
      ctx.fillRect(bx, by, 3, 3);
    });

    ctx.restore();
  }

  renderFloatingBadge(ctx, b) {
    const pos = this.gridToScreen(b.gridX + b.width / 2, b.gridY + b.height / 2);
    const sx = this.camera.x + pos.x * this.camera.zoom;
    const sy = this.camera.y + (pos.y - b.floors * 2.2 - 20) * this.camera.zoom;

    ctx.save();
    ctx.font = 'bold 11px monospace';
    const textW = ctx.measureText(b.name).width;

    ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
    ctx.fillRect(sx - textW / 2 - 8, sy - 18, textW + 16, 22);
    ctx.strokeStyle = b.color || '#38bdf8';
    ctx.lineWidth = 1;
    ctx.strokeRect(sx - textW / 2 - 8, sy - 18, textW + 16, 22);

    ctx.fillStyle = '#f8fafc';
    ctx.textAlign = 'center';
    ctx.fillText(b.name, sx, sy - 3);
    ctx.restore();
  }
}
'''

with open('/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer/src/engine/IsometricCanvas.js', 'w') as f:
    f.write(iso_canvas_code)

print("IsometricCanvas.js written successfully!")
