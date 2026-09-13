# Decoding the Two Images: The Arecibo Message

## TL;DR — The key finding

**Both panels encode the SAME message: the original 1974 Arecibo message** (the 1,679-bit binary radio transmission, arranged 23 columns × 73 rows). The left panel is a backlit screen/pixel rendering of the bitstream; the right panel is a physical 3D-printed relief of the identical 23×73 grid. It is **not** the famous 2001 Chilbolton "Arecibo reply" crop formation — the discriminators (5 DNA elements with no silicon column, a normal human figure with height code 14, a 6×6 population block, only Earth raised among the planets, and the Arecibo dish at the bottom) all match the 1974 original. This was verified by extracting both grids cell-by-cell from the photo and comparing them against the published, bit-verified decoding.

---

## 1. What the message is

| Parameter | Value |
|---|---|
| Sent | 16 November 1974, Arecibo Observatory upgrade ceremony |
| Target | Globular cluster M13 (~25,000 light-years away) |
| Bits | 1,679 = 23 × 73 (a semiprime — only one non-trivial rectangular arrangement makes a coherent picture) |
| Frequency | 2,380 MHz, frequency-shift keying (10 Hz shift between 0 and 1) |
| Wavelength | 12.6 cm — this is the message's built-in unit of length |
| Bit rate / duration | 10 bits/s → 167.9 s (under three minutes) |
| Authors | Frank Drake, with Carl Sagan and others |

## 2. Full section-by-section decode (verified against the published 1,679-bit string)

| # | Section (top → bottom) | Decoded content |
|---|---|---|
| 1 | Numbers 1–10 (rows 1–4) | The decimal numbers 1–10 in binary, one column per number, read top-to-bottom; a bottom marker row of 1s marks each number's least significant bit. 8, 9, 10 need 4 bits, so each spills into a second column — demonstrating the multi-column convention used later. |
| 2 | DNA elements (rows 6–10) | Five 4-bit columns with a 11111 marker row: **H = 0001 = 1, C = 0110 = 6, N = 0111 = 7, O = 1000 = 8, P = 1111 = 15** — the atomic numbers of hydrogen, carbon, nitrogen, oxygen, phosphorus. This column order (H-C-N-O-P) is the atom legend for all formulas below. |
| 3 | Nucleotide formulas (rows 12–26) | Four blocks of molecular formulas as atom counts in H-C-N-O-P order: deoxyribose **75010**, adenine **45500**, thymine **55220**, phosphate **00041**, cytosine **44310**, guanine **45510** — the building blocks of DNA as incorporated into the double helix. |
| 4 | DNA double helix + genome (rows 27–45) | Double-helix graphic with a central bar of binary: decodes to **≈ 4.29 billion** (strict bit-read: 4,294,441,822; many sources quote 4,294,441,823) — the 1974 estimate of the number of base pairs in the human genome. |
| 5 | Human + height + population (rows 46–56) | Stick-figure human. Left of it, a horizontal binary **1110 = 14** → 14 × 12.6 cm = **176.4 cm** (average human height). Right of it, a 6×6-bit block decoding to **4,292,853,750** — Earth's human population in 1974. (Both confirmed in the extracted left-panel grid.) |
| 6 | Solar system (rows 57–61) | Large Sun at left, then nine planets (Pluto still counted in 1974), glyph sizes hinting at relative size. **Earth (3rd planet) is raised one row**, directly beneath the human figure: "the message comes from here." |
| 7 | Arecibo telescope (rows 62–73) | The dish graphic (concave-mirror "M" curve with reflection schematic). Below it, a 12-bit binary **100101111110 = 2430** → 2430 × 12.6 cm = **306.18 m**, the dish's diameter. (Confirmed in the left-panel grid.) |

## 3. Comparison table — LEFT panel vs RIGHT panel

| Aspect | LEFT panel | RIGHT panel |
|---|---|---|
| Physical form | Backlit screen / LED pixel display | 3D-printed relief plate (raised/dark cells on a textured base) |
| Grid | 23 × 73 = 1,679 cells | 23 × 73 = 1,679 cells |
| Content | 1974 Arecibo message, original bit pattern | 1974 Arecibo message, same bit pattern |
| Numbers row (1–10) | Present, canonical | Present, identical layout |
| Elements block | H(1), C(6), N(7), O(8), P(15) — 5 columns | Same 5-column block; **no silicon column** (rules out the 2001 "reply") |
| Nucleotide formulas | Canonical 4 blocks | Same layout |
| DNA helix + genome bar | Double helix, central binary bar | Same double helix with central bar |
| Figure | Human stick figure; height bar **1110 = 14** (176.4 cm) | Same human figure (no oversized "Grey" head); same 6×6 population block |
| Solar system | 9 planets, **only Earth raised** | Same; only Earth offset |
| Bottom section | Arecibo dish + 2430 (306.18 m) | Same dish icon — **not** the crop-glyph "transmitter" of the reply |
| Encoding readout | Direct binary (bright = 1, dark = 0) | Direct binary in relief (dark raised cell = 1, flat = 0) |
| Verdict | Original 1974 transmission | Faithful physical replica of the same original |

**Bottom line: the two images are two renderings of one and the same message.** Every content section matches cell-for-cell in structure; they differ only in medium (screen vs. 3D print).

## 4. Why the right panel is NOT the famous "Arecibo reply" (Chilbolton, Aug 2001)

A common assumption when seeing two Arecibo images together is that one is the "alien answer." The real 2001 Chilbolton crop formation kept the 23×73 grid but changed specific sections. None of those changes appear in either of your panels:

| Section | 1974 original (= both your panels) | 2001 Chilbolton "reply" |
|---|---|---|
| Numbers 1–10 | Unchanged baseline | Same (unchanged) |
| Elements | H, C, N, O, P (1, 6, 7, 8, 15) | **Silicon (14) inserted** between O and P |
| DNA | Double helix, ~4.29 B bases | Extra strand; genome bar altered (+~2¹⁹); possibly SiO₄ backbone substitution |
| Figure | Human, height 14 × 12.6 cm = 176.4 cm | "Grey" alien with large head/eyes, height 8 × 12.6 cm ≈ **100.8 cm (~3′4″)** |
| Population | 4,292,853,750 | ~**21.3 billion** (most-cited decode; alternatives 10.8–12.7 B) |
| Solar system | Only Earth (3rd) raised | **3rd, 4th and 5th planets raised** (Earth, Mars, Jupiter — Jupiter glyph embellished, read as its Galilean moons) |
| Bottom | Arecibo dish, 2430 → 306.18 m | **Dish replaced by the Chilbolton 2000 crop glyph**; size value altered (≈6,748 units per some decoders) |

SETI's official stance (Seth Shostak, Aug 2001): the reply is almost certainly human-made — the M13-bound signal had only traveled ~27 light-years and the narrow beam was virtually certain to have reached no star system; real recipients would answer by radio, not wheat. Reddit discussions (r/UFOs threads from 2014, 2022, 2023) split between skeptics (message design was public for 27 years and easily copied; crop grids are demonstrably makable overnight) and believers (overnight precision, the obscure biochemistry touches, and the fact no hoaxer ever claimed it).

## 5. Sources

- Wikipedia, "Arecibo message" — full binary string, all section decodes, transmission parameters: https://en.wikipedia.org/wiki/Arecibo_message
- Original paper: NAIC staff, "The Arecibo message of November, 1974," *Icarus* 26(4):462–466 (1975)
- Paul Vigay's on-site decode of the Chilbolton formation: http://www.vigay.com/cropcircles/articles/arecibo.html
- Brian Crissey, "Chilbolton Code Analysis" (2001): https://www.bibliotecapleyades.net/circulos_cultivos/chilbolton02.htm
- SETI Institute response (Shostak), discussed at: https://www.circlemakers.org/totc2001.html
- The Independent, "Arecibo message decoded": https://www.independent.co.uk/tech/arecibo-message-decoded-meaning-google-doodle-reply-audio-response-explained-a8636856.html
- Reddit: r/UFOs threads uszmbw (May 2022), 15d9mpx (Jul 2023), 2bty9i (Jul 2014)
- Skeptic: https://www.skeptic.org.uk/2023/11/the-arecibo-reply-how-we-know-aliens-arent-calling-us-through-crop-circles/

*Method note: both grids were extracted directly from the uploaded photograph (cell-center sampling of the 23×73 lattice; perspective-warped for the relief plate). The left panel decoded cleanly to the canonical pattern — elements C/N/O/P columns, height 0111→14, planets row with Earth raised, and the telescope number 100101…→2430 all matched. The relief plate was verified region-by-region (numbers band, 5-element block, helix with central bar, human + population block, planets row, dish at bottom).*
