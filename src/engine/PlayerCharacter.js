/**
 * PlayerCharacter.js - The "Salesforce Explorer"
 * Handcrafted retro RPG explorer with 4-directional walk cycles,
 * sub-pixel smooth movement, collision handling, and subtle idle animation.
 */

export class PlayerCharacter {
  constructor(worldX = 420, worldY = 420) {
    this.x = worldX;
    this.y = worldY;
    this.vx = 0;
    this.vy = 0;
    this.speed = 150; // pixels per second

    this.width = 24;
    this.height = 32;
    // Collision box anchored at feet
    this.collider = {
      offsetX: -9,
      offsetY: -6,
      width: 18,
      height: 12
    };

    // Facing: 'down', 'up', 'left', 'right'
    this.facing = 'down';
    this.isMoving = false;

    // Animation state
    this.animTimer = 0;
    this.animFrame = 0;
    this.idleTimer = 0;

    // Input state
    this.keys = {
      up: false,
      down: false,
      left: false,
      right: false
    };

    this.bindInputs();
  }

  bindInputs() {
    if (typeof window === "undefined") return;
    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      if (e.key === 'w' || e.key === 'W' || e.key === 'ArrowUp') {
        this.keys.up = true;
      } else if (e.key === 's' || e.key === 'S' || e.key === 'ArrowDown') {
        this.keys.down = true;
      } else if (e.key === 'a' || e.key === 'A' || e.key === 'ArrowLeft') {
        this.keys.left = true;
      } else if (e.key === 'd' || e.key === 'D' || e.key === 'ArrowRight') {
        this.keys.right = true;
      }
    });

    window.addEventListener('keyup', (e) => {
      if (e.key === 'w' || e.key === 'W' || e.key === 'ArrowUp') {
        this.keys.up = false;
      } else if (e.key === 's' || e.key === 'S' || e.key === 'ArrowDown') {
        this.keys.down = false;
      } else if (e.key === 'a' || e.key === 'A' || e.key === 'ArrowLeft') {
        this.keys.left = false;
      } else if (e.key === 'd' || e.key === 'D' || e.key === 'ArrowRight') {
        this.keys.right = false;
      }
    });
  }

  update(dt, collisionChecker) {
    let dx = 0;
    let dy = 0;

    if (this.keys.up) dy -= 1;
    if (this.keys.down) dy += 1;
    if (this.keys.left) dx -= 1;
    if (this.keys.right) dx += 1;

    this.isMoving = (dx !== 0 || dy !== 0);

    if (this.isMoving) {
      // Normalize diagonal speed
      const len = Math.hypot(dx, dy);
      dx /= len;
      dy /= len;

      // Update facing direction
      if (Math.abs(dx) > Math.abs(dy)) {
        this.facing = dx > 0 ? 'right' : 'left';
      } else {
        this.facing = dy > 0 ? 'down' : 'up';
      }

      // Step animation
      this.animTimer += dt * 8;
      this.animFrame = Math.floor(this.animTimer) % 4;

      // Calculate desired new position with delta time
      const moveDistance = this.speed * dt;
      const targetX = this.x + dx * moveDistance;
      const targetY = this.y + dy * moveDistance;

      // Attempt full move, or slide on collision
      if (collisionChecker) {
        // Try X move
        if (!collisionChecker(targetX + this.collider.offsetX, this.y + this.collider.offsetY, this.collider.width, this.collider.height)) {
          this.x = targetX;
        }
        // Try Y move
        if (!collisionChecker(this.x + this.collider.offsetX, targetY + this.collider.offsetY, this.collider.width, this.collider.height)) {
          this.y = targetY;
        }
      } else {
        this.x = targetX;
        this.y = targetY;
      }
    } else {
      this.animFrame = 0;
      this.idleTimer += dt;
    }
  }

  teleport(newX, newY) {
    this.x = newX;
    this.y = newY;
    this.animFrame = 0;
    this.isMoving = false;
  }

  render(ctx) {
    const px = Math.round(this.x);
    const py = Math.round(this.y);

    ctx.save();
    ctx.translate(px, py);

    // 1. Soft Oval Ground Shadow
    ctx.fillStyle = 'rgba(0, 0, 0, 0.35)';
    ctx.beginPath();
    ctx.ellipse(0, 0, 10, 5, 0, 0, Math.PI * 2);
    ctx.fill();

    // Subtle idle breathing offset
    const idleBob = this.isMoving ? (this.animFrame % 2 === 1 ? -1 : 0) : Math.sin(this.idleTimer * 2.5) * 0.75;
    ctx.translate(0, idleBob);

    // 2. Render Handcrafted Sprite Layers
    this.renderSprite(ctx);

    ctx.restore();
  }

  renderSprite(ctx) {
    const f = this.facing;
    const walk = this.animFrame; // 0, 1, 2, 3

    // Leg offsets for walk animation
    let leftLegY = 0;
    let rightLegY = 0;
    if (this.isMoving) {
      if (walk === 0) { leftLegY = -3; rightLegY = 2; }
      else if (walk === 1) { leftLegY = 0; rightLegY = 0; }
      else if (walk === 2) { leftLegY = 2; rightLegY = -3; }
      else if (walk === 3) { leftLegY = 0; rightLegY = 0; }
    }

    // --- LEGS & BOOTS ---
    ctx.fillStyle = '#334155'; // Dark Navy Trousers
    if (f === 'down' || f === 'up') {
      ctx.fillRect(-6, -8 + leftLegY, 5, 8);
      ctx.fillRect(1, -8 + rightLegY, 5, 8);

      // Brown Boots
      ctx.fillStyle = '#78350f';
      ctx.fillRect(-6, -3 + leftLegY, 5, 4);
      ctx.fillRect(1, -3 + rightLegY, 5, 4);
    } else if (f === 'left') {
      ctx.fillRect(-4, -8 + leftLegY, 6, 8);
      ctx.fillStyle = '#78350f';
      ctx.fillRect(-6, -3 + leftLegY, 7, 4);
    } else if (f === 'right') {
      ctx.fillRect(-2, -8 + rightLegY, 6, 8);
      ctx.fillStyle = '#78350f';
      ctx.fillRect(-1, -3 + rightLegY, 7, 4);
    }

    // --- BACKPACK (drawn behind body if facing up/left/right) ---
    if (f === 'up') {
      ctx.fillStyle = '#b45309'; // Leather backpack
      ctx.fillRect(-7, -22, 14, 12);
      ctx.fillStyle = '#92400e';
      ctx.fillRect(-6, -24, 12, 4); // Bedroll / sleeping roll
      ctx.strokeStyle = '#451a03';
      ctx.lineWidth = 1;
      ctx.strokeRect(-7, -22, 14, 12);
    } else if (f === 'left') {
      ctx.fillStyle = '#b45309';
      ctx.fillRect(2, -22, 5, 12);
    } else if (f === 'right') {
      ctx.fillStyle = '#b45309';
      ctx.fillRect(-7, -22, 5, 12);
    }

    // --- TORSO & ADVENTURER JACKET ---
    ctx.fillStyle = '#0284c7'; // Salesforce Cerulean Blue Jacket
    ctx.fillRect(-6, -20, 12, 13);

    // Collar / Utility Vest Trim
    ctx.fillStyle = '#f8fafc'; // White shirt / trim
    if (f === 'down') {
      ctx.fillRect(-2, -20, 4, 6);
      // Utility pockets
      ctx.fillStyle = '#0369a1';
      ctx.fillRect(-5, -13, 4, 4);
      ctx.fillRect(1, -13, 4, 4);
      // Explorer belt & gold buckle
      ctx.fillStyle = '#78350f';
      ctx.fillRect(-6, -9, 12, 2);
      ctx.fillStyle = '#fbbf24';
      ctx.fillRect(-1.5, -9.5, 3, 3);
    } else if (f === 'left') {
      ctx.fillStyle = '#0369a1';
      ctx.fillRect(-4, -13, 4, 4);
      ctx.fillStyle = '#78350f';
      ctx.fillRect(-6, -9, 11, 2);
    } else if (f === 'right') {
      ctx.fillStyle = '#0369a1';
      ctx.fillRect(0, -13, 4, 4);
      ctx.fillStyle = '#78350f';
      ctx.fillRect(-5, -9, 11, 2);
    }

    // --- ARMS ---
    ctx.fillStyle = '#0284c7';
    let armSwing = this.isMoving ? Math.sin(this.animTimer * 2) * 2 : 0;
    if (f === 'down') {
      ctx.fillRect(-8, -20 + armSwing, 3, 9);
      ctx.fillRect(5, -20 - armSwing, 3, 9);
      // Hands
      ctx.fillStyle = '#fed7aa';
      ctx.fillRect(-8, -11 + armSwing, 3, 2.5);
      ctx.fillRect(5, -11 - armSwing, 3, 2.5);
    } else if (f === 'up') {
      ctx.fillRect(-8, -20 - armSwing, 3, 9);
      ctx.fillRect(5, -20 + armSwing, 3, 9);
    } else if (f === 'left') {
      ctx.fillRect(-4, -20 + armSwing, 3, 9);
      ctx.fillStyle = '#fed7aa';
      ctx.fillRect(-4, -11 + armSwing, 3, 2.5);
    } else if (f === 'right') {
      ctx.fillRect(1, -20 - armSwing, 3, 9);
      ctx.fillStyle = '#fed7aa';
      ctx.fillRect(1, -11 - armSwing, 3, 2.5);
    }

    // --- HEAD & FACE ---
    ctx.fillStyle = '#fed7aa'; // Skin Tone
    ctx.fillRect(-5, -28, 10, 9);

    if (f === 'down') {
      // Eyes
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(-3, -24, 2, 2.5);
      ctx.fillRect(1, -24, 2, 2.5);
      // Eye glint
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(-3, -24, 1, 1);
      ctx.fillRect(1, -24, 1, 1);
    } else if (f === 'left') {
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(-4, -24, 2, 2.5);
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(-4, -24, 1, 1);
    } else if (f === 'right') {
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(2, -24, 2, 2.5);
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(3, -24, 1, 1);
    }

    // --- HAIR & EXPLORER CAP ---
    ctx.fillStyle = '#451a03'; // Brown Hair
    if (f === 'down') {
      ctx.fillRect(-6, -29, 12, 3);
      ctx.fillRect(-6, -26, 2, 4);
      ctx.fillRect(4, -26, 2, 4);
    } else if (f === 'up') {
      ctx.fillRect(-6, -29, 12, 8);
    } else if (f === 'left') {
      ctx.fillRect(-5, -29, 11, 4);
      ctx.fillRect(2, -27, 3, 5);
    } else if (f === 'right') {
      ctx.fillRect(-6, -29, 11, 4);
      ctx.fillRect(-5, -27, 3, 5);
    }

    // Explorer Cap / Headband with Gold Badge
    ctx.fillStyle = '#0369a1';
    ctx.fillRect(-7, -32, 14, 4);
    // Cap brim
    if (f === 'down') {
      ctx.fillRect(-8, -29, 16, 2);
      ctx.fillStyle = '#f59e0b'; // Gold Cloud Badge
      ctx.fillRect(-2, -32, 4, 3);
    } else if (f === 'left') {
      ctx.fillRect(-9, -29, 14, 2);
    } else if (f === 'right') {
      ctx.fillRect(-5, -29, 14, 2);
    } else if (f === 'up') {
      ctx.fillRect(-7, -29, 14, 2);
    }

    // Subtle 1px crisp outline around character silhouette
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.4)';
    ctx.lineWidth = 0.75;
    ctx.strokeRect(-6.5, -32.5, 13, 31);
  }
}
