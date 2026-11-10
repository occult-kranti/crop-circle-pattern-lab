# Intake: occult-kranti/brainwave_opensync — Cymatics Engine

Cloned to `brainwave_opensync/` (HEAD `336e3fe`, 2026-11-09). MIT License (2026, Open Sync contributors). React/TS Vite app ("Open Sync"). The GitHub Pages URL `.../archive/cymatics/` serves only the SPA shell (3.6 KB index.html, title "Open Sync — A space to listen") — no static cymatics archive content; the real engine is in the repo source.

## Cymatics engine location
Canonical tree: `src/cymatics/` (superset). `integrations/open-sync/src/cymatics/` is a near-duplicate minus `plate3d.ts` and `instrument/`, with a 9-line diff in `render.ts`.

### `chladni.ts` (857 lines) — pure numeric core, node-testable
- **Square plate**: `squarePlateValue(x,y,n,m,sign)` — Bourke cos-form `cos(nπx)cos(mπy) − sign·cos(mπx)cos(nπy)`; `squarePlateValueMix(x,y,n,m,a,b)` — sin-form degenerate mix `a·sin(nπx)sin(mπy)+b·sin(mπx)sin(nπy)`, fractional n/m allowed ("art mode" morphing); `isTrivialMix` degenerate-case guard.
- **Circular plate**: `circularPlateValue(r,θ,m,s,boundary)` = `J_m(k·r)·cos(mθ)` normalized; hardcoded Bessel zero tables `BESSEL_ZEROS` (J_m zeros, m=0..5, A&S Table 9.5) and `BESSEL_DERIVATIVE_ZEROS` (J'_m zeros, free rim); own power-series `besselJ` (accurate |x|≲25); `circularWaveNumber`, `circularPlateNorm`.
- **Virtual plates** (`VIRTUAL_PLATES`): 5 declared plates (steel square 30 cm @180 Hz, glass 25 cm @320, plywood 40 cm @95, steel disc Ø17 cm @110 free-rim, ideal membrane @120) with shape/material/fundamental/boundary/scaling — this is the "honest" frequency→pattern anchor.
- **Eigenfrequency ladders**: `squareEigenvalue` (plate: f∝n²+m²; membrane: f∝√(n²+m²)); `frequencyToModes(hz, shape, opts)` → ranked `ModeCandidate[]` with relError/tolerance; `squareModeHz`, `circularModeHz` (thin-plate ω∝k² referenced to (0,1) mode).
- **Driven-plate physics**: `drivenSquareModes`/`drivenCircularModes` — Lorentzian resonance weights w∝1/((f−f_mn)²+γ²), γ default 6% of drive (Tuan et al. 2018 model re-implemented); `drivenSquareField`/`drivenCircularField` build weighted superposition fields.
- **Sand sim**: `createSand` (seeded mulberry32 PRNG, uniform disk/square), `stepParticles` (Euler drift down −∇|field| + seeded jitter, allocation-free, deterministic), `meanParticleAbs`.
- **Grids/stats**: `computeAbsGrid`, `nodalCount`, `nodalFraction`, `squareNodalLineEstimate`, `squareNodalCrossings` (scanline sign-change counting — monotonic in mode order).
- Explicit HONESTY NOTE in header: Hz does not determine a real plate pattern; engine simulates idealized virtual plates.

### `render.ts` (252 lines)
- 6 low-saturation colormaps (`amber-grain`, `gold-plate` photo-matched, `teal-glow`, `monochrome`, `inferno-warm`, `spectrum-lab`); `sampleColormap` NaN/clamp-safe.
- `renderToBuffer(w,h,params)` → RGBA typed array (DOM-free): |f|^p sharpening (p≈0.25), Gaussian ridge `exp(−t²/2σ²)` nodal-line emphasis, energy boost; 'lines' and 'sand' modes; 40k particle cap with stride-skip; `renderFrame` canvas wrapper.

### `plate3d.ts` (380 lines, src only)
- 3D terrain renderer, pure canvas (no WebGL): z = displacement×amp; gold palette sampled from a photographed Chladni figure; pure core (`projectPoint`, `fieldHeight`, `rampGold`) + `drawPlate3D`; page also has `plate5d` mode (`drawPlate5D`, higher-projection gimmick) and a `useField4d` hook used across other lab pages.

### `audioLink.ts` (136 lines)
- Decoupled `AnalyserLike` structural interface; `sampleAudioFeatures` (peak Hz, centroid, energy, silence gate −84 dBFS, never throws); `driveFromFeatures` → physics mode (Lorentzian superposition) or art mode (nearest ladder rung); `smoothDriveHz` one-pole smoother for glide.

### `presets.ts` (229 lines)
- `CymaticPreset` with explicit `label: 'physics'|'art'` honesty contract + per-preset note. Sets: explicit eigenmodes, 440/432 comparison, Schumann modes 7.83–32 Hz octave-folded with citations (Balser & Wagner 1960; Hylaty 2016), 40 Hz gamma fold (with contested-evidence caveat), alpha 10 Hz fold, Solfeggio set explicitly labeled "cultural, not physical (Puleo/Horowitz numerology)".

### `instrument/` (src only, ~1.1k lines)
- `Instrument.tsx`: performance-instrument UI — views Sand/Liquid/Lissajous/Nodal-Ink, sources Tone/Studio/Mic/File/Tab, effects Natural/Mono/Mirror/Halftone; `Capture.ts`: MediaRecorder webm/mp4 capture (30 s cap, 4 Mbps); `signal.ts`, `scenes.ts`, `useInstrumentInput.ts`, custom CSS.

### Pages
- `PrecisionCymatics.tsx` (934 lines): full Cymatic Studio — plate selector, physics/art interpretation toggle, drive modes (manual/frequency/audio), n/m/sign + mix sliders, render modes lines/sand/plate3d/plate5d, colormaps, threshold/particles/speed/resolution/seed, PNG export, "hear this pattern" tone, info panel, coach tour, a11y labels.
- `Cymatics.tsx` (32 lines) thin wrapper; `StudioCymatics.tsx`/`CymaticsOverlay.tsx` studio integrations.

### Tests (`src/cymatics/__tests__/`)
`chladni.test.ts` (300), `render.test.ts` (182), `presets.test.ts` (109), `plate3d.test.ts` (162), `freeplate-regression.test.ts` (16), `instrument.test.ts` (28). Vitest; numeric core is DOM-free by design.

## vs. our existing cymatics code (`/mnt/agents/output/cymatics/code/`, Python)
Our engine is a **reverse decoder** (pattern → modes): scipy `jn_zeros`/`jn` (n≤100, m≤20 + asymptotic fallback), membrane + square forward models, `decode_image` pipeline (angular FFT, Bessel-ratio radial matching via Hungarian assignment, log-polar spiral test, grid comb), structural rules R1–R11, top-3 candidates with confidence, `notes.py` presentation. Their engine is a **forward simulator/renderer** (Hz → pattern) with UI. Complementary, little overlap.

## What to port for Cymatics Lab v2 (website is static HTML/JS)
1. **Driven-plate Lorentzian superposition** (`drivenSquareModes/Field`, `drivenCircularModes/Field`) — the single biggest realism upgrade; our lab currently shows single modes.
2. **Virtual plates concept + `VIRTUAL_PLATES` data + eigenfrequency ladders** (`frequencyToModes`, scaling laws) — gives the honest Hz→mode mapping for monuments/Chladni page.
3. **Circular plate with free-rim boundary** (`BESSEL_DERIVATIVE_ZEROS`) — our Python table only has clamped J_m zeros; relevant to monument resonator modeling.
4. **Bourke cos-form square plate + sin-form mix with fractional modes** — richer than our plain sin(pπx)sin(qπy).
5. **Renderer tricks**: |f|^p sharpening, Gaussian ridge lines, colormaps, sand-particle gradient sim (TS→JS port is mechanical; core is DOM-free typed arrays).
6. **Honesty-labeling convention** (physics/art labels + per-preset notes) — adopt verbatim as a UX pattern for the site.
7. Audio-reactive link (`audioLink.ts`) if the lab gets a tone generator.

## Merge strategy
- Keep our Python reverse-decoder stack untouched (it feeds monuments.py/crossmatch.py in Wave 2); port the TS forward engine to a standalone ES module (e.g. `cymatics-engine.js`) for the website Cymatics Lab. The TS core is already DOM-free and dependency-free, so port ≈ transliteration (~1.5k lines for chladni+render+presets; skip React pages, plate5d gimmick optional, instrument optional).
- Optionally cross-validate: port Lorenztian/free-rim additions back into Python `cymatics.py` so forward models used by monuments.py share one physics base (scipy zeros already more accurate than their hardcoded tables — keep scipy).
- License: MIT — free to port; add attribution note ("engine adapted from Open Sync, MIT").
- Stress test: extend `test_cymatics.py` with parity checks between Python and ported JS outputs (e.g. Bessel zero tables, mode Hz ladders, Lorentzian weights) and repo's own vitest suites as reference vectors.
