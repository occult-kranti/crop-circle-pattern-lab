# Reverse Cymatic Decoding of Major Crop-Circle Patterns — Report

**Framing (read first):** cymatics renders vibration modes as visible nodal-line patterns (Chladni figures). This project runs the chain *backwards* — pattern geometry → candidate vibration modes → frequencies — as a **modeling exercise**, not as evidence that formations encode sound. The geometry→mode inversion is fundamentally ambiguous (many mode sets share a symmetry), so every decode carries a confidence class, and the dimensionless ratio f/f₀₁ is the primary output; absolute Hz requires assuming a resonator.

**Method:** built by a coder swarm from three expert specifications (physics: membrane/plate mode physics; math: symmetry-to-mode estimation with validated prototype, 23/24 top-1 on synthetic sweeps; sound engineering: 12-TET/beat/just-intonation presentation). Independently verified: all frequencies hand-recomputed against `scipy.special.jn_zeros`; a numeric bug in the high-order Bessel fallback was caught and fixed (pattern 9 ratios corrected by up to 2.35%). Final test battery: **31/31 passing** (scaling laws, zero-ratio identities, rotation/translation invariance, noisy round-trips, grid-pitch recovery, chirality, edge cases: blank/uniform images, f=0/NaN/negative, degenerate modes).

## Decoded frequencies (reference resonator R1: 30 cm drumhead, c = 100 m/s, f₀₁ = 255.2 Hz)

| # | Pattern | Model | Mode (n,m) | f/f₀₁ | Hz @ R1 | Note (12-TET) | Band | Confidence |
|---|---|---|---|---|---|---|---|---|
| 1 | Punchbowl quintuplet 1983 | membrane | (4, 1) | 3.1555 | 805.15 | G5 +46¢ | PITCH | MEDIUM |
| 2 | Cheesefoot dumbbell 1990 | membrane | (1, 1) | 1.5933 | 406.56 | G♯4 −37¢ | PITCH | MEDIUM |
| 3 | Barbury tetrahedron 1991 | membrane | (3, 1) | 2.6531 | 676.96 | E5 +46¢ | PITCH | MEDIUM |
| 4 | Stonehenge Julia Set 1996 | membrane | (1, 149)† | 194.98 | 49 750 | G11 −15¢ | ULTRASONIC | LOW† |
| 5 | Silbury Koch snowflake 1997 | membrane | (6, 1) | 4.1317 | 1 054.25 | C6 +13¢ | PITCH | LOW |
| 6 | Milk Hill Galaxy 2001 | membrane | (6, 68)† | 92.39 | 23 575 | F♯10 −8¢ | ULTRASONIC | LOW† |
| 7 | Chilbolton Arecibo grid 2001 | square plate | (23, 73) | 54.12 | 127 563 | B12 +15¢ | ULTRASONIC | HIGH |
| 8 | Crabwood disc 2002 | membrane | (0, 16) | 20.58 | 5 250 | E8 −8¢ | HIGH | MEDIUM |
| 9 | Barbury pi wheel 2008 | membrane | (10, 1) | 6.0194 | 1 535.90 | G6 −36¢ | PITCH | MEDIUM |
| 10 | Hackpen 3-D cubes 2012 | membrane | (6, 4) | 8.4500 | 2 156.10 | C♯7 −49¢ | PITCH | MEDIUM |

† Spiral "bead counts" (149, 409 circles) are construction counts, not physical modes — flagged LOW by design.

## Difference vibrations (Δf = |f₁−f₂|, each Δf itself mapped to a pitch)

All 45 pairs in `difference_vibrations.csv`. Highlights:

| Pair | Δf (Hz) | Δf as pitch | Ratio | Nearest just interval | Cents error |
|---|---|---|---|---|---|
| dumbbell 1990 ↔ tetrahedron 1991 | 270.40 | C♯4 | 1.6651 | **major 6th (5:3)** | **−1.6¢ (exact)** |
| pi wheel 2008 ↔ 3-D cubes 2012 | 620.20 | D♯5 | 1.4038 | **tritone (√2-ish)** | **−3.0¢ (exact)** |
| dumbbell 1990 ↔ quintuplet 1983 | 398.59 | G4 | 1.9804 | octave (2:1) | −17.1¢ |
| tetrahedron 1991 ↔ quintuplet 1983 | 128.19 | C3 | 1.1894 | minor 3rd (6:5) | −15.4¢ |
| quintuplet 1983 ↔ Koch 1997 | 249.10 | B3 | 1.3094 | perfect 4th (4:3) | −31.4¢ |

Every Δf here exceeds 40 Hz, so all pairs are perceived as **difference (combination) tones**, not beats — the early Hampshire pictograms land within a few cents of pure musical intervals, which is expected arithmetic for low Bessel-mode ratios (z₁,₁/z₀,₁ = 1.593 ≈ 8:5), not evidence of musical intent.

## Findings
1. **Early pictograms decode to low, near-harmonic modes** — inevitable for simple low-order symmetry, and the only regime where note-like intervals appear.
2. **Only the Chilbolton grid decodes at HIGH confidence**, because its mode numbers (23×73) are literally printed in the design — a reminder that information-bearing patterns are *not* physical modes.
3. **Confidence tracks information content**: simple symmetric glyphs = MEDIUM (aliased), bead-count spirals = LOW, printed grids = HIGH.
4. The inversion ambiguity is real and quantified: each decode lists alias modes (e.g., Bessel near-coincidence z₅,₁ ≈ z₀,₃).

## Files
- `code/` — cymatics.py, decode.py, notes.py, test_cymatics.py (31 tests), run_decoding.py
- `results/` — decoding_results.json, decoded_frequencies.csv, difference_vibrations.csv, 13 PNG renders
- Website integration: "Cymatics Lab" page of the crop-circles site.
