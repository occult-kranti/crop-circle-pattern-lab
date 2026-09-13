#!/usr/bin/env python3
"""run_decoding.py — decode the 10 canonical patterns end-to-end.

Pipeline (master spec §workflow):
  structural descriptors (SPEC canonical set) → decode.decode_structural
  → frequency ratios → absolute Hz on the reference resonators
  → notes / bands / difference vibrations → JSON + CSV artifacts.

Writes:
  results/decoding_results.json     (full machine-readable dump)
  results/decoded_frequencies.csv   (per-pattern headline rows)
  results/difference_vibrations.csv (all 45 pairwise Δf rows)
"""

import json
import os

import numpy as np

import cymatics as cym
import decode as dec
import notes

RESULTS = os.path.join(os.path.dirname(__file__), "..", "results")

# The SPEC's canonical pattern set (structural descriptors — see SPEC §data)
PATTERNS = [
    dict(id=1, name="Punchbowl quintuplet 1983",
         struct=dict(kind="cluster", components=5, arms=4, radial_nodes=1,
                     boundary="circle")),
    dict(id=2, name="Cheesefoot dumbbell 1990",
         struct=dict(kind="composite", boundary="circle",
                     notes="dumbbell: two lobes on an axis")),
    dict(id=3, name="Barbury Castle tetrahedron 1991",
         struct=dict(kind="radial", azimuthal_order=3, radial_nodes=2,
                     boundary="circle",
                     notes="tetrahedral 3-fold pictogram")),
    dict(id=4, name="Stonehenge Julia Set 1996",
         struct=dict(kind="spiral", arms=1, components=149,
                     boundary="circle")),
    dict(id=5, name="Silbury Koch snowflake 1997",
         struct=dict(kind="radial", azimuthal_order=6, boundary="circle",
                     notes="Koch snowflake fractal")),
    dict(id=6, name="Milk Hill Galaxy 2001",
         struct=dict(kind="spiral", arms=6, components=409,
                     boundary="circle")),
    dict(id=7, name="Chilbolton Arecibo grid 2001",
         struct=dict(kind="grid", components=(23, 73), boundary="square")),
    dict(id=8, name="Crabwood disc 2002",
         struct=dict(kind="rings", radial_nodes=16, boundary="circle")),
    dict(id=9, name="Barbury pi wheel 2008",
         struct=dict(kind="radial", azimuthal_order=10, radial_nodes=1,
                     boundary="circle",
                     notes="10-segment ratchet wheel, chiral")),
    dict(id=10, name="Hackpen 3-D cubes 2012",
         struct=dict(kind="radial", azimuthal_order=6, radial_nodes=4,
                     boundary="circle", notes="3-D cube hexagonal packing")),
]


def decode_all():
    resonators = notes.reference_resonator_table()
    f01 = [r["f01_hz"] for r in resonators]
    decodes, freq_map = [], {}
    for pat in PATTERNS:
        cands = dec.decode_structural(pat["struct"])
        top = cands[0]
        ratio = (cym.frequency_ratio_membrane(top.n, top.m)
                 if top.model == "membrane"
                 else float(np.hypot(top.n, top.m)) / float(np.hypot(1, 1)))
        hz = [ratio * f for f in f01]
        note = notes.freq_to_note(hz[0])
        freq_map[f"p{pat['id']:02d} {pat['name']}"] = hz[0]
        decodes.append(dict(
            id=pat["id"], name=pat["name"], model=top.model,
            n=top.n, m=top.m, confidence=top.confidence,
            freq_ratio=round(ratio, 4),
            ref_resonator=resonators[0]["resonator"],
            ref_hz=round(hz[0], 2), ref_note=note["label"],
            cents=note["cents"], band=note["band"],
            hz_2=round(hz[1], 2), hz_3=round(hz[2], 2),
            hz_4=(round(ratio * (f01[0] * 3.0), 2)),
            candidates=[dict(n=c.n, m=c.m, model=c.model,
                             confidence=c.confidence,
                             score=round(c.score, 3))
                        for c in cands[:4]],
            evidence=top.evidence))
    beats = notes.beat_table(freq_map)
    return decodes, beats, freq_map


def write_outputs(decodes, beats, freq_map):
    os.makedirs(RESULTS, exist_ok=True)
    dump = dict(
        reference_resonators=notes.reference_resonator_table(),
        honesty_note=notes.HONESTY_NOTE,
        decoded_frequencies=decodes,
        difference_vibrations=beats["pairs"],
    )
    with open(os.path.join(RESULTS, "decoding_results.json"), "w") as fh:
        json.dump(dump, fh, indent=2, default=_jsonable)

    with open(os.path.join(RESULTS, "decoded_frequencies.csv"), "w") as fh:
        fh.write("id,name,model,n,m,confidence,freq_ratio,ref_hz,ref_note,"
                 "cents,band\n")
        for d in decodes:
            fh.write(f"{d['id']},\"{d['name']}\",{d['model']},{d['n']},"
                     f"{d['m']},{d['confidence']},{d['freq_ratio']},"
                     f"{d['ref_hz']},{d['ref_note']},{d['cents']},"
                     f"\"{d['band']}\"\n")

    with open(os.path.join(RESULTS, "difference_vibrations.csv"), "w") as fh:
        fh.write("a,b,f_lo,f_hi,delta_f_hz,category,delta_f_note,ratio,"
                 "ji_interval,ji_ratio,ji_cents_error,ji_tier\n")
        for p in beats["pairs"]:
            ji = p["ji"] or {}
            dn = (p["delta_f_note"] or {}).get("label") or ""
            fh.write(f"\"{p['a']}\",\"{p['b']}\",{p['f_lo']},{p['f_hi']},"
                     f"{p['delta_f_hz']},{p['category']},{dn},{p['ratio']},"
                     f"{ji.get('interval') or ''},{ji.get('ratio_str') or ''},"
                     f"{ji.get('cents_error') if ji else ''},"
                     f"{ji.get('tier') or ''}\n")


def _jsonable(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.ndarray,)):
        return o.tolist()
    if isinstance(o, float) and not np.isfinite(o):
        return None
    return o


def main():
    decodes, beats, freq_map = decode_all()
    write_outputs(decodes, beats, freq_map)
    print(f"decoded {len(decodes)} patterns "
          f"({sum(d['confidence'] == 'HIGH' for d in decodes)} HIGH), "
          f"{len(beats['pairs'])} difference rows → {RESULTS}")


if __name__ == "__main__":
    main()
