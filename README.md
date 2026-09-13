# Crop Circle Pattern Lab

A data-driven investigation of the crop-circle phenomenon — dataset, statistics, hypotheses, a verified reverse-cymatic decoder, and a three-way comparison with DMT form constants and sacred geometry. Everything runs on open-source tools (Python, pandas, SciPy, scikit-learn, SQLite, vanilla JS).

## Contents

| Path | What |
|---|---|
| `website/` | Self-contained static site (no CDNs). Serve with `python -m http.server` → `localhost:8000`. Pages: Overview, Timeline, Dataset, Analysis, Hypotheses & Experiments, Research Papers, Cymatics Lab, DMT × Sacred Geometry. |
| `data/` | Canonical dataset: `crop_circles.csv` (60 curated major formations, 21 fields), `papers.csv` (19 research works), `annual_counts.csv` (16 sourced counts), `symmetry_orders.csv`, `motif_mapping.csv`, `cropcircles.sqlite` (all tables). |
| `cymatics/` | Reverse cymatic decoder: forward Chladni/membrane simulator, pattern→mode decoder, frequency/note/beat engine. `code/test_cymatics.py` → 31/31 passing. `results/` → decoded frequencies, 45-pair difference-vibration table, 13 rendered figures. `SPEC.md`, `report.md`. |
| `compare/` | DMT × sacred geometry × crop circles comparison: `motif_mapping.csv`, `comparison_data.json`, `report.md`. |
| `arecibo/` | Bit-level decode of the 1974 Arecibo message (the project that started this repo — decoding a photo of the message + its 3D-printed replica). |

## Headline results

- **Trend:** world reports ρ = −0.95 (p ≈ 3e-4): ~1,000/yr (1990) → 34–68/yr (2016–21).
- **Seasonality:** 98% of dated English formations April–September (χ² p ≈ 3e-21).
- **Geography:** 43% of curated English formations within 15 km of Avebury (matches Northcote's unbiased census ~44%).
- **Cymatics:** spiral form constant and 1990 dumbbell pictogram decode to the *identical* membrane mode (1,1); honeycomb and 2012 3-D cubes both (6,4).
- **Comparison:** 86.8% of formations have symmetry n ≤ 6 — the same wallpaper families as V1-cortex hallucination geometry (Bressloff–Cowan). Divergences (legible bit grids, exact fractals, n = 10–44 symmetry) mark deliberate human design.

## Honesty notes

The formations dataset is **curated** (notable formations, not a census); every aggregate count is flagged hard data / estimate / media claim. The cymatic decoding is a modeling exercise — the geometry→mode inversion is fundamentally ambiguous, and absolute Hz depends on the assumed resonator (ratios are reported as primary). Shared geometry with DMT/sacred motifs reflects shared human neuroarchitecture, not shared cosmic sources.

## Binary artifacts (.b64 sidecars)

Raw binaries (images, SQLite DB) are **not committed directly** — they ship as base64 sidecar files (`*.b64`). After cloning, restore them with:

```bash
bash decode_b64.sh
```

This decodes every `*.b64` next to its target (e.g. `data/cropcircles.sqlite.b64` → `data/cropcircles.sqlite`, `website/assets/cymatics/*.jpg.b64` → the `.jpg` figures the site displays). The two `cropcircles.sqlite.b64` sidecars are stored as `base64(gzip(db))` (the raw DB is mostly empty pages whose plain base64 is tens of KB of repeated `A` runs that cannot transit a text-only API intact); `decode_b64.sh` auto-detects the gzip magic and restores the byte-identical database.

## Reproduce

```bash
bash decode_b64.sh   # restore binaries from .b64 sidecars first
cd cymatics/code && python test_cymatics.py && python run_decoding.py
sqlite3 data/cropcircles.sqlite "SELECT era, COUNT(*) FROM formations GROUP BY era;"
cd website && python -m http.server 8000
```

## Sources

Full citations inside `data/papers.csv` and each report. Key anchors: Wikipedia *Crop circle*; Northcote 2006 (GIS census); Levengood 1994/1999 + Grassi et al. 2005; Hawkins 1992/1997; Klüver 1928/1966; Ermentrout & Cowan 1979; Bressloff et al. 2001/2002; Lawrence et al. 2022 (n=3,778); Davis et al. 2020; Markowsky 1992; Taylor 2010/2011.
