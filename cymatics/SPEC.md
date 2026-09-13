# SPEC — Reverse Cymatic Decoder (implementation contract)

## Mission
Build a pure-Python (numpy/scipy/matplotlib) toolkit that:
1. Simulates cymatic nodal-line patterns (forward: modes → pattern image).
2. Decodes geometric patterns (structural descriptors and/or synthetic images) into candidate vibration modes (n, m) with confidence.
3. Converts modes → frequencies on reference resonators → musical notes, beat/"difference vibration" tables.

## Consultant specs (READ THESE FIRST — they are authoritative)
- Physics: /mnt/agents/output/1a0782fe-bb82-80eb-8000-0f3b0e2dc667/reverse_cymatic_decoder_spec.md
- Math/algorithms: /mnt/agents/output/1a0782fe-bcd2-8a43-8000-0f3b58c559ba/reverse_cymatic_decoder.md
- Presentation/acoustics: /mnt/agents/output/cymatic_presentation_spec.md

## Files to create in /mnt/agents/output/cymatics/code/
- `cymatics.py` — forward models:
  - `bessel_zeros()` — table of z_{n,m} for n=0..8, m=1..6 (scipy) + asymptotic fallback for beyond-table.
  - `membrane_pattern(n, m, R=1.0, res=512, phase=0, weight=1.0)` and `membrane_superposition(modes, ...)` — render |u|; nodal mask at |u|<=eps*max (eps default 0.08).
  - `square_pattern(p, q, L=1.0, res=512, sign=+1)` and superposition variant.
  - `frequency_membrane(n, m, R, c)` = z_{n,m}·c/(2πR); `frequency_square(p, q, L, c, dispersion='membrane'|'plate')`.
- `decode.py` — reverse:
  - `decode_structural(descriptor: dict) -> list[ModeCandidate]` implementing rules R1–R11 from the math spec §2. Descriptor keys: kind (rings|radial|spiral|grid|composite|cluster), azimuthal_order (int or None), radial_nodes (int|None), arms, components, boundary ('circle'|'square'), notes.
  - `decode_image(img, res=512) -> list[ModeCandidate]` implementing §1 pipeline (center → polar unwrap → power-summed angular FFT → n; nodal-circle minima matched to Bessel-zero ratios → m; log-polar spiral test with coherence C; grid → square model). Must return top-3 with scores and confidence (high/medium/low per §3).
  - ModeCandidate dataclass: n, m, model ('membrane'|'square'), score, confidence, evidence (dict of measured quantities).
- `notes.py` — presentation per sound spec:
  - `freq_to_note(f)` → (name, cents, midi, band_label[INFRASONIC/SUB-PITCH/PITCH/HIGH/ULTRASONIC]), wavelength in air (343 m/s).
  - `beat_table(freqs: dict[str,float])` → pairwise Δf, beat category, ratio, nearest just-intonation interval (13-interval table), cents error; chord view (sorted, ratio-to-root + consecutive ratios).
- `run_decoding.py` — decodes the 10 patterns below (structural path), prints results JSON to stdout; also renders forward-simulation PNGs of each pattern's top candidate mode (and, for 3 patterns, a comparison grid of top-3 candidates) into results/.
- `test_cymatics.py` — test battery: physics 10 checks (spec §sanity) + math V1–V15 subset feasible offline (clean round-trip decode n=1..8,m=1..3 top-3; rotation invariance; noisy round trip; grid pitch recovery; spiral chirality) + presentation edge cases (f=0 → handled, f=8 Hz infrasonic label, Δf=0 unison, Δf>40 difference tone, cents rounding ±50).

## The 10 patterns to decode (structural descriptors; from crop-circle dataset)
1. Punchbowl quintuplet 1983 — kind=cluster: 4 satellites around 1 center, equal ring radius. boundary=circle.
2. Cheesefoot dumbbell 1990 — kind=composite: two lobes on an axis. boundary=circle.
3. Barbury Castle tetrahedron 1991 — kind=radial: 3-fold, 1–2 radial rings, boundary=circle.
4. Stonehenge Julia Set 1996 — kind=spiral: ~149 circles on a single winding spiral, chirality unknown → test both; boundary=circle.
5. Silbury Koch snowflake 1997 — kind=radial: 6-fold boundary with 3-fold interior motif; boundary=hexagon-ish → circle model acceptable.
6. Milk Hill Galaxy 2001 — kind=spiral: 6 arms, ~68 circles/arm (409 total); boundary=circle.
7. Chilbolton Arecibo grid 2001 — kind=grid: 23×73 cells, rectangular → square model (23,73).
8. Crabwood disc 2002 — kind=composite: figure + disc; disc = Archimedean spiral groove (high radial order); boundary=circle.
9. Barbury pi wheel 2008 — kind=radial: 10 segments, ratchet (chiral), 1 ring; boundary=circle.
10. Hackpen 3-D cubes 2012 — kind=radial: 6-fold hexagonal packing, ~3 radial shells; boundary=circle.

## Reference resonators (absolute Hz sensitivity)
R1 drumhead: R=0.15 m, c=100 m/s (K=106.1 Hz). R2 plate: R=0.15 m, c_eff=1000 m/s. R3 plate: R=0.5 m, c_eff=1000 m/s. Dimensionless ratio f/f_{0,1} is the PRIMARY output; Hz at R1–R3 are sensitivity illustrations. Every output table must carry the honesty note: "absolute Hz depends on assumed resonator; ratios are resonator-independent."

## Acceptance criteria
- `python test_cymatics.py` exits 0 with all tests passing (print PASS/FAIL per test).
- `python run_decoding.py` writes results/decoding_results.json + ≥10 PNGs to /mnt/agents/output/cymatics/results/.
- No network access; only numpy/scipy/matplotlib. Clean docstrings citing which spec section each function implements.
