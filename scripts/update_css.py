css_content = '''/* 2.5D Salesforce Org Pixel City Stylesheet */

@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

:root {
  --font-pixel: 'Press Start 2P', monospace;
  --font-mono: 'Space Mono', monospace, -apple-system, sans-serif;
  --color-bg: #070b14;
  --color-panel: #0f172a;
  --color-border: #1e293b;
  --color-accent: #38bdf8;
}

*, *::before, *::after {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: var(--color-bg);
  color: #f8fafc;
  font-family: var(--font-mono);
  user-select: none;
  position: relative;
}

/* Canvas absolute positioning */
#city-canvas {
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  display: block !important;
  z-index: 1 !important;
  background-color: #070b14;
}

/* Essential utilities guaranteed regardless of Tailwind */
.hidden {
  display: none !important;
}

.absolute { position: absolute; }
.relative { position: relative; }
.fixed { position: fixed; }
.inset-0 { top: 0; right: 0; bottom: 0; left: 0; }
.w-full { width: 100%; }
.h-full { height: 100%; }
.flex { display: flex; }
.grid { display: grid; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.justify-center { justify-content: center; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }
.flex-1 { flex: 1 1 0%; }
.gap-1 { gap: 0.25rem; }
.gap-2 { gap: 0.5rem; }
.gap-3 { gap: 0.75rem; }
.gap-4 { gap: 1rem; }

/* Pixel panel box shadows and borders */
.pixel-panel {
  background: rgba(15, 23, 42, 0.95);
  border: 2px solid #334155;
  box-shadow: 0 0 0 2px #0f172a, 4px 4px 0 2px rgba(0, 0, 0, 0.6);
}

.pixel-btn {
  font-family: var(--font-mono);
  border: 2px solid #475569;
  box-shadow: 2px 2px 0 0 #0f172a;
  transition: all 0.1s ease;
  cursor: pointer;
}

.pixel-btn:active {
  transform: translate(2px, 2px);
  box-shadow: 0 0 0 0 #0f172a;
}

button {
  cursor: pointer;
  font-family: inherit;
}

/* CRT Scanlines Overlay */
.scanlines {
  background: linear-gradient(
    rgba(18, 16, 16, 0) 50%, 
    rgba(0, 0, 0, 0.25) 50%
  ), linear-gradient(
    90deg,
    rgba(255, 0, 0, 0.03),
    rgba(0, 255, 0, 0.01),
    rgba(0, 0, 255, 0.03)
  );
  background-size: 100% 3px, 6px 100%;
  pointer-events: none;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 5;
  opacity: 0.35;
}

/* Custom Pixel Scrollbars */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #090d16;
}

::-webkit-scrollbar-thumb {
  background: #334155;
  border-radius: 2px;
}

::-webkit-scrollbar-thumb:hover {
  background: #475569;
}

/* Navigation headers and UI overlays */
header.app-header {
  position: absolute;
  top: 12px;
  left: 12px;
  right: 12px;
  z-index: 20;
  background: rgba(15, 23, 42, 0.92);
  backdrop-filter: blur(8px);
  border: 2px solid #334155;
  border-radius: 8px;
  padding: 10px 14px;
}

footer.app-footer {
  position: absolute;
  bottom: 12px;
  left: 12px;
  right: 12px;
  z-index: 20;
  background: rgba(15, 23, 42, 0.92);
  backdrop-filter: blur(8px);
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 8px 12px;
}

#building-inspector {
  position: absolute;
  top: 75px;
  right: 12px;
  bottom: 58px;
  width: 380px;
  max-width: calc(100vw - 24px);
  z-index: 30;
  background: rgba(15, 23, 42, 0.96);
  backdrop-filter: blur(12px);
  border: 2px solid #38bdf8;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
  overflow: hidden;
}

#sim-banner {
  position: absolute;
  top: 75px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 30;
  width: 90%;
  max-width: 580px;
  background: rgba(15, 23, 42, 0.96);
  border: 2px solid #10b981;
  border-radius: 8px;
  padding: 12px 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
}
'''

with open('/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer/src/styles/pixel-city.css', 'w') as f:
    f.write(css_content)

print("Updated pixel-city.css successfully!")
