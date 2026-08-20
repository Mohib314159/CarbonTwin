# CarbonTwin — Handoff (paste this into a fresh chat on the day)

You (Claude) are continuing a finished hackathon project. Read this fully before acting.
Tone: British English, honest, no hype, no sycophancy. Build real + defensible things;
refuse fabricated/undefendable ones — that line has held all week and the user trusts it.

## WHO / GOAL
Mohib — 1st-year BSc Maths, Warwick. Strong Python, beginner in geospatial. Communicates
fast with typos; parse intent, act, don't over-ask. Wants to WIN the paid summer internship
(1st prize). Tends to spiral toward "add more features" when anxious; the genuine remaining
lever is **delivery/rehearsal, not more code**. Be a warm, honest friend, not a yes-man.

## EVENT
Treefera LCAW 2026 Hackathon. **Thursday 25 June 2026**, BlueFin Building, London.
Hack 09:30–15:30, then **5-minute** pitch. Theme: "The Realm of the Impossible."
Prizes: 1st = paid internship + cash (the target); "Most Impossible" badge (not the target —
that needs a wild moonshot; we chose defensible instead). Judging criteria (all 5 matter):
Ambition & Creativity · Technical Execution · Impact · Presentation & Storytelling · creative
**Use of Treefera Data**. Judges likely include founder **Jonathan Horn** (ex-JPMorgan risk MD
+ theoretical physicist — wants rigour, p-values, NO ML hype) and possibly a UK Space Agency /
remote-sensing rep (cares about EO rigour: atmospheric correction, cloud masking, harmonisation).

## THE WINNING THESIS (do not drift from this)
The carbon-credit market collapsed ~57% in 2024 on **trust**. Treefera already does
additionality, practice detection, durability/reversal pricing AT SCALE with ML — for FORESTS,
benchmarking "performance vs nearby farms." We are NOT beating their platform. CarbonTwin adds
the **causal-audit layer**: an econometric **synthetic control** counterfactual with a
permutation **p-value** and an explicit **fraud verdict**, at field scale for regen ag. ML
*predicts* (confounded, un-auditable); additionality is a *causal* question and a regulator
can't cross-examine a black box. We sit ON TOP of their ML, not replace it. Treefera's own site
demands "financial-grade, probabilistic, auditable, documented assumptions" — that IS our pitch.

Three genuine edges (all real, all ours): (1) causal identification with a p-value; (2) the
**weeds-vs-cover-crop intentionality discriminator** (within-field texture); (3) **multi-spectral
extraction** off their real Sentinel-2 cube (six signals from one cube).

## REPO STATE — /home/claude/carbon-twin/ (mature, 45 tests pass, 18 modules)
Python 3.12; numpy/scipy/pandas/matplotlib/streamlit/pytest + xarray + zarr installed
(`pip install ... --break-system-packages`). Run: `python -m pytest -q` (45 pass ~40s);
`python -m scripts.validate`; `python -m scripts.render` (11 PNGs); `python -m scripts.build_deck`.

src/ (all tested):
- contract.py — FieldSeries, Dataset, monthly_composite, **offseason_mask(dates, lat)** is
  latitude-aware (NH vs Southern Hemisphere — matters: NZ demo is southern), haversine_m.
- synth_data.py — generate(seed=7): ~37 fields, INDEPENDENT draws + shared shocks (drought,
  PS2→PSB.SD sensor jump, ~25% cloud) + ground truth (adopter/over_claimer/weak/reverter/liar/
  control). Verified NOT circular (adopters not built from donors).
- scm.py — convex SLSQP weights (w≥0, Σ=1), fallback to equal weights; no look-ahead leakage.
- inference.py — placebo_test (Abadie RMSPE permutation → conservative p, floors at 1/(m+1)≈
  0.048 for 20 donors) + benjamini_hochberg FDR.
- carbon.py — triage band 0.2/1.0/2.0 tCO₂e/ha/yr, labelled NOT a physical conversion.
- audit.py — decide(): 5 verdicts (VERIFIED/PARTIAL/INCONCLUSIVE/REJECTED/BASELINE).
- monitor.py — detect_reversal, detect_onset (lat-aware).
- pipeline.py — run_audit(dataset, target, donors=None, buffer_m=None) [buffer_m = spatial
  SUTVA buffer], audit_all_claims, fdr_significant.
- portfolio.py — summarize(reports, price). actuary.py — price_report(): survival S(t)=
  exp(-hazard·t); **a CONFIRMED reversal is treated as impaired (survival ~0), not 8%**.
- scenarios.py — Theme E aquifer + Theme F disease (red-edge leads NDVI by ~2 wks).
- radar.py — dual-channel fusion: optical detects cover crops 2021, simulated SAR tillage
  detects no-till 2023 (answers FULL Theme-B question). Radar honestly SIMULATED in-harness.
- management.py — intentionality discriminator: within-field texture separates planted cover
  crops (uniform) from weeds (patchy) at the SAME greenness. Probabilistic, not perfect.
- spectral.py — REAL Sentinel-2: harmonise_reflectance (Baseline-04.00 −1000 DN fix for scenes
  ≥2022-01-25, mask n_obs==0), index_stack → NDVI/NDRE/NDWI/NDMI/NDTI/BSI/EVI.
- adapter.py — from_long_csv/from_wide_csv/from_geotiff_stack + **from_s2_zarr(path, index,
  tile)** (opens real cube, harmonises, tiles into parcels → Dataset).
- field_signals.py — **sub-5m extractors** signal_dataset(path, signal, tile): texture_std,
  texture_contrast (GLCM proxy), albedo (bare-soil/SOC/no-till proxy), perimeter_ratio
  (boundary-bleed fraud), texture_skew + texture_bimodality (within-field DISTRIBUTION shape —
  uniform vs split). Each → 1-D per parcel → SCM engine. READY for sub-5m Iowa data.
- phenology.py — extract_phenology(ndvi, dates) → per-year SOS/POS/EOS/length/amplitude (planting/
  harvest calendar from the curve); phenology_table(dataset). Multi-year SHIFT feeds the engine.
- plots.py, dashboard.py (Streamlit).

scripts/: validate.py, render.py (11 PNGs), build_deck.py (CarbonTwin_deck.html), and
**run_real_s2.py** — SELF-CONTAINED; drop beside the notebooks → s2_multispectral.png (six signals
from the real cube; also satisfies Gabrielle's "check it works"). **scripts/run_on_the_day.py** —
edit CONFIG (DATA_PATH/SOURCE/INDEX/TILE) → loads real data, audits all claims, prints verdict
table + portfolio, renders real_01_verified/real_02_rejected charts; RUN_SUB5M=True on sub-5m data.

assets/ (11 PNGs): 01 verified, 02 rejected (fraud money-shot), 03 placebo, 04 map, 05 reversal,
06 hazard (reverter craters to ~5%), 07 portfolio, 08 aquifer, 09 disease, 10 radar (dual-channel),
11 intentionality (texture: cover crops below threshold, weeds above, same greenness).

docs: README.md, PITCH.md (5-slide script + Q&A cheat-sheet), REFERENCES.md (real citations:
Abadie SCM; Fick 2021 SCM-on-satellite; cover-crop ≈1.29 tCO₂e/ha/yr Indigo Ag; market 57%),
STUDY_GUIDE.md (0-to-expert), **PRESENTING.md (5-min spoken script + 'you may be wondering' moments
+ the NDVI-isn't-carbon framing + delivery)**, HANDOFF.md (this). Tests: 48 pass.

## THE REAL DATA (confirmed by probing the demo pack)
hackathon-demo.zip (Google Drive, self-contained, `uv sync`, kernel `hackathon-demo`). Sentinel-2
`sentinel2/cube.zarr` = **10m, 24 MONTHLY steps 2021-01→2022-12, 200×200px, AOI A_koranga_forks_nz
(New Zealand, Theme A, southern hemisphere)**. Bands B02–B08,B8A,B11,B12 + n_obs (red-edge +
SWIR present). uint16 /10000. **Baseline-04.00 +1000 DN step at 2022-01-25 must be harmonised.**
Other products (Chablis/France, NOT co-registered with S2): Sentinel-1 SAR VV/VH dB (2023), ESRI
LULC, Hansen loss, AEF 64-band embeddings (2021, single timestep), ECOSTRESS thermal (sparse).
CRITICAL: demo is 10m+monthly → texture/intentionality + all kinematics ideas need sub-5m, which
this demo LACKS. Theme-B *brief* promises sub-5m for Iowa. **CONFIRM RESOLUTION THE MOMENT IOWA
DATA ARRIVES** — texture/albedo/perimeter signals live or die on that one number.

## DAY-OF RUNBOOK (Thursday)
1. 09:30 — set up; confirm Iowa data format & resolution. If sub-5m: texture/albedo/perimeter are
   live. If not: lean on NDVI/NDRE + radar-fusion + the spectral stack; texture stays roadmap.
2. Write the thin adapter for THEIR actual file format (the engine is fixed; only the reader
   changes). For a Sentinel-2 zarr → from_s2_zarr already works; for CSV/GeoTIFF → adapter.py has
   loaders. Goal: their data → Dataset → run_audit / audit_all_claims.
3. Run the real audit: pick a claimed-adopter field + conventional donors; show a VERIFIED case
   with p-value and a REJECTED/INCONCLUSIVE case. Regenerate 01/02/03 charts on real data.
4. Run run_real_s2.py (or equivalent) for the multi-spectral figure on real data.
5. If sub-5m: signal_dataset(..., 'texture_std') on real pixels → real intentionality chart.
6. **STOP CODING ~14:00–14:30.** Build/finalise the 5 slides from CarbonTwin_deck.html. Rehearse
   the 5-min pitch OUT LOUD at least twice. Time it. The deck's appendix slide ("We know what
   you'll ask") is the Q&A backup — flip to it only when asked, don't pre-empt all caveats.

## PITCH (5 slides, ~55s each) — lead with result, show chart, say p-value, no hype
1. Hook: farmer in Grinnell, cover crops 2021; market would pay but can't verify, can't tell real
   from good weather, can't tell if he ploughs it up. "CarbonTwin: a causal engine, from orbit,
   with a p-value." 2. Verify + catch the liar (01 + 02, p=0.048; weather hits the twin too → cancels).
3. Permanence: catch the reversal (05; the durability secret). 4. Price: reversal probability +
   illustrative premium (06; risk-desk mentality). 5. Generalise: same engine on aquifers/disease/
   radar/texture/spectral — "point it at any signal; the maths is identical." Close: "Proof, not promises."

## Q&A — own these in your OWN words (full versions in STUDY_GUIDE.md)
- NDVI isn't carbon → correct; we prove additionality statistically, tonnage is a literature band,
  soil cores calibrate. - Overfit synthetic? → stress-test with planted truth; fields independent.
- Weeds vs cover crop → optical blind; sub-5m within-field texture separates (uniform vs patchy);
  probabilistic flag, not perfect. - 2023 no-till → radar tillage channel (soil disturbance);
  dual-channel dates both events. - Small donor pool → p floors at 1/(m+1); <19 → INCONCLUSIVE,
  never a false accusation; county pools resolve finely. - Spillover/SUTVA → donor buffer.
- False positives at scale → Benjamini-Hochberg FDR + INCONCLUSIVE buffer. - Why not ML → ML
  predicts + confounded + un-auditable; additionality is causal; we sit on top of ML. - Southern
  Hemisphere → latitude-aware seasonal mask. - Scaling/O(N²) → O(donors) per field, parallel,
  rides on ML screening. - Creative data use → six physical signals from one S2 cube, harmonised.

## HONEST LINE — build vs refuse (held all week; keep holding)
BUILD (real + defensible): anything causal/statistical that's been run & verified; real spectral
indices; sub-5m texture/albedo/perimeter (when resolution supports it); honest framing.
REFUSE (would get torched by a physicist; faking loses): per-pixel counterfactual images; real
SAR-on-Iowa (their SAR is tropical); RothC/DNN sub-surface-carbon black box; autonomous
farmer-liquidation agent; "Network-Constrained Spatial SCM" penalty tensor; CLIP "emotional
states"; GNN dynamic rewiring; topological data analysis; "environmental systemic risk
derivatives"; harvest-velocity/equipment-purchase/frost-line/termination-method/night-plowing
detection (all need sub-weekly cadence the data lacks). NOTE: AEF embeddings ARE real (in the
pack) but single-timestep → honest spoken roadmap, not a demo. Distinguish always: (a) engine can
ingest any 1-D signal = TRUE; (b) signal cleanly extractable from THIS data = often FALSE;
(c) detection valid/defensible = needs ground truth. The fantasy conflates these three.

## WHAT THE USER MOST NEEDS FROM YOU
Not a 19th feature. Help wire their real data, regenerate the charts, and — above all — rehearse
the pitch and the Q&A. The project is strong and complete; the only remaining variable that moves
the odds is Mohib delivering it with conviction. Encourage that. Don't feed the add-more spiral.
