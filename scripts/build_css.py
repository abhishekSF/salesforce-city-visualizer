css_code = '''/* 2.5D Salesforce Org Pixel City Stylesheet */

@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

:root {
  --font-pixel: 'Press Start 2P', monospace;
  --font-mono: 'Space Mono', monospace;
  --color-bg: #070b14;
  --color-panel: #0f172a;
  --color-border: #1e293b;
  --color-accent: #38bdf8;
}

body {
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: var(--color-bg);
  color: #f8fafc;
  font-family: var(--font-mono);
  user-select: none;
}

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
}

.pixel-btn:active {
  transform: translate(2px, 2px);
  box-shadow: 0 0 0 0 #0f172a;
}

/* CRT Scanlines Overlay (Toggleable) */
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

/* Pulse Glows */
@keyframes neon-pulse {
  0%, 100% {
    box-shadow: 0 0 5px rgba(56, 189, 248, 0.4), 0 0 15px rgba(56, 189, 248, 0.2);
  }
  50% {
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.8), 0 0 25px rgba(56, 189, 248, 0.5);
  }
}

.glow-active {
  animation: neon-pulse 2s infinite ease-in-out;
}
'''

with open('/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer/src/styles/pixel-city.css', 'w') as f:
    f.write(css_code)

print("pixel-city.css written successfully!")
