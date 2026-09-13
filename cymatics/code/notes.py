#!/usr/bin/env python3
"""notes.py — frequency → musical note / band / difference-vibration engine.

Presentation spec §1 (note labelling), §2 (beat categories, JI matching),
§3 (chord view), §4 (reference resonators), §5 (edge cases).

Conventions:
* 12-TET, A4 = 440 Hz; MIDI 69 = A4; note labels C..B with # only.
* cents always in [−50, +50); the ±50 boundary carries `alt_spelling`.
* Bands: INFRASONIC < 20 Hz; PITCH 20–5000; HIGH 5000–15000 (pitch
  weakens); ULTRASONIC > 15000 (17.6 kHz labelled borderline per §1.3).
"""

import math

A4 = 440.0
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

HONESTY_NOTE = (
    "Absolute Hz depends entirely on the assumed resonator; only the "
    "dimensionless ratio f/f₀₁ is resonator-independent and is reported "
    "as primary."
)


# ------------------------------------------------------------- §1 notes

def _midi_to_label(midi):
    name = NOTE_NAMES[midi % 12]
    octave = midi // 12 - 1
    return f"{name}{octave}"


def freq_to_note(f):
    """Frequency (Hz) → note row (presentation spec §1, edge cases §5).

    Returns dict(note, label, midi, cents, alt_spelling, band, flags).
    f = 0, NaN or negative → handled gracefully, note=None, band INFRASONIC,
    with an explanatory flag.  Negative MIDI numbers are legal (8 Hz ≈ C−1).
    """
    flags = []
    if f is None or not isinstance(f, (int, float)) or not math.isfinite(f) or f <= 0:
        if f == 0:
            flags.append("f = 0: no pitch; treated as DC/offset")
        else:
            flags.append("invalid frequency (NaN/negative/non-finite)")
        return dict(note=None, label=None, midi=None, cents=None,
                    alt_spelling=None, band="INFRASONIC", flags=flags)

    midi_f = 69.0 + 12.0 * math.log2(f / A4)
    midi = int(math.floor(midi_f + 0.5))
    cents = (midi_f - midi) * 100.0
    # keep cents in [−50, +50)
    if cents >= 50.0:
        midi += 1
        cents -= 100.0
    alt = None
    if abs(abs(cents) - 50.0) < 1e-9 or abs(cents) >= 49.95:
        # quarter-tone boundary: double spelling (e.g. between C4 and C#4)
        alt = _midi_to_label(midi + (1 if cents > 0 else -1))

    if f < 20.0:
        band = "INFRASONIC"
    elif f <= 5000.0:
        band = "PITCH"
    elif f <= 17600.0:
        band = "HIGH (pitch weakens)"
    elif f <= 17600.0 * 1.0 + 0.0:  # unreachable, kept for clarity
        band = "ULTRASONIC (borderline)"
    else:
        band = "ULTRASONIC"
    # §1.3 verified row: 17 600 Hz → C#10 labelled ULTRASONIC (borderline)
    if 15000.0 < f <= 17600.0:
        band = "HIGH (pitch weakens)"
    if f == 17600.0:
        band = "ULTRASONIC (borderline)"

    return dict(note=_midi_to_label(midi), label=_midi_to_label(midi),
                midi=midi, cents=round(cents, 1), alt_spelling=alt,
                band=band, flags=flags)


# ----------------------------------------------------- §2 beats & ratios

def beat_category(delta_f):
    """Presentation spec §2.2/§2.4 beat categories.

    Δf = 0      → 'UNISON (exact)'
    0 < Δf ≤ 4  → 'SLOW BEAT'
    4 < Δf ≤ 15 → 'ROUGHNESS'
    15 < Δf ≤ 40→ 'TRANSITION'
    Δf > 40     → 'DIFFERENCE TONE' (a combination tone, NOT a beat)
    """
    if delta_f is None or not math.isfinite(delta_f) or delta_f < 0:
        return "INVALID"
    if delta_f == 0:
        return "UNISON (exact)"
    if delta_f <= 4.0:
        return "SLOW BEAT"
    if delta_f <= 15.0:
        return "ROUGHNESS"
    if delta_f <= 40.0:
        return "TRANSITION"
    return "DIFFERENCE TONE"


# Just-intonation interval table (§2.3) — tolerance tiers:
#   ≤ 5 ¢  'exact (JI)'   ≤ 15 ¢ 'near'   ≤ 50 ¢ 'approximate'
JI_INTERVALS = [
    (1 / 1, "unison", "1:1"), (16 / 15, "minor 2nd", "16:15"),
    (9 / 8, "major 2nd", "9:8"), (6 / 5, "minor 3rd", "6:5"),
    (5 / 4, "major 3rd", "5:4"), (4 / 3, "perfect 4th", "4:3"),
    (45 / 32, "tritone", "45:32"), (3 / 2, "perfect 5th", "3:2"),
    (8 / 5, "minor 6th", "8:5"), (5 / 3, "major 6th", "5:3"),
    (9 / 5, "minor 7th", "9:5"), (15 / 8, "major 7th", "15:8"),
    (2 / 1, "octave", "2:1"),
]


def _cents(ratio):
    return 1200.0 * math.log2(ratio)


def nearest_ji(ratio, max_cents=50.0):
    """Nearest just-intonation interval within one octave.

    ratio is octave-reduced into [1, 2).  Returns dict(interval, ratio_str,
    cents_error, tier) or None if nothing within max_cents.
    """
    if ratio <= 0 or not math.isfinite(ratio):
        return None
    while ratio < 1.0:
        ratio *= 2.0
    while ratio >= 2.0:
        ratio /= 2.0
    best = None
    for r, name, rs in JI_INTERVALS:
        err = _cents(ratio) - _cents(r)
        if best is None or abs(err) < abs(best[0]):
            best = (err, name, rs)
    err, name, rs = best
    if abs(err) > max_cents:
        return None
    tier = ("exact (JI)" if abs(err) <= 5.0
            else "near" if abs(err) <= 15.0 else "approximate")
    return dict(interval=name, ratio_str=rs, cents_error=round(err, 1),
                tier=tier)


def octave_reduced_match(ratio):
    """Like nearest_ji but reports compound ratios as 2^k × JI (§2.3 note)."""
    if ratio <= 0 or not math.isfinite(ratio):
        return None
    k = 0
    r = ratio
    while r < 1.0:
        r *= 2.0
        k -= 1
    while r >= 2.0:
        r /= 2.0
        k += 1
    ji = nearest_ji(r)
    if ji is None:
        return None
    out = dict(ji)
    if k:
        out["compound"] = f"2^{k} × {ji['ratio_str']}"
    return out


def beat_table(freqs):
    """All-pairs difference-vibration table (§2.1–§2.4).

    freqs: {label: f_hz}.  Each row: a, b, f_lo, f_hi, delta_f_hz,
    category, delta_f_note (pitch of Δf when audible), ratio (f_hi/f_lo),
    ji (nearest JI match incl. tier), beat_period_s when it is a true beat.
    """
    items = [(k, float(v)) for k, v in freqs.items()]
    pairs = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            (a, fa), (b, fb) = items[i], items[j]
            lo, hi = (fa, fb) if fa <= fb else (fb, fa)
            df = hi - lo
            cat = beat_category(df)
            row = dict(a=a, b=b, f_lo=round(lo, 2), f_hi=round(hi, 2),
                       delta_f_hz=round(df, 2), category=cat,
                       delta_f_note=None, ratio=round(hi / lo, 4) if lo else None,
                       ji=None, beat_period_s=None)
            if cat == "DIFFERENCE TONE":
                row["delta_f_note"] = freq_to_note(df)
            if lo > 0:
                row["ji"] = octave_reduced_match(hi / lo)
            if cat in ("SLOW BEAT", "ROUGHNESS", "TRANSITION"):
                row["beat_period_s"] = round(1.0 / df, 3)
            pairs.append(row)
    return dict(pairs=pairs)


# ------------------------------------------------------------ §3 chords

def chord_view(freqs):
    """Chord view (§3.3): rows sorted by f, ratio-to-root and consecutive
    JI matches."""
    rows = sorted((float(f), k) for k, f in freqs.items())
    if not rows:
        return dict(rows=[])
    f0 = rows[0][0]
    out = []
    prev = None
    for f, k in rows:
        row = dict(label=k, f_hz=f,
                   ratio_to_root=round(f / f0, 4),
                   ji_vs_root=octave_reduced_match(f / f0),
                   ji_consecutive=None)
        if prev is not None:
            row["ji_consecutive"] = octave_reduced_match(f / prev)
        out.append(row)
        prev = f
    return dict(rows=out)


# --------------------------------------------- §4 reference resonators

def reference_resonator_table():
    """The three agreed reference resonators (presentation spec §4).

    R1: 30 cm drumhead, c = 100 m/s   → f₀₁ = z₀₁·c/(2πR) ≈ 255.2 Hz
    R2:  3 cm drumhead, c = 100 m/s   → f₀₁ ≈ 2551.6 Hz
    R3: 30 cm drumhead, c = 300 m/s   → f₀₁ ≈ 765.5 Hz
    """
    import cymatics as cym  # local import to avoid a cycle
    rows = []
    for name, R, c in (("R1 drumhead 30cm, c=100 m/s", 0.15, 100.0),
                       ("R2 drumhead 3cm, c=100 m/s", 0.015, 100.0),
                       ("R3 drumhead 30cm, c=300 m/s", 0.15, 300.0)):
        rows.append(dict(resonator=name, R_m=R, c_m_s=c,
                         f01_hz=round(cym.frequency_membrane(0, 1, R, c), 1)))
    return rows
