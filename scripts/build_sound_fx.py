sound_fx_code = '''/**
 * Synthesized 8-Bit Web Audio API Sound System
 * Zero external audio files required. Crisp retro synthesizer sound fx.
 */

class SoundFx {
  constructor() {
    this.ctx = null;
    this.muted = false;
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.ctx = new AudioContext();
        this.initialized = true;
      }
    } catch (e) {
      console.warn('Web Audio not supported or blocked:', e);
    }
  }

  toggleMute() {
    this.muted = !this.muted;
    return this.muted;
  }

  playBeep(freq = 440, duration = 0.08, type = 'square', gainVal = 0.08) {
    if (this.muted) return;
    this.init();
    if (!this.ctx) return;

    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }

    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

      gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch (e) {
      // Audio autoplay policy catch
    }
  }

  click() {
    this.playBeep(520, 0.05, 'triangle', 0.06);
  }

  buildingSelect() {
    if (this.muted) return;
    this.playBeep(440, 0.06, 'square', 0.08);
    setTimeout(() => this.playBeep(660, 0.09, 'square', 0.08), 50);
  }

  districtSelect() {
    if (this.muted) return;
    this.playBeep(330, 0.06, 'triangle', 0.08);
    setTimeout(() => this.playBeep(495, 0.06, 'triangle', 0.08), 60);
    setTimeout(() => this.playBeep(660, 0.12, 'square', 0.09), 120);
  }

  pulse() {
    if (this.muted) return;
    this.playBeep(880, 0.04, 'sine', 0.04);
  }

  simulationStep() {
    if (this.muted) return;
    this.playBeep(587.33, 0.08, 'sawtooth', 0.06);
    setTimeout(() => this.playBeep(880, 0.1, 'square', 0.07), 70);
  }

  openModal() {
    if (this.muted) return;
    this.playBeep(392, 0.05, 'triangle', 0.06);
    setTimeout(() => this.playBeep(523.25, 0.08, 'triangle', 0.07), 50);
    setTimeout(() => this.playBeep(784, 0.12, 'square', 0.08), 100);
  }

  closeModal() {
    if (this.muted) return;
    this.playBeep(659.25, 0.05, 'triangle', 0.06);
    setTimeout(() => this.playBeep(440, 0.08, 'triangle', 0.05), 50);
  }
}

export const sfx = new SoundFx();
'''

with open('/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer/src/engine/SoundFx.js', 'w') as f:
    f.write(sound_fx_code)

print("SoundFx.js written successfully!")
