/**
 * Atlas.js - Dual-Layer Viewport Coordinator
 * Bridges the "Explore" RPG Town Layer and the "Atlas" 2.5D Axonometric Architecture Layer.
 * Manages mode switching, camera transitions, relationship conduits in RPG space,
 * and fast-travel coordinates.
 */

import { sfx } from '../engine/SoundFx.js';

export class AtlasCoordinator {
  constructor({
    canvas,
    topDownWorld,
    player,
    isoCanvas,
    inspector,
    fieldGuide,
    onModeChange
  }) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.topDownWorld = topDownWorld;
    this.player = player;
    this.isoCanvas = isoCanvas;
    this.inspector = inspector;
    this.fieldGuide = fieldGuide;
    this.onModeChange = onModeChange;

    // Modes: 'explore' (RPG Town) or 'atlas' (2.5D Axonometric)
    this.currentMode = 'explore';
    this.showConduits = true;

    // RPG Camera (smooth lerp follow player)
    this.rpgCamera = {
      x: player.x,
      y: player.y,
      zoom: 1.35
    };

    this.bindEvents();
  }

  setMode(newMode) {
    if (this.currentMode === newMode) return;
    this.currentMode = newMode;
    sfx.openModal();

    if (newMode === 'atlas') {
      // Sync isometric camera to player's current grid position
      const gridX = Math.round(this.player.x / 40);
      const gridY = Math.round(this.player.y / 40);
      const centerScreen = this.isoCanvas.gridToScreen(gridX, gridY);
      this.isoCanvas.camera.targetX = this.isoCanvas.width / 2 - centerScreen.x * this.isoCanvas.camera.targetZoom;
      this.isoCanvas.camera.targetY = this.isoCanvas.height / 2 - (centerScreen.y - 100) * this.isoCanvas.camera.targetZoom;
    } else {
      // Sync player near selected isometric building if any
      if (this.isoCanvas.selectedBuilding) {
        const b = this.topDownWorld.buildings.find(item => item.id === this.isoCanvas.selectedBuilding.id);
        if (b) {
          this.player.teleport(b.entranceX, b.entranceY);
        }
      }
    }

    if (this.onModeChange) {
      this.onModeChange(this.currentMode);
    }
  }

  toggleMode() {
    this.setMode(this.currentMode === 'explore' ? 'atlas' : 'explore');
  }

  fastTravel(building) {
    if (this.currentMode === 'explore') {
      this.player.teleport(building.entranceX, building.entranceY);
      this.rpgCamera.x = building.entranceX;
      this.rpgCamera.y = building.entranceY;
      sfx.pulse();
      // Discover if not already
      this.fieldGuide.discover(building);
      this.inspector.show(building);
    } else {
      this.isoCanvas.focusBuilding(building.id);
      this.inspector.show(building);
    }
  }

  bindEvents() {
    // Keyboard 'V' to toggle view modes, 'E' to interact with nearby building
    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      if (e.key === 'v' || e.key === 'V') {
        this.toggleMode();
      } else if (e.key === 'e' || e.key === 'E') {
        if (this.currentMode === 'explore') {
          const nearby = this.topDownWorld.getNearbyBuilding(this.player.x, this.player.y);
          if (nearby) {
            this.fieldGuide.discover(nearby);
            this.inspector.show(nearby);
          }
        }
      }
    });

    // Touch / Click on canvas in Explore mode to move toward target
    this.canvas.addEventListener('click', (e) => {
      if (this.currentMode !== 'explore') return;

      const rect = this.canvas.getBoundingClientRect();
      const clickScreenX = e.clientX - rect.left;
      const clickScreenY = e.clientY - rect.top;

      // Convert screen to world coords
      const worldX = (clickScreenX - this.canvas.width / (2 * (window.devicePixelRatio || 1))) / this.rpgCamera.zoom + this.rpgCamera.x;
      const worldY = (clickScreenY - this.canvas.height / (2 * (window.devicePixelRatio || 1))) / this.rpgCamera.zoom + this.rpgCamera.y;

      // Check if clicked near a building entrance
      const b = this.topDownWorld.buildings.find(item => {
        return Math.hypot(worldX - item.entranceX, worldY - item.entranceY) < 32;
      });

      if (b) {
        this.fastTravel(b);
      }
    });
  }

  update(dt) {
    if (this.currentMode === 'explore') {
      // 1. Update Player Movement with collision against TopDownWorld
      this.player.update(dt, (x, y, w, h) => this.topDownWorld.isColliding(x, y, w, h));

      // 2. Smoothly track camera to player
      this.rpgCamera.x += (this.player.x - this.rpgCamera.x) * 0.12;
      this.rpgCamera.y += (this.player.y - this.rpgCamera.y) * 0.12;

      // 3. Check for discovery of nearby landmarks
      const nearby = this.topDownWorld.getNearbyBuilding(this.player.x, this.player.y, 48);
      if (nearby) {
        this.fieldGuide.discover(nearby);
      }
    }
  }

  render(timestamp = 0) {
    const ctx = this.ctx;
    const dpr = window.devicePixelRatio || 1;
    const screenW = this.canvas.width / dpr;
    const screenH = this.canvas.height / dpr;

    if (this.currentMode === 'explore') {
      // Clean background
      ctx.fillStyle = '#060911';
      ctx.fillRect(0, 0, screenW, screenH);

      ctx.save();
      // Center camera on player in world space
      ctx.translate(screenW / 2, screenH / 2);
      ctx.scale(this.rpgCamera.zoom, this.rpgCamera.zoom);
      ctx.translate(-this.rpgCamera.x, -this.rpgCamera.y);

      // Viewport bounds in world space
      const vp = {
        x: this.rpgCamera.x - (screenW / 2) / this.rpgCamera.zoom,
        y: this.rpgCamera.y - (screenH / 2) / this.rpgCamera.zoom,
        width: screenW / this.rpgCamera.zoom,
        height: screenH / this.rpgCamera.zoom
      };

      // 1. Render TopDown RPG World (Terrain, Shoreline, Y-Sorted Entities & Player)
      this.topDownWorld.render(ctx, this.player, vp, timestamp);

      // 2. Render Conduits Overlay in RPG mode if enabled
      if (this.showConduits) {
        this.renderRpgConduits(ctx, timestamp);
      }

      ctx.restore();

      // 3. Screen HUD in RPG Mode (Minimap / Zone indicator)
      this.renderRpgHud(ctx, screenW, screenH);

    } else {
      // Render the 2.5D Isometric Architectural Masterplan
      this.isoCanvas.render(timestamp);
    }
  }

  renderRpgConduits(ctx, timestamp) {
    ctx.save();
    this.topDownWorld.catalog.conduits.forEach(c => {
      const b1 = this.topDownWorld.buildings.find(b => b.id === c.from);
      const b2 = this.topDownWorld.buildings.find(b => b.id === c.to);
      if (!b1 || !b2) return;

      let strokeColor = 'rgba(56, 189, 248, 0.45)';
      if (c.type === 'automation') strokeColor = 'rgba(245, 158, 11, 0.45)';
      if (c.type === 'semantic') strokeColor = 'rgba(6, 182, 212, 0.45)';
      if (c.type === 'agentforce') strokeColor = 'rgba(168, 85, 247, 0.5)';
      if (c.type === 'claudeforce') strokeColor = 'rgba(249, 115, 22, 0.5)';
      if (c.type === 'mcp') strokeColor = 'rgba(236, 72, 153, 0.5)';
      if (c.type === 'headless') strokeColor = 'rgba(16, 185, 129, 0.5)';

      // Draw dashed energy conduit between building entrances
      ctx.beginPath();
      ctx.moveTo(b1.entranceX, b1.entranceY);
      ctx.lineTo(b2.entranceX, b2.entranceY);
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Discrete data pulse traveling along conduit
      ctx.setLineDash([4, 12]);
      ctx.lineDashOffset = -timestamp * 0.035;
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.setLineDash([]);
    });
    ctx.restore();
  }

  renderRpgHud(ctx, screenW, screenH) {
    // Current District Badge at bottom-left
    const currentDistrict = this.getCurrentDistrict();
    ctx.save();

    // Zone Pill
    ctx.fillStyle = 'rgba(8, 12, 22, 0.85)';
    ctx.strokeStyle = currentDistrict.color;
    ctx.lineWidth = 1.2;

    const pillW = 220;
    const pillH = 34;
    const pillX = 20;
    const pillY = screenH - 72;

    ctx.beginPath();
    ctx.roundRect(pillX, pillY, pillW, pillH, 8);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = currentDistrict.color;
    ctx.font = '700 9px JetBrains Mono, monospace';
    ctx.fillText('ZONE: ' + currentDistrict.id.toUpperCase(), pillX + 12, pillY + 14);

    ctx.fillStyle = '#ffffff';
    ctx.font = '600 11.5px Plus Jakarta Sans, sans-serif';
    ctx.fillText(currentDistrict.name, pillX + 12, pillY + 27);

    ctx.restore();
  }

  getCurrentDistrict() {
    const gx = Math.floor(this.player.x / 40);
    const gy = Math.floor(this.player.y / 40);

    if (gx <= 8 && gy <= 8) return { id: 'metadata', name: 'Metadata Citadel', color: '#38bdf8' };
    if (gx >= 9 && gx <= 16 && gy <= 8) return { id: 'automation', name: 'Logic & Automation Grid', color: '#f59e0b' };
    if (gx >= 17 && gy <= 9) return { id: 'semantic', name: 'Data Cloud & Semantic Harbor', color: '#06b6d4' };
    if (gx <= 8 && gy >= 13) return { id: 'headless', name: 'Headless 360 Skyport', color: '#10b981' };
    if (gx >= 9 && gx <= 15 && gy >= 9 && gy <= 16) return { id: 'agentforce', name: 'Agentforce Autonomous Forum', color: '#a855f7' };
    if (gx >= 16 && gx <= 20 && gy >= 10 && gy <= 15) return { id: 'claudeforce', name: 'Claudeforce Research Complex', color: '#f97316' };
    if (gx >= 15 && gy >= 16) return { id: 'mcp', name: 'Dual-Plane MCP Interchange', color: '#ec4899' };

    return { id: 'commons', name: 'Salesforce Metropolitan Commons', color: '#94a3b8' };
  }
}
