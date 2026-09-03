import { TILE_WIDTH, TILE_HEIGHT, GRID_SIZE, generateTileMap } from '../data/cityLayout.js';
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

    // View modes: 'rendered' (axonometric model), 'wireframe' (structural blueprint)
    this.viewMode = 'rendered';
    this.hoveredBuilding = null;
    this.selectedBuilding = null;
    this.activeFilter = 'all';
    this.showCallouts = true;

    this.initCanvasSize();
    this.centerCamera(true);
    this.bindEvents();
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
    const targetY = this.height / 2 - (centerScreen.y - 100) * this.camera.targetZoom;

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
    this.camera.targetY = this.height / 2 - (pos.y - b.floors * 1.5) * this.camera.targetZoom;
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
      const zoomFactor = e.deltaY < 0 ? 1.14 : 0.88;
      const newZoom = Math.max(0.4, Math.min(2.5, this.camera.targetZoom * zoomFactor));

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
      const sy = this.camera.y + (p.y - b.floors * 1.5) * this.camera.zoom;
      const bW = (b.width * TILE_WIDTH) * this.camera.zoom * 0.95;
      const bH = (b.height * TILE_HEIGHT + b.floors * 3.0) * this.camera.zoom;

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
    this.camera.x += (this.camera.targetX - this.camera.x) * 0.14;
    this.camera.y += (this.camera.targetY - this.camera.y) * 0.14;
    this.camera.zoom += (this.camera.targetZoom - this.camera.zoom) * 0.14;
  }

  render(timestamp = 0) {
    const ctx = this.ctx;
    this.update(16);

    // Architectural drafting board background
    ctx.fillStyle = '#060911';
    ctx.fillRect(0, 0, this.width, this.height);

    ctx.save();
    ctx.translate(this.camera.x, this.camera.y);
    ctx.scale(this.camera.zoom, this.camera.zoom);

    // 1. Architectural Masterplan Ground Grid
    this.renderMasterplanGrid(ctx, timestamp);

    // 2. Circulation Arterials & Data Conduits
    this.renderCirculationConduits(ctx, timestamp);

    // 3. Axonometric Architectural Masses (Depth-Sorted)
    this.renderArchitecturalMasses(ctx, timestamp);

    // 4. Dynamic Data Vectors & Autonomous Drone Particles
    this.renderParticlesAndDrones(ctx, timestamp);

    // 5. Architectural Callout Annotations with Leader Lines
    if (this.showCallouts) {
      this.renderArchitecturalCallouts(ctx, timestamp);
    }

    ctx.restore();

    // 6. Active Building Floating Spec Badge (Screen-space)
    if (this.hoveredBuilding) {
      this.renderHoverSpecBadge(ctx, this.hoveredBuilding);
    }
  }

  renderMasterplanGrid(ctx, timestamp) {
    // Draw subtle isometric ground datum lines
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
          // Data Lake Reservoir (Semantic Harbor)
          const wave = Math.sin(timestamp * 0.0025 + (x + y) * 0.5) * 6;
          ctx.fillStyle = `rgba(6, 182, 212, ${0.12 + wave * 0.005})`;
          ctx.fill();
          ctx.strokeStyle = 'rgba(6, 182, 212, 0.4)';
          ctx.lineWidth = 0.75;
          ctx.stroke();

          // Delicate contour hatching
          if ((x + y) % 2 === 0) {
            ctx.beginPath();
            ctx.moveTo(-12, 0);
            ctx.lineTo(12, 0);
            ctx.strokeStyle = 'rgba(6, 182, 212, 0.2)';
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        } else if (type === 1 || type === 2) {
          // Primary Circulation Highway
          ctx.fillStyle = type === 2 ? 'rgba(15, 23, 42, 0.95)' : 'rgba(10, 16, 30, 0.8)';
          ctx.fill();
          ctx.strokeStyle = type === 2 ? 'rgba(56, 189, 248, 0.5)' : 'rgba(255, 255, 255, 0.1)';
          ctx.lineWidth = type === 2 ? 1.2 : 0.6;
          ctx.stroke();

          if (type === 2) {
            // Centerline dashed datum line
            ctx.beginPath();
            ctx.moveTo(-10, 0);
            ctx.lineTo(10, 0);
            ctx.strokeStyle = 'rgba(56, 189, 248, 0.7)';
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        } else if (type === 5) {
          // Central Agentforce Forum / Tech Plaza
          ctx.fillStyle = 'rgba(99, 102, 241, 0.12)';
          ctx.fill();
          ctx.strokeStyle = 'rgba(168, 85, 247, 0.45)';
          ctx.lineWidth = 0.8;
          ctx.stroke();
        } else if (type === 6) {
          // Maglev Transit Corridor
          ctx.fillStyle = 'rgba(236, 72, 153, 0.1)';
          ctx.fill();
          ctx.strokeStyle = 'rgba(236, 72, 153, 0.5)';
          ctx.lineWidth = 1;
          ctx.stroke();
        } else {
          // Standard Urban Datum Lot
          ctx.fillStyle = 'rgba(12, 18, 32, 0.4)';
          ctx.fill();
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.035)';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }

        ctx.restore();
      }
    }
  }

  renderCirculationConduits(ctx, timestamp) {
    ctx.save();
    this.conduits.forEach(conduit => {
      const b1 = this.buildings.find(b => b.id === conduit.from);
      const b2 = this.buildings.find(b => b.id === conduit.to);
      if (!b1 || !b2) return;

      const p1 = this.gridToScreen(b1.gridX + b1.width / 2, b1.gridY + b1.height / 2);
      const p2 = this.gridToScreen(b2.gridX + b2.width / 2, b2.gridY + b2.height / 2);

      let strokeColor = 'rgba(56, 189, 248, 0.4)';
      if (conduit.type === 'automation') strokeColor = 'rgba(245, 158, 11, 0.5)';
      if (conduit.type === 'semantic') strokeColor = 'rgba(6, 182, 212, 0.5)';
      if (conduit.type === 'agentforce') strokeColor = 'rgba(168, 85, 247, 0.55)';
      if (conduit.type === 'claudeforce') strokeColor = 'rgba(249, 115, 22, 0.55)';
      if (conduit.type === 'mcp') strokeColor = 'rgba(236, 72, 153, 0.55)';
      if (conduit.type === 'headless') strokeColor = 'rgba(16, 185, 129, 0.55)';

      if (this.activeFilter !== 'all' && this.activeFilter !== conduit.type) {
        strokeColor = 'rgba(255, 255, 255, 0.04)';
      }

      // Architectural Schematic Line with Arrow Terminals
      ctx.beginPath();
      ctx.moveTo(p1.x, p1.y);
      ctx.lineTo(p2.x, p2.y);
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Traveling discrete datum packets
      ctx.setLineDash([4, 14]);
      ctx.lineDashOffset = -timestamp * 0.035;
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.setLineDash([]);
    });
    ctx.restore();
  }

  renderArchitecturalMasses(ctx, timestamp) {
    const sorted = [...this.buildings].sort((a, b) => {
      const depthA = (a.gridX + a.width) + (a.gridY + a.height);
      const depthB = (b.gridX + b.width) + (b.gridY + b.height);
      return depthA - depthB;
    });

    sorted.forEach(b => {
      this.renderSingleAxonometricBuilding(ctx, b, timestamp);
    });
  }

  renderSingleAxonometricBuilding(ctx, b, timestamp) {
    const { x: sx, y: sy } = this.gridToScreen(b.gridX, b.gridY);
    const widthPx = b.width * (TILE_WIDTH / 2);
    const heightPx = b.height * (TILE_HEIGHT / 2);
    const massHeight = b.floors * 3.2;

    const isHovered = this.hoveredBuilding && this.hoveredBuilding.id === b.id;
    const isSelected = this.selectedBuilding && this.selectedBuilding.id === b.id;
    const isDimmed = this.activeFilter !== 'all' && this.activeFilter !== b.districtId;

    ctx.save();
    ctx.translate(sx, sy);

    if (isDimmed) {
      ctx.globalAlpha = 0.18;
    }

    // 1. Precise Axonometric Drop Shadow (Architectural Hatching)
    ctx.fillStyle = 'rgba(0, 0, 0, 0.55)';
    ctx.beginPath();
    ctx.moveTo(0, heightPx * 0.5);
    ctx.lineTo(widthPx * 1.6, heightPx * 1.8);
    ctx.lineTo(widthPx * 0.8, heightPx * 2.3);
    ctx.lineTo(-widthPx * 0.3, heightPx * 1.2);
    ctx.closePath();
    ctx.fill();

    // 2. Concrete Structural Plinth (Base Podium)
    ctx.fillStyle = '#0a0f1d';
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(-widthPx, heightPx);
    ctx.lineTo(0, heightPx * 2);
    ctx.lineTo(widthPx, heightPx);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.18)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // 3. Facade Tones & Architectural Glazing
    const baseAccent = b.color || '#38bdf8';
    const leftFacade = 'rgba(16, 24, 42, 0.95)';
    const rightFacade = 'rgba(10, 15, 28, 0.98)';
    const roofSlab = 'rgba(26, 38, 64, 0.92)';

    // Left Elevation Face
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(-widthPx, heightPx);
    ctx.lineTo(-widthPx, heightPx - massHeight);
    ctx.lineTo(0, -massHeight);
    ctx.closePath();
    ctx.fillStyle = leftFacade;
    ctx.fill();
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Right Elevation Face
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(widthPx, heightPx);
    ctx.lineTo(widthPx, heightPx - massHeight);
    ctx.lineTo(0, -massHeight);
    ctx.closePath();
    ctx.fillStyle = rightFacade;
    ctx.fill();
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // 4. Architectural Floor Slabs & Vertical Mullions
    this.renderFloorPlatesAndMullions(ctx, b, widthPx, heightPx, massHeight, baseAccent, timestamp);

    // 5. Roof Floor Slab (Horizontal Datum)
    ctx.beginPath();
    ctx.moveTo(0, -massHeight);
    ctx.lineTo(-widthPx, heightPx - massHeight);
    ctx.lineTo(0, heightPx * 2 - massHeight);
    ctx.lineTo(widthPx, heightPx - massHeight);
    ctx.closePath();
    ctx.fillStyle = roofSlab;
    ctx.fill();
    ctx.strokeStyle = baseAccent;
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // 6. Inset Penthouse / Mechanical Crown Assembly
    const crownW = widthPx * 0.65;
    const crownH = heightPx * 0.65;
    const crownLift = massHeight + 12;

    ctx.beginPath();
    ctx.moveTo(0, -crownLift);
    ctx.lineTo(-crownW, crownH - crownLift);
    ctx.lineTo(0, crownH * 2 - crownLift);
    ctx.lineTo(crownW, crownH - crownLift);
    ctx.closePath();
    ctx.fillStyle = baseAccent;
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1.2;
    ctx.stroke();

    // 7. Rooftop Architectural Focal Element
    this.renderArchitecturalCrown(ctx, b, widthPx, heightPx, crownLift, timestamp);

    // 8. Architectural Hover / Active Selection Boundary
    if (isHovered || isSelected) {
      // Crisp neon wireframe bounding contour
      ctx.lineWidth = isSelected ? 2.5 : 1.75;
      ctx.strokeStyle = isSelected ? '#facc15' : varAccent(b.districtId);
      ctx.stroke();

      // Footprint datum frame
      ctx.beginPath();
      ctx.moveTo(0, -2);
      ctx.lineTo(-widthPx - 4, heightPx);
      ctx.lineTo(0, heightPx * 2 + 4);
      ctx.lineTo(widthPx + 4, heightPx);
      ctx.closePath();
      ctx.strokeStyle = isSelected ? '#facc15' : 'rgba(0, 240, 255, 0.8)';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }

    ctx.restore();
  }

  renderFloorPlatesAndMullions(ctx, b, w, h, bh, accent, timestamp) {
    const floorLevels = Math.min(12, Math.floor(b.floors / 3.8));
    const bays = 3;

    // Horizontal Floor Slab Linework
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.lineWidth = 0.75;

    for (let f = 1; f <= floorLevels; f++) {
      const yL = (bh / (floorLevels + 1)) * f;

      // Left face floor slab
      ctx.beginPath();
      ctx.moveTo(0, -yL);
      ctx.lineTo(-w, h - yL);
      ctx.stroke();

      // Right face floor slab
      ctx.beginPath();
      ctx.moveTo(0, -yL);
      ctx.lineTo(w, h - yL);
      ctx.stroke();

      // Subtle architectural interior office glow
      for (let c = 1; c <= bays; c++) {
        const isLit = Math.sin(timestamp * 0.0012 + f * 7 + c * 3 + b.floors) > -0.15;
        if (isLit) {
          ctx.fillStyle = 'rgba(255, 255, 255, 0.75)';
          const wx = -w * (c / (bays + 1));
          const wy = h * (c / (bays + 1)) - yL;
          ctx.fillRect(wx - 2, wy - 3, 3, 5);

          const rx = w * (c / (bays + 1));
          const ry = h * (c / (bays + 1)) - yL;
          ctx.fillStyle = accent;
          ctx.fillRect(rx - 1, ry - 3, 3, 5);
        }
      }
    }

    // Vertical Mullion Columns
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 0.5;
    for (let c = 1; c <= bays; c++) {
      const ratio = c / (bays + 1);
      ctx.beginPath();
      ctx.moveTo(-w * ratio, h * ratio);
      ctx.lineTo(-w * ratio, h * ratio - bh);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(w * ratio, h * ratio);
      ctx.lineTo(w * ratio, h * ratio - bh);
      ctx.stroke();
    }
  }

  renderArchitecturalCrown(ctx, b, w, h, lift, timestamp) {
    const cx = 0;
    const cy = h * 0.65 - lift;

    if (b.roofType === 'pulsing_orb') {
      // Agentforce Atlas Spire: Suspended Polyhedral Energy Core
      const pulse = Math.sin(timestamp * 0.004) * 6;
      const gradient = ctx.createRadialGradient(cx, cy - 26, 2, cx, cy - 26, 26 + pulse);
      gradient.addColorStop(0, '#ffffff');
      gradient.addColorStop(0.35, '#c084fc');
      gradient.addColorStop(0.7, 'rgba(168, 85, 247, 0.35)');
      gradient.addColorStop(1, 'transparent');

      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(cx, cy - 26, 26 + pulse, 0, Math.PI * 2);
      ctx.fill();

      // Octahedral Core
      ctx.fillStyle = '#9333ea';
      ctx.beginPath();
      ctx.moveTo(cx, cy - 36);
      ctx.lineTo(cx + 8, cy - 26);
      ctx.lineTo(cx, cy - 16);
      ctx.lineTo(cx - 8, cy - 26);
      ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = '#f3e8ff';
      ctx.lineWidth = 1.2;
      ctx.stroke();

      // Gyroscopic Orbital Gimbal Rings
      ctx.beginPath();
      ctx.ellipse(cx, cy - 26, 20, 8, timestamp * 0.002, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(0, 240, 255, 0.7)';
      ctx.lineWidth = 1.2;
      ctx.stroke();
    } else if (b.roofType === 'beacon') {
      // Calculated Insights Lighthouse: Dynamic 3D Axonometric Light Cone
      const angle = timestamp * 0.0028;
      ctx.fillStyle = '#06b6d4';
      ctx.beginPath();
      ctx.arc(cx, cy - 14, 7, 0, Math.PI * 2);
      ctx.fill();

      ctx.save();
      ctx.beginPath();
      ctx.moveTo(cx, cy - 14);
      ctx.arc(cx, cy - 14, 160, angle - 0.25, angle + 0.25);
      ctx.closePath();
      ctx.fillStyle = 'rgba(6, 182, 212, 0.18)';
      ctx.fill();
      ctx.restore();
    } else if (b.roofType === 'rotating_dome' || b.roofType === 'radar') {
      // Claudeforce Geodesic Observatory Dome
      ctx.beginPath();
      ctx.arc(cx, cy - 10, 11, 0, Math.PI, true);
      ctx.fillStyle = '#1e293b';
      ctx.fill();
      ctx.strokeStyle = '#f97316';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Radar Azimuth Pointer
      const angle = timestamp * 0.035;
      ctx.beginPath();
      ctx.moveTo(cx, cy - 10);
      ctx.lineTo(cx + Math.cos(angle) * 18, cy - 10 + Math.sin(angle) * 9);
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();
    } else if (b.roofType === 'antenna') {
      // Structural Communications Mast with Ruby Strobe
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx, cy - 36);
      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 1.8;
      ctx.stroke();

      const strobe = Math.sin(timestamp * 0.007) > 0.3;
      ctx.fillStyle = strobe ? '#ff453a' : '#450a0a';
      ctx.beginPath();
      ctx.arc(cx, cy - 36, 3.5, 0, Math.PI * 2);
      ctx.fill();
      if (strobe) {
        ctx.strokeStyle = 'rgba(255, 69, 58, 0.6)';
        ctx.stroke();
      }
    } else if (b.roofType === 'helipad') {
      // Headless Skyport Cantilevered Aerospace Deck
      ctx.fillStyle = '#064e3b';
      ctx.beginPath();
      ctx.arc(cx, cy, 15, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.font = '700 11px JetBrains Mono, monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('HXL', cx, cy);
    } else if (b.roofType === 'crystal') {
      // Vector RAG Knowledge Monolith
      const bob = Math.sin(timestamp * 0.004) * 5;
      ctx.fillStyle = '#22d3ee';
      ctx.beginPath();
      ctx.moveTo(cx, cy - 30 + bob);
      ctx.lineTo(cx + 8, cy - 16 + bob);
      ctx.lineTo(cx, cy - 2 + bob);
      ctx.lineTo(cx - 8, cy - 16 + bob);
      ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1.2;
      ctx.stroke();
    }
  }

  renderParticlesAndDrones(ctx, timestamp) {
    // 1. Ingestion / Action Data Packets
    this.particleSystem.packets.forEach(p => {
      const curX = p.fromX + (p.toX - p.fromX) * p.progress;
      const curY = p.fromY + (p.toY - p.fromY) * p.progress;
      const pos = this.gridToScreen(curX, curY);
      const arc = Math.sin(p.progress * Math.PI) * 28;

      ctx.save();
      ctx.fillStyle = p.color;
      ctx.shadowColor = p.color;
      ctx.shadowBlur = 12;
      ctx.beginPath();
      ctx.arc(pos.x, pos.y - arc, p.size || 4.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });

    // 2. Autonomous Coworker Drones (Spatial Waypoint Flight)
    this.particleSystem.drones.forEach((d, i) => {
      const pos = this.gridToScreen(d.currentX, d.currentY);
      const bob = Math.sin(timestamp * 0.005 + i) * 3;
      const altitudeY = pos.y - d.altitude + bob;

      ctx.save();
      // Drop Shadow
      ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
      ctx.beginPath();
      ctx.ellipse(pos.x, pos.y, 8, 4, 0, 0, Math.PI * 2);
      ctx.fill();

      // Drone Chassis
      ctx.fillStyle = d.color;
      ctx.fillRect(pos.x - 5, altitudeY - 3, 10, 5);
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 0.8;
      ctx.strokeRect(pos.x - 5, altitudeY - 3, 10, 5);

      // Rotors
      const angle = timestamp * 0.07;
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(pos.x - 10 + Math.cos(angle) * 5, altitudeY - 5);
      ctx.lineTo(pos.x - 10 - Math.cos(angle) * 5, altitudeY - 5);
      ctx.moveTo(pos.x + 10 + Math.cos(angle) * 5, altitudeY - 5);
      ctx.lineTo(pos.x + 10 - Math.cos(angle) * 5, altitudeY - 5);
      ctx.stroke();

      ctx.restore();
    });
  }

  renderArchitecturalCallouts(ctx, timestamp) {
    // Elegant architectural leader-line callouts anchored to signature landmarks
    const landmarks = [
      { id: 'b_standard_objects', label: 'METADATA SCHEMA CITADEL', sub: 'Standard & Custom SObjects', color: '#38bdf8', dir: -1 },
      { id: 'b_agentforce_core', label: 'ATLAS REASONING ENGINE', sub: 'Autonomous Cognitive Spire', color: '#a855f7', dir: 1 },
      { id: 'b_data_lake', label: 'DATA CLOUD RESERVOIR', sub: 'Unified Context Graph (DLO/DMO)', color: '#06b6d4', dir: 1 },
      { id: 'b_headless_gateway', label: 'HEADLESS 360 SKYPORT', sub: 'The API is the UI // HXL', color: '#10b981', dir: -1 },
      { id: 'b_mcp_context', label: 'DUAL-PLANE MCP TERMINAL', sub: 'Model Context Protocol Hub', color: '#ec4899', dir: 1 }
    ];

    ctx.save();
    landmarks.forEach(lm => {
      const b = this.buildings.find(item => item.id === lm.id);
      if (!b) return;

      const pos = this.gridToScreen(b.gridX + b.width / 2, b.gridY + b.height / 2);
      const anchorY = pos.y - b.floors * 3.2 - 25;
      const offsetLength = 40 * lm.dir;
      const labelX = pos.x + offsetLength;
      const labelY = anchorY - 30;

      // Leader line with node circle
      ctx.beginPath();
      ctx.arc(pos.x, anchorY, 2.5, 0, Math.PI * 2);
      ctx.fillStyle = lm.color;
      ctx.fill();

      ctx.beginPath();
      ctx.moveTo(pos.x, anchorY);
      ctx.lineTo(pos.x + offsetLength * 0.4, labelY);
      ctx.lineTo(labelX, labelY);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.35)';
      ctx.lineWidth = 1;
      ctx.stroke();

      // Typographic callout text
      ctx.font = '700 9px JetBrains Mono, monospace';
      ctx.fillStyle = lm.color;
      ctx.textAlign = lm.dir > 0 ? 'left' : 'right';
      ctx.fillText(lm.label, labelX + (lm.dir > 0 ? 6 : -6), labelY - 3);

      ctx.font = '500 8.5px Plus Jakarta Sans, sans-serif';
      ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
      ctx.fillText(lm.sub, labelX + (lm.dir > 0 ? 6 : -6), labelY + 9);
    });
    ctx.restore();
  }

  renderHoverSpecBadge(ctx, b) {
    const pos = this.gridToScreen(b.gridX + b.width / 2, b.gridY + b.height / 2);
    const sx = this.camera.x + pos.x * this.camera.zoom;
    const sy = this.camera.y + (pos.y - b.floors * 3.2 - 35) * this.camera.zoom;

    ctx.save();
    ctx.font = '600 12px Plus Jakarta Sans, sans-serif';
    const textWidth = ctx.measureText(b.name).width;

    const padX = 14;
    const padY = 8;
    const w = textWidth + padX * 2;
    const h = 32;

    ctx.fillStyle = 'rgba(10, 15, 26, 0.94)';
    ctx.strokeStyle = b.color || '#38bdf8';
    ctx.lineWidth = 1.5;

    ctx.beginPath();
    ctx.roundRect(sx - w / 2, sy - h / 2, w, h, 6);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(b.name, sx, sy);
    ctx.restore();
  }
}

function varAccent(districtId) {
  if (districtId === 'metadata') return '#38bdf8';
  if (districtId === 'automation') return '#f59e0b';
  if (districtId === 'semantic') return '#06b6d4';
  if (districtId === 'headless') return '#10b981';
  if (districtId === 'agentforce') return '#a855f7';
  if (districtId === 'claudeforce') return '#f97316';
  if (districtId === 'mcp') return '#ec4899';
  return '#ffffff';
}
