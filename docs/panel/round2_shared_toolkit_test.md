# Round 2 — Formalized Cross-Domain Test
## H: Shared-Toolkit Hypothesis

Crop formations' key ratios and symmetry orders concentrate on the historically constructible landmark set
**C = {integer ratios a:b with a,b ≤ 9; √2, √3, √5; n-fold orders n ∈ {2,3,4,6,8,12,16}}**
at rates statistically indistinguishable from the documented-monument corpus — both outputs of the same human
straightedge-and-circle toolkit. Explains family-level matches (12-spoke ↔ rose window) without item-level
identity (hence zero FWER-significant brute-force hits).

**Competitors:**
- H_E (esoteric): crops concentrate on E = {φ, π, e, prime orders 5,7,11,13,…,22,23,…} significantly more than monuments.
- H_0 (null): crop ratios smooth/unconstrained (log-uniform on [1, 2.5]); no excess mass at C or E.

## Test (one instrument, three corpora)
1. Blind ratio extraction, same pipeline for: (a) crop corpus; (b) monument corpus = POSITIVE CONTROL
   (must recover C-concentration or test void); (c) non-sacred modern layouts = negative control.
   Ratios: bounding radii, ring spacings, segment counts; n-fold via rotational autocorrelation. Log-transform.
2. Landmark-distance statistic: D_S(x) = min_{c∈S} |log x − log c| for S ∈ {C, E}.
   Tolerance τ = 0.02 relative (aerial measurement-error floor) — PRE-REGISTERED.
3. Excess-mass test: f_C = fraction of ratios within τ of C. Expected f_C under H_0 = C's coverage fraction
   of the log-interval. One-sided binomial; FWER via 10,000 permutations across all landmarks.
4. Two-sample: KS/permutation on D_C distributions, crops vs monuments; equivalence via TOST with power report.

## Falsifiers
- H falsified: crops fail C-concentration (no excess mass; TOST equivalence rejected).
- H_E wins: E-excess > C-excess AND > monuments' E-rate.
- H_0 retained: neither C nor E shows excess mass beyond coverage expectation.

## Alias rule (pre-registered)
π vs 22/7 = 0.04%; φ vs seked-derived 1.6186 = 0.03% — both below measurement floor, indistinguishable
per item. Resolution: ratio within τ of both C and E landmarks → assigned to C (simplest-construction rule).
Discriminating power therefore comes from PRIME ORDERS and NON-ALIASED RATIOS ONLY.
Decisive cases: 22-fold, 11-fold, 23×73 grid — outside C and outside every documented monument.

## Staked prediction
Crops show moderate C-concentration (human rope/circle manufacture → √2/√3/4/6-fold emerge naturally) BUT a
significantly heavier prime-order tail than monuments → two-sample test rejects distributional identity while
C-excess-mass rejects H_0. Joint outcome = "shared toolkit, divergent canon": crop geometry is modern
recreational/fractal geometry borrowing generic rose-window/mandala templates, not the historical sacred canon.
This is the formal explanation of the Round-2 result (FWER-zero item matches; relaxed matches only on generic
families: rose window D=0.091, quincunx D=0.0, golden-spiral D=0.0).
