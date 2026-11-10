# Round 2 — One sharp cross-domain hypothesis (post-null)

## Diagnosis of the null
Your min-statistic degenerates at D=0 because the match criterion uses only **mode labels / low-order symmetry classes** ((1,1), (2,1)…). These are shared by every bounded resonator — they carry ~1 bit. A real encoded monument must satisfy a much stronger, quantitative constraint that generic symmetry cannot fake:

## H — the One-Geometry Hypothesis (scale coherence)
> **IF** a crop decode encodes the mode field of a *specific physical resonator*, **THEN** all matched modes must be reproducible from that monument's spectrum by **one single multiplicative scale factor** s (detune / unit conversion / transposition), because one object has one geometry. Equivalently: every matched mode implies an effective radius R = z_mn·c/(2πf), and for a true encoding all implied R agree (equivalently, all s_i = f_decode/f_monument agree) to within the engine's frequency resolution, for **≥4 matched modes**. Generic-symmetry matches produce *inconsistent* scales (random s_i).

This is sharp, physically motivated (mode frequencies of one body are locked to one length scale: f ∝ c/L), and directly repairs the degenerate null: it converts boolean label matching into a continuous, quantitative coincidence.

## Pre-registered target spectra (from Round 1, computed, not measured)
| Monument | Reference spectrum f_mon [Hz] | Rare sub-structure |
|---|---|---|
| King's Chamber | 16.38, 32.76, **32.77**, 49.1, 65.5, 81.9, 98.3, 114.7 | quasi-1D ladder 16.38·n; exact doublet at 32.8 (Lx=2Ly) |
| Newgrange | 26.4, 29.6, 39.6, 47.6, 52.8, 105.5, **109.6** | split 4th harmonic: 105.5 & 109.6 (4 % apart) |
| Hypogeum (measured) | **70, 114** (+ niche 50–91) | joint pair; ratio 1.63, non-integer |
| Sarcophagus (air modes) | 60, 67, 86 | triad within 26 Hz span |

## Test
Statistic T(pair) = max over free s ∈ [0.25, 4] of #{matched modes with |f_dec − s·f_mon| < ε}, ε = max(engine resolution, 1 %).
Null: your existing Westfall-Young machinery, B=100k, permuting decode spectra. Per-pair FWER threshold (α=0.05, 3570 pairs): p_pair < **1.4×10⁻⁵** (Bonferroni) / 1.44×10⁻⁵ (Šidák).

Computed pass-criterion power (scale ratios null-distributed over ~2 octaves, 2 % coherence window):
- ≥3 coherent of m=6 matches: p=5.9×10⁻⁵ → ×3570 = 0.21 → **NOT significant** (do not use).
- **≥4 coherent of m=5–6: p=2.2×10⁻⁷–6.5×10⁻⁷ → ×3570 = 8×10⁻⁴–2×10⁻³ → passes FWER.** ← pre-register this.
- Monument-specific boosters (use as joint conditions if T=3):
  - KC equal-spacing chain: ≥3 consecutive inter-mode spacings = 16.4 ±0.45 Hz: p≈3×10⁻⁷/decode (×85 ≈ 2.5×10⁻⁵).
  - Newgrange: ladder ≥3/5 slots AND split-fourth partner both present: joint p=5.5×10⁻⁴ (×85 ≈ 0.046) — marginal alone, strong in combination with scale coherence.

## Falsification
H is **falsified** if either:
1. No decode–monument pair reaches ≥4 scale-coherent matches (p_pair < 1.4×10⁻⁵); or
2. The count of scale-coherent pairs equals the permutation-null expectation (enrichment factor ≈ 1, 95 % CI includes 1).
Either closes the monument-matching claim at current resolution — the decodes would then encode only generic/ideal circular cymatics, not any specific ancient resonator.

## Caveats (honesty)
- If the engine's frequency resolution is >1 %, the KC doublet is unresolvable; use the Newgrange split (4 % spacing) and equal-spacing chain instead.
- If decodes hypothetically encode *measured* (not idealized-box) spectra, widen ε to 5 % for vaulted/irregular rooms (Newgrange, Hypogeum) — power drops ~10×; state this as a sensitivity analysis.
- Scale factor s should be reported even on success: s=1 is the strong claim; s≈const≠1 is weaker (systematic detune) but still coherent.
