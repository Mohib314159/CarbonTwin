# CarbonTwin — Your Complete Briefing (from zero)

Read this once slowly and you'll go from "I don't know what Treefera is" to "I can
hold my own in the Q&A." It's long on purpose. Plain English first; the maths is
explained so you can *defend* it, not just recite it.

---

# PART 1 — THE WORLD YOU'RE WALKING INTO

## What a carbon credit is
A **carbon credit** = a certificate saying "one tonne of CO₂ was kept out of, or
pulled from, the atmosphere." Companies buy them to offset their own emissions. A
farmer who changes their practices to store more carbon in their soil can, in
principle, generate credits and get paid.

## Why the market is in trouble (your opportunity)
The market is built on **trust**, and trust has been collapsing. In 2024 the
voluntary agricultural-carbon market shrank ~57% (about $85M down to $36M) because
buyers stopped believing the credits were real. At the same time, investment in
"digital MRV" (the verification tech) surged to ~$2.3B, and by 2027 an estimated
90% of carbon transactions will require satellite verification. Only ~5% of
projects pass the strictest integrity screens. **Translation: the world urgently
needs cheap, credible, automated proof that a credit is real. That's the problem
CarbonTwin attacks.**

## The four hard problems every credit must pass
1. **Additionality** — *would this have happened anyway?* If the farmer would have
   planted cover crops regardless, paying them changes nothing, and the credit is
   fake. To prove additionality you must compare against a **counterfactual**: what
   *would* have happened without the practice. This is the heart of CarbonTwin.
2. **Permanence (durability)** — *does the carbon stay put?* If a farmer ploughs the
   field in year 3, the stored carbon is released and the credit is void. Someone
   has to keep watching. (Our reversal monitor.)
3. **Leakage** — does reducing emissions here just push them elsewhere? (We don't
   tackle this; know the word.)
4. **MRV** — **M**easurement, **R**eporting, **V**erification. The whole pipeline of
   proving and auditing the above. Traditionally slow, manual, expensive.

## Regenerative agriculture (the Iowa challenge)
- **Cover cropping**: planting something (e.g. cereal rye) in the off-season so the
  soil isn't bare over winter. The roots add organic carbon to the soil. Published
  large-scale MRV (Indigo Ag) found cover cropping sequesters about **1.29 tonnes
  CO₂e per hectare per year** on average — that's the real number behind our band.
- **No-till**: not ploughing. Ploughing breaks up soil structure and releases
  carbon; no-till keeps it locked in. The Iowa farmer started cover crops in 2021
  and no-till in 2023.
- **Soil organic carbon (SOC)** is the biggest land carbon store on Earth (~2,500
  gigatonnes in the top 3 m — more than the atmosphere and all plants combined).
  Croplands could sequester an extra ~0.9–1.85 GtCO₂e/year. Big prize, hard to measure.

## Satellites & the signals we read
- **NDVI** (Normalised Difference Vegetation Index) = `(NIR − Red)/(NIR + Red)`.
  A greenness number from ~0 (bare soil) to ~0.9 (lush canopy). Plants reflect
  near-infrared (NIR) strongly and absorb red light, so the ratio measures how much
  living, photosynthesising plant is there. **Cover crops show up as *off-season*
  NDVI** — greenness in winter when a bare conventional field would be brown.
- **Red-edge / NDRE**: a band between red and NIR that's sensitive to chlorophyll.
  Plant stress (disease) shows here *before* overall greenness drops — the basis of
  our disease example.
- **SAR (radar, Sentinel-1)**: bounces microwaves off the ground; sees *structure
  and roughness*, works through clouds and at night. It responds to **soil
  disturbance (tillage)** — which NDVI can't see. This is why no-till is a job for
  radar (our roadmap, not a built feature).
- **Clouds** are the enemy of optical satellites; a cloudy pixel is useless. We fix
  this with **median compositing** (take the median of all cloud-free looks in a
  month) and refuse to judge fields whose key window is too cloudy.
- **Resolution & sensors**: Sentinel-2 = 10 m, free, has red-edge and SWIR bands.
  **PlanetScope** = sub-5 m (the Theme-B data), near-daily, but only RGB+NIR (no
  SWIR) and it switched sensor generations mid-archive (PS2 → PSB.SD), which can
  create a fake "jump" in the data. (Our method cancels that — see Q&A.)

---

# PART 2 — WHO TREEFERA IS (know your judges)

- **Founded 2022, London.** Raised ~$40–44M (pre-seed → Series A $12M → Series B
  $30M). ~45 staff. A "first-mile intelligence platform" for carbon & soft commodities.
- **Jonathan Horn** — CEO, **theoretical physicist and former Managing Director at
  J.P. Morgan** (ran risk). He will want statistical rigour, error bars, and no AI
  hype. **Caroline Grey** — co-founder, ex-UiPath. Advisor: **Manuela Veloso**,
  Head of AI Research at J.P. Morgan and a famous CMU professor.
- **What they sell:** satellite + drone + ground data + AI → "Market, Risk and
  Environmental Intelligence at plot resolution, in near real time." They turn
  first-mile conditions into "financial-grade, auditable, defensible" evidence for
  carbon accounting, project validation and regulatory (EUDR) compliance.
- **What they ALREADY have** (important — don't claim you invented these):
  - Additionality and **durability** assessment (their Anew Climate partnership is
    explicitly about "forest carbon project additionality and durability").
  - **Reversal-risk** insight and pricing (fire, flood, drought).
  - Deforestation detection, EUDR supply-chain assessment, carbon baselines,
    "agricultural management practice detection," comparing a field to nearby farms.
- **The gap you fill (your honest pitch):** their additionality/durability is mostly
  **forest carbon**, estimated with **machine learning**. Yours is **field-scale
  regenerative agriculture** using **econometric synthetic control** — a transparent
  *causal* method that yields an **auditable counterfactual with a p-value**, plus an
  explicit **fraud/false-claim verdict**. You're not rebuilding their product; you're
  bringing a rigorous, regulator-friendly method into a domain (soil/ag) that's their
  newer frontier.

---

# PART 3 — WHAT YOU BUILT (CarbonTwin), in plain English

**One sentence:** *"CarbonTwin is a causal engine that verifies a farm's carbon
claim from satellite data — proving whether a practice really caused a benefit,
catching false claims, watching for reversals, and pricing the risk — with a p-value."*

## The core idea: the "synthetic twin"
You can't see the parallel universe where the farmer *didn't* adopt cover crops. So
we **build** it. We take many neighbouring conventional fields and find the weighted
blend of them that best matches the target field's NDVI **before** 2021. That blend
is the field's **synthetic twin** — its counterfactual. After 2021, if the real
field is greener in winter than its twin, that gap is the **additional** effect of
the cover crops. The twin feels the same weather (a drought hits both), so weather
cancels out — only the practice remains. This is the **Synthetic Control Method**
(SCM), borrowed from economics (Abadie et al.), first used on satellite data by
Fick et al. in 2021, and used since for deforestation, fisheries and wildfire.

## The components (each is a module in the repo)
- **Synthetic control** (`scm.py`): builds the twin. Weights are forced to be
  positive and sum to 1 (a weighted *average*) — see Q&A for why.
- **Placebo test** (`inference.py`): gives the **p-value** — how surprised we should
  be by the gap. (Explained in Part 4.)
- **Carbon** (`carbon.py`): converts a *verified* greenness effect to an indicative
  tCO₂e using the published literature band (0.2–2.0 tCO₂e/ha/yr). Honest: this is a
  triage estimate, not a measured tonnage.
- **Audit** (`audit.py`): the **five verdicts** —
  - 🟢 **VERIFIED** — significant real effect → credit it.
  - 🟠 **PARTIAL** — real but smaller than claimed → credit the verified part.
  - 🟣 **INCONCLUSIVE** — weak/uncertain signal, or too cloudy → *don't credit, don't
    accuse; go look.* (This honest "I don't know" state is a feature.)
  - 🔴 **REJECTED** — claimed a practice but the field is flat → possible false claim.
  - ⚪ **BASELINE** — no claim, no change → a normal donor field.
- **Permanence monitor** (`monitor.py`): keeps watching; if a verified credit's
  effect collapses (farmer ploughs up), it flags a **REVERSAL** with the year. Also
  **detects the adoption year itself** from the data (the literal Theme-B question).
- **Actuary** (`actuary.py`): turns reversal risk into a **survival curve** and an
  *illustrative* insurance premium. (Treefera already prices reversal risk, so frame
  this as "an econometric reversal model," not a new invention.)
- **Portfolio** (`portfolio.py`): rolls everything up — verified tonnage, $ of
  claimed-but-unverifiable carbon (fraud exposure), tonnage at reversal risk.
- **Dashboard** (`dashboard.py`): the Streamlit app that shows all this.

## It's a *general* engine (the multi-theme proof)
The same SCM + placebo machinery, with a thin per-domain wrapper, also:
- detects **Saudi pivot-circle abandonment** as aquifers deplete (Theme E) — a green
  circle collapsing to desert is the same "regime change" maths;
- flags **crop disease 2–3 weeks before it's visible in NDVI** (Theme F), by running
  on a red-edge stress index instead of NDVI.
Honest line: the *temporal* themes (B, E, F) share one engine; the *spatial* ones
(the dingo fence, the NZ river fork) would need a difference-in-differences variant.

## How you know it works (the validation — your anti-"you faked it" shield)
We generate synthetic data where we **secretly plant the truth** in every field
(honest adopters, over-claimers, weak adopters, liars, reverters, controls), plus
the real-world nasties (a shared drought year, the PlanetScope sensor jump, ~25%
cloud gaps, noise). The engine has to *recover the truth it can't see*. It scores
**97% overall**, catches **100% of liars and 100% of reversals with zero false
credits**, and dates every real adopter to 2021. That's the proof it's not a rigged
demo — it recovers hidden ground truth on messy data. (Run `make validate`.)

## What you deliberately did NOT build (say this — it's a strength)
- No fake per-pixel "counterfactual satellite image" (would be a hallucinated blob on
  real data).
- No fabricated radar demo (you have no real SAR for Iowa; you kept it as an honest
  roadmap).
- No "autonomous agent that liquidates farmers' accounts" (in real finance you price
  risk, you don't auto-execute on one signal — Horn knows this cold).

---

# PART 4 — THE MATHS, SO YOU CAN DEFEND IT

## Synthetic control — what the optimiser does
We solve: choose weights **w** (one per donor field) to minimise the squared
difference between the target's pre-2021 NDVI and the weighted sum of the donors'
pre-2021 NDVI. Subject to: every weight ≥ 0, and all weights sum to 1.

- **Why ≥0 and sum to 1 (convexity)?** It forces the twin to be a *weighted average*
  of real fields — an interpolation that can never be greener or browner than the
  donors actually were. Ordinary regression would allow huge positive/negative
  weights that fit the pre-period perfectly by *extrapolating* to an impossible field
  — i.e. overfitting to noise. In a small donor pool that overfitting risk is worse,
  so the convex constraint is a strong, honest regulariser. Bonus: weights come out
  sparse, so you can *name* the few neighbours that built the twin.

## Placebo test — where the p-value comes from
- **The problem:** one treated field isn't a sample; you can't get a normal standard
  error. **The fix (Abadie's idea):** pretend each *donor* was the treated one, build
  its twin from the *other* donors, and measure its post-2021 gap. Do this for all
  donors → you get a **null distribution** of "gaps you'd see by chance" in fields
  where nothing happened.
- **Test statistic:** the **RMSPE ratio** = (size of the post-2021 gap) ÷ (size of the
  pre-2021 fit error). A real effect fits tightly before and diverges sharply after →
  big ratio. A field that just fits badly everywhere → small ratio.
- **p-value** = the fraction of placebo fields whose ratio is as extreme as the real
  field's. p = 0.048 with 20 donors means: only 1 in 21 fake-treated fields diverges
  as much as this one. **Null hypothesis:** "this field behaves like an untreated
  field — the practice had no effect." A small p lets us reject that.
- **Why it's valid with one treated unit:** it's a *randomisation/permutation* test,
  not a parametric one. It makes no assumption about the data's distribution; it asks
  an exact combinatorial question about how the real field ranks among controls. That
  is a legitimate, standard inference (the same logic as Fisher's exact test).

## The honest carbon caveat
NDVI measures greenness, not carbon. So we never claim a precise tonnage. The
*statistics* prove additionality; the *tonnage* is a literature-bounded triage
estimate (0.2–2.0 tCO₂e/ha/yr, central ≈ the published ~1.0–1.3). Real crediting
needs soil cores to calibrate. Saying this *gains* credibility with a physicist.

## Two robustness details (mention if pushed)
- **Adaptive thresholds:** the "baseline fit too weak to trust" cutoff scales to the
  donor pool's own typical fit error (the dataset's noise floor), so the method
  doesn't break on noisier real data.
- **Coverage gate:** if a field's off-season window is mostly cloud-filled, we return
  INCONCLUSIVE rather than interpolating a fake flat line and calling it "no cover crop."

---

# PART 5 — Q&A: THE BRUTAL QUESTIONS + YOUR ANSWERS

**"Treefera already does additionality and reversal risk. What's new?"**
"You do it for forest carbon with machine-learning baselines. I bring econometric
synthetic control to field-scale regenerative agriculture — a transparent causal
counterfactual with a placebo p-value an auditor can interrogate, plus an explicit
false-claim verdict. It's a complementary method in your newer ag domain, not a
rebuild of your forestry product."

**"One field isn't a sample. Why is your p-value meaningful?"**
(Part 4, placebo paragraph.) "It's a permutation test — I rank the real field's
divergence against every neighbour re-tested as a fake-treated unit. No distributional
assumptions; it's the same exact-test logic as Fisher. p=0.048 means 1 in 21 control
fields diverges this much by chance."

**"Why convex weights, not regression?"**
(Part 4.) "To forbid extrapolation. Free weights overfit a small donor pool by
building an impossible field; convex weights keep the twin a real-world-plausible
average and give sparse, interpretable weights."

**"NDVI isn't carbon."**
"Correct — that's the weakest link, so I don't fake it. The causal *significance* is
what I prove; the tonnage is a literature-bounded triage number that needs soil-core
calibration. Cover cropping is ~1.3 tCO₂e/ha/yr in the published large-scale MRV;
I carry a 0.2–2.0 band, not a fake-precise figure."

**"Isn't this just a before/after comparison or difference-in-differences?"**
"No — those assume the control trend equals the treated field's counterfactual.
Synthetic control *builds* a bespoke counterfactual weighted to match this field's
pre-history, and the literature shows it catches effects that before-after, BACI and
interrupted-time-series designs miss."

**"How do you handle clouds and different sensors?"**
"Monthly median composite for clouds; if the signal window is mostly cloud-filled the
field returns INCONCLUSIVE. Sensor jumps like PlanetScope PS2→PSB.SD hit the target
and its donors equally, so they cancel in the difference — that's a benefit of a
counterfactual method."

**"Did you just tune this to your own synthetic data?"**
"The thresholds adapt to each dataset's noise floor, and significance is
non-parametric, so it travels. And the synthetic data is a *test*, not a demo — I
plant hidden truth and require recovery; it scores 97% with zero false credits."

**"What about the 2023 no-till? You didn't detect that."**
"We do, by fusing a second channel. Optical NDVI catches the cover-crop year (2021,
a rise in off-season greenness). No-till is the *absence of soil disturbance* — invisible
to greenness but visible to radar, because C-band backscatter responds to the canopy-soil
structure, so tillage leaves a signature that vanishes when a field goes no-till. The same
SCM engine on the radar channel detects the no-till year (2023, a fall). So we answer the
FULL question — both transitions. Honesty: the radar is simulated in our harness to prove
the fusion; real Sentinel-1 is free and global on Earth Engine and plugs into the same
channel-agnostic pipeline. It also closes the weeds-vs-cover-crop loophole: weeds green a
field but don't change the tillage signal."


"No-till is near-invisible to optical NDVI — it's about soil disturbance, not
greenness. That's exactly what Sentinel-1 radar sees, because radar responds to soil
structure. It's my roadmap, and I built the pipeline channel-agnostic so a radar
control plugs straight in."

**"What if the farm is in the Southern Hemisphere? Your seasons are flipped."**
"The off-season window is latitude-aware. Cover crops show as off-season greenness;
in the Northern-Hemisphere corn belt that's ~Oct–Apr, and the code shifts it by six
months below the equator (Brazil/Argentina ~Apr–Oct). So I track the genuine
off-season rather than mistaking their summer harvest for a missing cover crop."

**"What about spatial spillover / SUTVA — your neighbours aren't independent?"**
"Real concern. If the target's practice changes runoff or microclimate, nearby donors
are contaminated. The fix isn't to destabilise the optimiser with a distance penalty —
it's a **spatial buffer** in donor selection: exclude donors within, say, 1 km of the
treated field, drawn from the wider county. My pipeline takes a `buffer_m` argument that
does exactly this; the convex solver then runs unchanged on a physically clean pool.
That's the standard applied-econometrics fix and it keeps the method auditable."

**"Why synthetic control instead of a deep-learning model?"**
"Auditability. A regulator or assurer can't interrogate a neural net's hidden
weights. Synthetic control is transparent: you can see which real neighbours built
the baseline and test significance with a permutation p-value. For *evidence*, that
defensibility matters more than raw predictive power."

**"What would you do with more time / how does it scale?"**
"Pull real Sentinel-2 and Sentinel-1, fuse radar for tillage, calibrate the carbon
band against soil cores, and run it across a whole region — colour the map, send
inspectors only to the red (rejected/reversing) fields. The maths is O(donors); it
scales."

---

# PART 6 — THE 5-MINUTE PRESENTATION (see PITCH.md for the full script)
1. **Hook**: the Iowa farmer who didn't know he was being watched from space.
2. **Verify + catch the liar**: the verified-vs-rejected chart side by side.
3. **Permanence**: the reversal timeline (credited carbon flatlines, then collapses).
4. **Price + portfolio**: survival curve + fraud-exposure number (calibrate emphasis
   to the judge — rigour for a space-agency judge, risk language if Horn is there).
5. **One engine, any natural experiment**: the aquifer (and optional 10-sec disease),
   then the honest close ("what we didn't build, and why"). Map it to Treefera's
   real products: practice detection + carbon baselines, *plus* the fraud check,
   permanence monitor and reversal price they don't yet have.

---

# PART 7 — GLOSSARY (quick reference)
- **Additionality** — would the benefit have happened without the incentive? Needs a counterfactual.
- **Permanence / durability** — does the stored carbon stay stored?
- **Leakage** — emissions pushed elsewhere rather than removed.
- **MRV** — Measurement, Reporting, Verification.
- **Counterfactual** — what would have happened otherwise; the "twin".
- **Synthetic Control Method (SCM)** — builds a counterfactual as a weighted blend of control units.
- **Donor pool** — the control fields the twin is built from (here: no-claim neighbours).
- **Placebo / permutation test** — re-running the method on controls to get a null distribution and a p-value.
- **RMSPE ratio** — post-period gap ÷ pre-period fit error; the significance statistic.
- **p-value** — probability of seeing a gap this big by chance; small = significant.
- **Convex weights** — non-negative, sum to 1; force an interpolation, prevent overfitting.
- **NDVI** — greenness index `(NIR−Red)/(NIR+Red)`.
- **NDRE / red-edge** — chlorophyll-sensitive index; shows stress before NDVI does.
- **SAR (Sentinel-1)** — radar; sees structure/tillage, works through cloud.
- **SWIR** — shortwave infrared; used for tillage/residue indices (Sentinel-2 has it, PlanetScope doesn't).
- **Median composite** — monthly median of cloud-free pixels; the standard cloud fix.
- **EUDR** — EU Deforestation Regulation; supply-chain compliance Treefera serves.
- **SOC** — soil organic carbon, the biggest land carbon store.
- **tCO₂e** — tonnes of CO₂-equivalent; the unit of a credit.
- **Reversal** — a verified credit's carbon being released again (e.g. ploughing).
- **Leakage / additionality / permanence** — the three accounting tests for a quality credit.

---

*You don't need to memorise the code. You need to be able to say, in your own words:
what additionality is, why a counterfactual is the honest way to prove it, what the
synthetic twin is, why the p-value is valid from a permutation test, why you don't
overclaim the carbon number, and what Treefera has versus what you add. Own those six
things and you'll be calm in that room.*

---

# PART 8 — DEEPER DIVE (for the hardest questions)

## 8.1 The maths, one level down

**What the optimiser actually solves.** Given the target's pre-2021 NDVI vector `y`
(length = number of pre-dates) and the donor matrix `X` (pre-dates × donors), it
finds weights `w` solving:

  minimise ‖y − Xw‖²  subject to  wᵢ ≥ 0  and  Σwᵢ = 1.

This is a **convex quadratic program**. Geometrically, `Xw` with those constraints
is the **convex hull** of the donor fields — every point you can reach by averaging
them. The optimiser finds the point in that hull closest to the target's pre-history.
Because it's a hull (not a linear span), the twin can never be *more extreme* than
the donors actually were — no extrapolation. That's the entire reason for the
constraints, and it's why the method is robust on a small, collinear donor pool.

**Worked placebo example.** Say the target's RMSPE ratio (post-gap ÷ pre-fit error)
is 6.0, and you have 20 donors. You re-fit each donor as a fake-treated unit on the
other 19 and get 20 ratios, e.g. mostly between 1 and 3 with one at 5. Count how many
placebo ratios ≥ 6.0: suppose none. Then p = (0 + 1)/(20 + 1) = 0.048. Reading:
"a divergence this sharp, relative to pre-fit, happened in 0 of 20 untreated fields;
the chance of it under the no-effect null is about 1 in 21." The `+1` makes it
slightly conservative (you can never claim p = 0).

**Why the RMSPE *ratio*, not just the post gap?** A field that fits its twin badly
*before* treatment isn't a credible counterfactual, so a big post gap there is
meaningless. Dividing by pre-fit error penalises bad fits and rewards the signature
that actually implies causation: tight before, divergent after.

## 8.2 Multiple comparisons at scale (the FDR finding — own this)

Run the audit on 10,000 fields and ~5% of genuinely-unchanged fields will show
p < 0.05 by chance. Trusting raw per-field p at scale would manufacture false
positives. The fix is **Benjamini-Hochberg FDR control** across the batch (in
`inference.py`), which caps the expected proportion of false discoveries.

**The subtlety I found (a maturity point):** a permutation p-value from `m` donors is
*floored* at 1/(m+1). With 20 donors that's 0.048, so BH — which needs p ≤ α·(rank/n)
— is overly strict and rejects everything on a tiny pool. At **county scale** you have
hundreds of donors, the p resolves finely, and BH works as intended. So the honest
line: *"FDR is the right control and it's implemented; it requires a reasonably large
donor pool per field, which at scale you have. Until then, the INCONCLUSIVE state
prevents false accusation of honest-but-weak fields."*

## 8.3 Is the validation circular? (No — be ready to prove it)

Each synthetic field is an **independent draw**: its own baseline, its own amplitude,
its own phenology curve, plus shared shocks and noise. Adopters are **not** built as a
blend of the donor fields — the cover-crop effect is *added* to an independently
generated series. So synthetic control reconstructing an adopter from a convex mix of
*other, independently-generated* donors is a genuine test of the method, not a tautology.
If the adopters had been constructed *from* the donors, 97% recovery would be circular —
they weren't, so it isn't.

## 8.4 Honest limitations & production roadmap (your closing slide — steal their ammo)

State these before they ask:
1. **NDVI is a proxy, not carbon.** Statistics prove additionality; tonnage is a
   literature band (≈1.3 tCO₂e/ha/yr) needing soil-core calibration.
2. **Small-N inference.** p floors at 1/(donors+1); <19 clean donors can't reach
   95%. Fallback: triage flag → wider donor pool or ridge-augmented SCM review.
3. **Southern-Hemisphere phenology** — handled (latitude-aware mask), but flagged as
   a calibration the pipeline performs.
4. **Constant-hazard pricing.** Exponential survival is a baseline; production fits a
   **Weibull** (shape k≠1) for early-adoption friction and contract-expiry spikes.
5. **Spatial spillover (SUTVA).** Handled by a donor buffer; not validated against
   *modelled* spillover here.
6. **Homogeneous donors.** Our synthetic donors share a crop curve; real fields are
   more heterogeneous, so real matching is harder — argues for covariate-matched
   donor selection (maps to Treefera's "Location Similarity").
7. **No-till is near-invisible to optical** — Sentinel-1 radar roadmap.

## 8.5 More questions you might get

**"What's the confidence interval on the effect size, not just the p-value?"**
"The placebo distribution *is* the uncertainty: the spread of placebo gaps is the
null band. A bootstrap over donor composition would give a CI on the point estimate;
I report significance and a bounded carbon range rather than a fake-precise tonnage."

**"Why not difference-in-differences or regression discontinuity?"**
"DiD assumes parallel trends — that the average control equals this field's
counterfactual. SCM *builds* a bespoke weighted counterfactual matched to this field's
pre-history, which is strictly more flexible. RDD needs a spatial/temporal cutoff,
which fits the dingo fence (a boundary) but not a field's adoption in time."

**"Why not just threshold winter NDVI? Greenness in January = cover crop."**
"Because a wet winter greens every field — you'd credit weather. The whole point is
the *counterfactual*: the twin sees the same winter, so only the difference survives.
A fixed threshold has no defence against shared shocks; that's what broke trust."

**"How do you choose the treatment year?"**
"Two ways: take the claimed year for verification, and *independently* detect it from
the data (sustained off-season divergence) — if detected ≠ claimed, that's itself a flag."

**"Why a median composite, not a mean?"**
"The median is robust to residual cloud/haze that escapes masking — a few bright
cloudy pixels won't drag the monthly value; the mean would."

**"What's creative about your use of the data? Treefera already does all this."**
"Two honest answers. First, on the data: from a single Sentinel-2 cube of raw bands we
extract a whole *stack* of physical signals — NDVI (greenness), NDRE (red-edge chlorophyll
stress), NDWI (water), NDMI (moisture), NDTI (tillage/residue, from SWIR), BSI (bare soil) —
and our engine runs causal verification on *any* of them. One cube, six lenses, one engine.
We handle the real-data gotchas: the Baseline-04.00 +1000 DN step at 2022-01-25 (harmonised
before any index) and n_obs==0 nodata (masked, never interpolated). Second, on Treefera: yes,
they do additionality, practice detection and risk pricing at scale with ML — for forests,
benchmarking 'performance vs nearby farms'. We're not claiming to beat their platform. We add
the *causal-audit layer*: an econometric counterfactual with a permutation p-value and an
explicit fraud verdict, the thing their own site says the market needs — 'financial-grade,
probabilistic, auditable, documented assumptions'. ML predicts; we make the claim defensible."

**"Couldn't weeds look like a cover crop? Both are green in winter."**
"Mean NDVI can't tell them apart — and I won't pretend it can. But a planted cover
crop is drilled, so it's spatially *uniform*; weeds are patchy. At sub-5m resolution we
measure within-field texture, and that separates them: uniform winter green reads as a
managed cover crop, patchy green as likely weeds. It's a *probabilistic discriminator*,
not a perfect classifier — some cover crops establish patchily — so it moves weeds from
an invisible loophole to a flagged low-confidence case. It's real intentionality detection,
and it exploits the sub-5m data Treefera provides."

**"Couldn't irrigation or a crop switch fake your signal?"**
"Possibly — any management change shows in NDVI. That's why this is *evidence for
triage*, not a verdict: a VERIFIED field is one worth a soil core, not an automatic
credit. And a crop switch wouldn't produce the specific off-season signature cover
crops do."

**"What's the compute cost at scale?"**
"Each audit is a small convex solve plus `m` placebo re-fits — `O(m)` per field,
seconds per asset, trivially parallel across fields. It rides on top of an ML
pipeline that does the planetary-scale screening."

---

# APPENDIX Z — Zero-to-Expert (final additions)

## Z1. The new signal modules, in plain English

**radar.py — answering the FULL Theme-B question.** The farmer did TWO things: cover crops
(2021) and no-till (2023). Greenness sees the first (cover crops are green in winter) but is
blind to the second (no-till is the *absence of soil disturbance* — the field can look identical
either way). Radar isn't: C-band backscatter responds to the canopy-soil *structure*, so a
tillage event leaves a signature that disappears when a field stops ploughing. We run the same
synthetic-control engine on a radar "tillage" channel and detect the no-till year as a *fall*,
while the optical channel detects the cover-crop year as a *rise*. Honest caveat to say out loud:
the radar is **simulated in our harness** (no real Sentinel-1 over Iowa in the data); real
Sentinel-1 is free and global on Earth Engine and plugs into the identical channel-agnostic pipe.

**management.py — intentionality, not greenness.** Weeds and a planted cover crop are *both*
green in winter, so NDVI can't tell them apart. But a planted crop is *drilled* → spatially
**uniform**; weeds are opportunistic → **patchy**. At sub-5m we measure within-field texture
(NDVI std, or a GLCM-contrast proxy). Uniform green = managed; patchy green = likely weeds. Say
it as a **probabilistic discriminator** (some cover crops establish patchily) that moves weeds
from an invisible loophole to a flagged low-confidence case. This is the project's boldest
*honest* idea — it reframes you from "detecting greenness" to "detecting human intention."

**spectral.py — six physical signals from one cube (your data-creativity answer).** From the raw
Sentinel-2 bands we extract NDVI (greenness), NDRE (red-edge chlorophyll/nitrogen stress, leads
visible symptoms by weeks), NDWI (open water), NDMI (vegetation moisture, SWIR), NDTI (tillage/
crop residue, SWIR), BSI (bare soil), EVI (biomass, less saturation). Each is a textbook remote-
sensing index; each feeds the same engine. Two real-data gotchas we handle: the **Baseline-04.00
+1000 DN step** at 2022-01-25 (subtract 1000, clamp 0, *before* any index — else every cross-2022
NDVI is wrong) and **n_obs==0 nodata** (masked to NaN, never interpolated into a fake value).

**field_signals.py — the sub-5m extractors (ready for Iowa).** Each turns a pixel cube into a
1-D signal per parcel over time → straight into fit()+placebo_test(), no core change:
- `texture_std` / `texture_contrast` → the weeds-vs-cover-crop discriminator on real pixels.
- `albedo` (mean visible+NIR brightness) → during a bare-soil window, a tillage/no-till signal
  (ploughing flips dark moist subsoil up → brightness drops) and a rough SOC-by-soil-colour proxy.
- `perimeter_ratio` (outer-ring mean / core mean) → "boundary bleed": inputs dumped at the fence
  line to game additionality show up as a perimeter spike vs the field core.
These are weak on the 10m demo (a parcel is few pixels) and come alive on sub-5m. Confirm the
resolution on the day before leaning on them.

## Z2. The CLIP / embeddings question — the honest answer
Gemini pushed CLIP and "512-dim embeddings." The honest version: the engine is signal-agnostic,
so it *can* ingest a time series of embedding-distance like any other array — and the data pack
DOES ship real foundation-model embeddings (AEF, 64-band). So the idea isn't crazy. BUT the demo
embeddings are a **single timestep over France**, so there's no time series to run here — it's an
honest *spoken roadmap* ("learned representations are just another channel"), not a demo. What is
NOT honest and must be refused: CLIP "emotional states" of crops, GNN "dynamic rewiring",
topological data analysis, "systemic risk derivatives" — buzzword maximalism a physicist sees
through, none buildable-and-defensible on monthly/10m data. Saying "we *could* feed embeddings,
here's why the maths is identical" is strong; pretending you built a GNN is fatal.

## Z3. The HTML deck — what it is and how to present from it
`CarbonTwin_deck.html` is a single self-contained file (open in any browser, press F11 for
fullscreen, arrow keys or scroll between the 8 sections). Slides 1–6 are the 5-minute narrative;
slide 7 is the honest close; slide 8 is the **appendix "We know what you'll ask"** — eight
concern→answer pairs you flip to ONLY when a judge asks, never pre-emptively. To present: have it
fullscreen on your laptop, charts already rendered (assets/*.png are embedded). If they want a
PDF, print-to-PDF from the browser. Don't read the slides — they're your prompts; you talk.

## Z4. Delivery masterclass (the only thing left that moves your odds)
You have practised the pitch zero times. This section matters more than any code.
- **Structure each slide as: result → evidence → one sentence of why it matters.** Lead with the
  answer ("This field is verified, p=0.048"), then the chart, then the significance. Never build
  up to a result; state it, then support it.
- **Say the p-value out loud, once, with confidence.** It's your signature. Horn rewards it.
- **The one-breath summary** (memorise, deliver in 20 seconds): "The carbon market collapsed on
  trust because greenness can be faked by weather. CarbonTwin builds each field a synthetic twin
  from its neighbours, so weather cancels, and what's left is the *causal* effect of the practice
  — with a p-value, a fraud verdict, and a reversal price. It's the auditable layer the market
  needs." If you can say that cleanly, you can survive any opening.
- **Handling Horn:** he'll probe NDVI-isn't-carbon and "did you overfit." Concede the true part
  immediately ("you're right, NDVI isn't carbon — which is why tonnage is a literature band, not
  a claim"), then pivot to what you DO prove (causal additionality). Conceding the honest limit
  *builds* trust; defending an overclaim destroys it. Never bluff a number you can't derive.
- **If you don't know:** "I don't know — here's how I'd find out" beats invention every time.
- **Nerves/timing:** rehearse out loud twice, with a timer; aim for 4:30 to leave air. If you
  blank, return to the one-breath summary. Slow down — the instinct under pressure is to rush.
- **What wins the internship:** not duplicating Treefera's platform (impossible in two days, and
  not the bar). It's sharp thinking + rigour + honest creative data use + a clear story. You have
  all four. Stand on it.

## Z5. Final day-of checklist (mirror of HANDOFF.md)
1. Confirm Iowa data format + **resolution** (texture/albedo/perimeter need sub-5m).
2. Thin adapter for their format → Dataset (engine fixed; only the reader changes).
3. Real audit: a VERIFIED field (p-value) + a REJECTED/INCONCLUSIVE one; regenerate 01/02/03.
4. run_real_s2.py → multi-spectral figure on real data (also = Gabrielle's "check it works").
5. If sub-5m: signal_dataset(...,'texture_std') → real intentionality chart.
6. **Stop coding ~14:00–14:30.** Finalise 5 slides. Rehearse out loud ×2. Time it.
