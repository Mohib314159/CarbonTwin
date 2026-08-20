# CarbonTwin

**A risk desk for carbon credits.** Most regenerative-agriculture tools answer
*"did this field get greener?"* - which a wet spring can fake. CarbonTwin runs a
three-layer engine on one defensible statistical core:

1. **VERIFY** - was the carbon benefit *caused* by the practice, and does the data
   back the farmer's claim? Returns a verdict **with a p-value**, and catches farms
   that claim a practice they never adopted.
2. **MONITOR** - a credit isn't a one-time stamp. We keep watching and flag a credit
   **reversing in real time** (the farmer ploughs it up in year 3 and the carbon is
   released) - the permanence problem almost nobody monitors.
3. **PRICE** - from the portfolio's observed reversal rate and each field's
   trajectory, we put a **reversal probability and an illustrative risk premium** on
   every credit. Standard actuarial maths, applied to orbital MRV.

Built for the Treefera LCAW 2026 hackathon, Challenge B (regenerative agriculture).

---

## Layer 1 - Verify (causal additionality + fraud)

For each field that *claims* a practice (e.g. cover cropping from 2021), we build a
**synthetic twin**: a convex-weighted blend of neighbouring *business-as-usual*
fields, fitted to match the field's own NDVI **before** the claimed change. After
the change, the gap between the real field and its twin is the **causal
additionality**. A **placebo permutation test** (Abadie et al.) turns that gap into
a p-value. This is the Synthetic Control Method - the standard "one treated unit,
many controls" causal tool - pointed at carbon MRV and at fraud.

Why it beats a greenness detector: a shared drought or wet spring moves *every*
field at once. The synthetic twin experiences the **same** regional weather, so
differencing against it removes the common shock. The same logic neutralises
satellite **sensor jumps** (PlanetScope PS2->PSB.SD): a common-mode shift hits target
and donors alike and is differenced out.

**Five verdicts** (defensibility over cleverness):

| Verdict | Meaning | Action |
|---|---|---|
| VERIFIED | significant effect, real additionality | credit it |
| PARTIAL | real & significant, but **below the claimed amount** | credit verified part |
| INCONCLUSIVE | weak signal, not statistically separable, or window too cloudy | **don't credit, don't accuse - go look** |
| REJECTED | a claim was made but the field is flat | possible false claim, flag |
| BASELINE | no claim, no change | business-as-usual (donor) |

The INCONCLUSIVE state is deliberate: a weak genuine adopter must **never** be
branded a liar, and a clouded-out winter must never be flattened into a confident
"no cover crop".

## Layer 2 - Monitor (permanence / reversal)

We track yearly off-season additionality and the **cumulative credited carbon**. If a
verified credit's additionality collapses relative to its own peak (denoised over the
last two off-seasons), we raise a **REVERSAL alert** with the year it broke -
continuous verification, not a one-off stamp.

## Layer 3 - Price (the Orbital Actuary)

The honest bridge to finance. We do **not** invent a precise per-farmer probability
from radar we don't have. Instead:

```
hazard(field) = base_annual_hazard  x  stability_multiplier(field)
```

- `base_annual_hazard` = the **observed reversal frequency** across the portfolio
  (a frequency estimate - exactly what an actuary starts from).
- `stability_multiplier` = a transparent score from this field's own additionality
  trajectory (declining / volatile credits are riskier).

Exponential survival `S(t)=exp(-hazard*t)` (Weibull is the natural generalisation)
gives a horizon reversal probability and an **illustrative** annual premium
`= price x hazard`. Every number is bounded and labelled indicative - the novelty is
the *bridge*, not a claim of actuarial precision from one short series.

---

## One engine, many regimes (B + E)

CarbonTwin is not a cover-crop detector. It is a causal engine for **regime change
from orbit**: a field *gaining* a practice (cover crops), *losing* it (reversal /
tillage), or an aquifer-fed farm being *abandoned* are all the same question — does
the treated unit diverge from a counterfactual built from its untreated peers, and
is that divergence significant?

To prove it, the **identical synthetic-control solver and placebo test** are run on
**Theme E (Saudi pivot-irrigation abandonment)**: a green circle is reconstructed
from still-irrigated neighbours, and the engine flags the year its aquifer ran dry
as it collapses to desert (see `assets/08_aquifer.png`). On synthetic Theme-E data
it recovers **100% of abandonment years with 0 false positives**.

What is reused (the engine): the convex SCM solve + Abadie placebo inference. What
is domain-specific (a thin, honest wrapper): the signal window (year-round vs
off-season) and whether we hunt a gain or a collapse. The *spatial* themes (the
dingo fence, the NZ river fork) are the same idea with a difference-in-differences
estimator instead of a temporal one — a clear extension, not claimed as done.

---

## Run it

```bash
make install        # numpy / scipy / pandas / matplotlib / streamlit / pytest
make validate       # prove it works on data with known ground truth
make demo           # render the static charts into assets/
make run            # launch the interactive dashboard
make test           # 31 unit + integration tests
```

## Does it actually work? (validation)

`make validate` runs the whole engine on a **synthetic Iowa dataset with planted
ground truth** - every field is secretly an honest adopter, an over-claimer, a weak
adopter, a **reverter**, a liar, or a control. The data carries the real-world
confounders (a shared drought year, the PlanetScope sensor jump, ~25% cloud gaps,
noise). The engine has to *recover the truth it can't see*:

```
adopter      : 100% VERIFIED
over_claimer : 100% PARTIAL          (real, downgraded vs inflated claim)
weak         : 100% INCONCLUSIVE/PARTIAL   (never wrongly accused)
reverter     : 100% VERIFIED + 100% REVERSAL detected
transition yr: 100% of true adopters dated to 2021 (liars: none)
liar         : 100% REJECTED
control      :  95% BASELINE         (5% mild "go look" = expected placebo null)

false-credit (control marked VERIFIED): 0%
false reversal alerts on non-reverters: 0
OVERALL ground-truth recovery: 97.3%
```

Zero honest fields lose credit; zero liars get through; zero controls are wrongly
credited; every reverter's collapse is caught with no false alarms.

## Architecture - built for hackathon day

```
src/contract.py    fixed internal data format + cloud-aware compositing (+ observed mask)
src/synth_data.py  realistic synthetic data + planted ground truth (the test harness)
src/scm.py         synthetic control solver (convex LS, optimiser-failure fallback)
src/inference.py   placebo permutation test -> p-value; Benjamini-Hochberg FDR (multiple-comparison control at scale)   Abadie placebo permutation -> p-value (+ dataset noise floor)
src/carbon.py      verified additionality -> tCO2e, literature band (triage only)
src/audit.py       five-state verdict, adaptive thresholds + coverage gate
src/monitor.py     permanence: reversal detection
src/portfolio.py   risk roll-up: verified tonnage, fraud exposure $, reversal at risk
src/actuary.py     reversal probability + illustrative premium (survival model)
src/scenarios.py   2nd + 3rd worked examples: Theme E aquifer abandonment AND
                   Theme F pre-symptomatic disease (red-edge), same engine
src/pipeline.py    Dataset -> per-field audit (one call the UI + tests share)
src/plots.py       counterfactual / reversal / survival figures
src/dashboard.py   Streamlit app
src/adapter.py     << THE ONLY FILE YOU WRITE ON THE DAY >>
```

On the day, Treefera's real files only need an **adapter**: read their data ->
return a `Dataset`. Everything downstream is built and tested. See `src/adapter.py`
for the Sentinel-2 / GEE recipe (server-side `reduceRegion`, not a pixel dump) and
ready-made loaders: `from_long_csv`, `from_wide_csv`, `from_geotiff_stack`. The full
raw-file -> adapter -> pipeline path is tested end to end (tests/test_adapter.py);
`data/SAMPLE_ndvi_long.csv` shows the expected format.

---

## Defend it (judge Q&A)

**"NDVI isn't carbon."** Correct, and it's the weakest link, so we don't fake it.
The synthetic control rigorously establishes *whether* a causal effect exists; the
tonnage is a literature-bounded triage scaling (0.2-2.0 tCO2e/ha/yr) that needs soil
calibration. We sell the verification and the risk pricing, not a fake tonnage.

**"How do you know the effect is real?"** Placebo test: re-fit every donor as a
fake-treated unit; the field is significant only if it diverges more than the
neighbours do by chance.

**"Your thresholds are tuned to your own data."** They adapt: the "baseline too weak
to trust" cutoff scales to the donor pool's own pre-fit RMSE (the dataset's noise
floor), and significance is non-parametric (placebo), so it travels to noisier data.

**"Clouds? Different satellites?"** Monthly median composite; common-mode sensor
shifts difference out; and a field whose off-season window is mostly cloud-filled
returns INCONCLUSIVE instead of a fabricated flat line.

**"How can you price a 10-year reversal probability?"** We don't claim per-farmer
precision. The hazard starts from the *observed* portfolio reversal rate and is
modulated by each field's trajectory stability; the premium is explicitly
illustrative and would be calibrated on real reversal history. The novelty is
bridging orbital causal inference to actuarial pricing, not the survival maths.

## What we deliberately did NOT build (and why)

Being able to say *no* to the wrong idea is part of the engineering.

- **Per-pixel "counterfactual satellite image".** A rigorous per-pixel synthetic
  control needs spatially-registered pixel donors across many fields; the cheap
  version applies a scalar field-weight to a 2-D grid and produces a hallucinated
  blob that falls apart on real, noisy data. The time-series divergence chart is the
  honest, defensible visual.
- **Sentinel-1 radar (SAR) multi-modal fusion.** Scientifically the strongest
  extension (radar sees tillage; NDVI can be faked by weeds) and a clear roadmap
  item - but it needs real SAR we can't validate here, so we kept the pipeline
  *channel-agnostic* (a second control plugs straight in) rather than ship an
  unvalidated demo.
- **Autonomous "liquidate the farmer" execution.** In real finance you never
  auto-liquidate a livelihood on a single signal - basis risk and liability. We
  *price* risk; humans decide.

## Honest limitations

- NDVI->soil-carbon conversion is indicative and needs ground calibration.
- Needs enough cloud-free history (~3+ years) and a pool of genuine BAU donors.
- Field-level mean NDVI (not per-pixel); within-field variation is averaged.
- The reversal premium is illustrative; calibrate hazard on real reversal histories.
- Validated on synthetic data with known truth; the pre-event homework is to re-run
  on real Sentinel-2 via Google Earth Engine before judging.

*Synthetic data is clearly labelled as such throughout. No results are fabricated -
every number in the validation section is produced by `make validate`.*
