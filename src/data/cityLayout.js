/**
 * City layout grid definition for 2.5D Isometric Salesforce Org Visualizer.
 * 28x28 isometric grid with thematic districts, roads, waterways, and conduits.
 */

export const GRID_SIZE = 28;
export const TILE_WIDTH = 64;
export const TILE_HEIGHT = 32;

// Tile types:
// 0: Grass / Cyber Turf
// 1: Paved Road
// 2: Glowing Fiber-Optic Data Highway
// 3: Water (Data Lake Reservoir)
// 4: Building Foundation / Concrete Pad
// 5: Tech Plaza / Stone Cobble
// 6: Maglev Transit Track

export function generateTileMap() {
  const map = [];
  for (let y = 0; y < GRID_SIZE; y++) {
    const row = [];
    for (let x = 0; x < GRID_SIZE; x++) {
      // Default ground
      let type = 0;

      // Data Lake reservoir in North-East (x >= 18 and y <= 8)
      if (x >= 18 && y <= 6) {
        type = 3;
      }

      // Main East-West Highway (y = 10, y = 11)
      if (y === 10 || y === 11) {
        type = (x % 2 === 0) ? 2 : 1;
      }

      // Main North-South Highway (x = 10, x = 11)
      if (x === 10 || x === 11) {
        type = (y % 2 === 0) ? 2 : 1;
      }

      // Secondary roads
      if (y === 5 || y === 18) {
        if (type !== 3) type = 1;
      }
      if (x === 5 || x === 18) {
        if (type !== 3) type = 1;
      }

      // Maglev Track to MCP Interchange (South-East loop)
      if ((x >= 15 && y >= 17) && (x === 15 || y === 17 || x === 24 || y === 24)) {
        type = 6;
      }

      // Central Agentforce Plaza (x: 10-15, y: 10-15)
      if (x >= 11 && x <= 14 && y >= 11 && y <= 14) {
        type = 5;
      }

      row.push(type);
    }
    map.push(row);
  }
  return map;
}

export const DRONE_PATHS = [
  // Kaveri Autonomous Drone: Semantic Harbor -> Agentforce Core -> Headless 360
  [
    { x: 19, y: 4 },
    { x: 18, y: 8 },
    { x: 13, y: 12 },
    { x: 6, y: 18 },
    { x: 3, y: 15 },
    { x: 13, y: 12 }
  ],
  // Claudeforce Co-Pilot Drone: Claudeforce Lab -> Apex Foundry -> Metadata Citadel
  [
    { x: 17, y: 13 },
    { x: 14, y: 5 },
    { x: 4, y: 4 },
    { x: 10, y: 12 },
    { x: 17, y: 13 }
  ],
  // MCP Transit Shuttle: MCP Interchange -> Agentforce -> Security Citadel
  [
    { x: 16, y: 20 },
    { x: 20, y: 17 },
    { x: 12, y: 12 },
    { x: 6, y: 2 },
    { x: 16, y: 20 }
  ]
];
