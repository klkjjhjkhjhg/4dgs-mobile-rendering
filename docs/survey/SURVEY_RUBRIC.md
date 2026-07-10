# Survey Evaluation Rubric

> Goal: give two independent sub-agents a single, scoreable
> standard for assessing the current draft. The rubric is designed
> to surface *actionable* gaps, not just "is the writing nice".

Each dimension is scored 1-5. The total is a weighted average
where weights reflect what an EG / TOG reviewer would weigh
most. The 6 dimensions are derived from the user's standing
spec (`完整性 / 深度 / 前瞻性 / 准确性` + `可读性 / 可复现性`).

---

## 1. Completeness (完整性) — weight 25%

**Definition:** does the survey cover the field's full landscape,
or does it have obvious blind spots?

### What to check (machine-greppable)

- [ ] **All 5 派系 (A/B/C/D/E) are represented** in the survey's
      body, not just INDEX.md.
- [ ] **At least 80% of the 54 paper notes are cited** somewhere
      in the body, not just in the per-section `\item` lists.
- [ ] **No 派系 has < 3 papers cited** in its primary section.
- [ ] **All 9 sections have at least 1 paper citation**.
- [ ] **bib has ≥ 50 entries**; missing entries are documented.
- [ ] **All citation keys used in body resolve in bib** (no
      `Citation undefined` warnings on `pdflatex` run 2).

### Score guide

| Score | Definition |
|-------|------------|
| 1 | Coverage of 1-2 派系 only, >20% papers uncited |
| 2 | 3 派系 covered, 50-80% papers cited |
| 3 | 4 派系 covered, 80-90% papers cited, 1-2 sections with no paper |
| 4 | 5 派系 covered, 90-100% papers cited, all sections have papers |
| 5 | 5 派系 covered, 100% papers cited, all sections balanced (no section has <5% of total) |

---

## 2. Depth (深度) — weight 20%

**Definition:** does the survey go beyond citation listing? Does
it explain *why* a method works, not just *what* it does?

### What to check

- [ ] **Each section's prose explains the mechanism**, not just
      lists papers. (Rule of thumb: ≥ 3 sentences of mechanism
      per subsection.)
- [ ] **Quantitative numbers are present in body** (FPS, PSNR,
      storage, model size) — not only in `\item` lists.
- [ ] **Comparison tables have ≥ 4 columns** (not just "method vs
      trade-off").
- [ ] **Cross-section references exist** (e.g. §5 refers back to
      a §3 method).
- [ ] **No "is proposed" / "is introduced" without context** —
      every method mention should also mention the *problem* it
      solves.

### Score guide

| Score | Definition |
|-------|------------|
| 1 | Mostly `\item` lists, no mechanism explanation |
| 2 | Each section has 1-2 mechanism sentences, no cross-refs |
| 3 | Each section has 3+ mechanism sentences, comparison table has 4+ cols, few cross-refs |
| 4 | Mechanism explanations dense, 2+ comparison tables, 1+ cross-refs per section |
| 5 | Mechanism dense, multiple comparison tables, dense cross-refs, includes derived insights (e.g. "the trend across these 5 papers is X") |

---

## 3. Forward-Looking (前瞻性) — weight 20%

**Definition:** does the survey identify research directions that
are *not yet* obvious from individual papers? Does it make
*prescriptive* predictions, not just *descriptive* summaries?

### What to check

- [ ] **§8 has ≥ 3 future directions** (currently 5; the test is
      *quality* not count).
- [ ] **Each direction names a specific missing piece**, not
      just "more work is needed".
- [ ] **Each direction mentions at least 1 nearby early work** as
      a stepping stone.
- [ ] **At least 1 direction is bold/contrarian** (e.g. "we
      expect hardware-software co-design to matter more than
      algorithmic progress").
- [ ] **Discussion engages with the project's own positioning**
      (our README target on Snapdragon 8 Gen 4 / Vulkan 1.3).

### Score guide

| Score | Definition |
|-------|------------|
| 1 | §8 is a recap of §1-§7, no new directions |
| 2 | 1-2 directions, mostly descriptive |
| 3 | 3-4 directions, each names a missing piece |
| 4 | 4-5 directions, each has missing piece + nearby early work, 1 contrarian claim |
| 5 | 5+ directions, dense prescriptive content, 2+ contrarian claims, explicit link to project's positioning |

---

## 4. Accuracy (准确性) — weight 20%

**Definition:** are the claims in the survey correct, with
verifiable sources, and no hallucinated numbers?

### What to check (machine-verifiable)

- [ ] **Every quantitative claim cites a source** (PDF page or
      paper-note `0.5 元数据` field).
- [ ] **No `\cite{}` undefined** (run `pdflatex` and check log).
- [ ] **No contradictory numbers** (e.g. PSNR 28.5 in §3, 30.2
      in §5 for the same method).
- [ ] **Author / venue / year match the bib entry** (spot check 5
      entries).
- [ ] **Mobile SoC claims match vendor specs** (e.g. "Snapdragon
      8 Gen 4 / Adreno 830 FP32 ~2 TFLOPs" — verify against
      Qualcomm spec page).

### Score guide

| Score | Definition |
|-------|------------|
| 1 | Multiple `Citation undefined`, several uncited numbers, 1+ contradictory claim |
| 2 | Some undefined cites or uncited numbers, 0 contradictions |
| 3 | No undefined cites, 80%+ numbers cited, 0 contradictions |
| 4 | All numbers cited, 0 contradictions, 1 spot-check pass |
| 5 | All numbers cited with PDF page, 0 contradictions, all 5 spot-checks pass, mobile SoC claims verified |

---

## 5. Readability (可读性) — weight 10%

**Definition:** is the survey easy to navigate, with clear
sectioning, consistent terminology, and a logical flow?

### What to check

- [ ] **Each section starts with a 1-2 sentence orientation
      paragraph** that previews the section's content.
- [ ] **Consistent terminology** (e.g. "4DGS" used everywhere, no
      mixing with "dynamic 3DGS" or "temporal 3DGS").
- [ ] **No wall-of-text paragraphs** (>200 words without
      break).
- [ ] **Active voice in intro/conclusion**, descriptive voice
      elsewhere.
- [ ] **No "in this paper we…" filler**.

### Score guide

| Score | Definition |
|-------|------------|
| 1 | No orientation paragraphs, inconsistent terminology, wall-of-text |
| 2 | Some orientation, mostly consistent terminology, 1+ wall-of-text |
| 3 | Every section has orientation, terminology consistent, no wall-of-text |
| 4 | Orientation + consistent terminology + varied sentence structure, no filler |
| 5 | Above + the survey reads like a coherent narrative when read linearly, not just a stack of bullets |

---

## 6. Reproducibility (可复现性) — weight 5%

**Definition:** can a reader reproduce the survey's claims from
the materials provided?

### What to check

- [ ] **bib is complete and machine-readable** (no hand-edited
      fields, all entries have title / author / year / venue).
- [ ] **Survey compiles with `make`** (no manual `latexmk`
      incantation required).
- [ ] **GitHub Action workflow exists and works** (M3 already
      delivered; just verify).
- [ ] **Paper notes are linked from the survey** (so a reader can
      drill down from `\cite{}` to the full paper note).
- [ ] **No proprietary data** (all citations are public arXiv /
      DOI).

### Score guide

| Score | Definition |
|-------|------------|
| 1 | bib incomplete, survey doesn't compile, no workflow |
| 2 | bib OK, compile OK, no workflow |
| 3 | bib OK, compile OK, workflow exists, partial paper-note linkage |
| 4 | Above + every `\cite{}` links to a paper note (or external DOI) |
| 5 | Above + the survey is regenerable from a single `make` invocation, bib is regenerable from `scripts/extract_paper_summary.py --bib` |

---

## Weighted total

`total = 0.25·completeness + 0.20·depth + 0.20·forward + 0.20·accuracy + 0.10·readability + 0.05·reproducibility`

### Interpretation

| Total | Grade | Action |
|-------|-------|--------|
| < 2.0 | F | Major rework required; multiple core dimensions missing |
| 2.0-2.5 | D | Significant gaps; needs another full pass |
| 2.5-3.0 | C | Functional but not submission-ready; targeted improvements |
| 3.0-3.5 | B | Submission-quality with minor edits |
| 3.5-4.0 | A | Strong survey, ready for review |
| 4.0-5.0 | A+ | Top-tier, EG STAR / TOG submission candidate |

---

## How the two sub-agents will use this

1. **Sub-agent A** (the "structuralist") reads the survey cold
   and scores the 6 dimensions. Outputs a JSON object + a
   bulleted "what to fix" list per dimension.
2. **Sub-agent B** (the "skeptic") re-reads the same survey,
   scores the 6 dimensions *without seeing A's output*, and
   writes an independent list. Cross-check the two lists to
   find:
   - **Consensus issues** (both A and B flagged) → must-fix
   - **A-only issues** → likely real, lower priority
   - **B-only issues** → likely real, lower priority
   - **Disagreements** (A scores high, B scores low) → re-evaluate
     with the user
3. The main agent merges the two lists, ranks by impact, and
   dispatches the top 5 to sub-agents for v2 editing.

The two-agent setup catches the "two blind spots" problem: a
single agent (or the author) gets used to the survey's quirks
and stops seeing them.
