# EG / TOG Survey Style Reference

> Goal: extract the structural conventions used by established
> 3DGS / radiance-field survey papers, then transplant the parts
> that lift our draft from "list of bullets" to "field-defining
> review".

We surveyed three arXiv review papers and one EG STAR as reference:

| # | Title | arXiv | Year | Authors | Scope |
|---|-------|-------|------|---------|-------|
| 1 | *3D Gaussian Splatting: Survey, Technologies, Challenges, and Opportunities* | 2407.17418 | 2024-07 | Fei et al. (Wuhan U.) | 3DGS only, 9-module taxonomy |
| 2 | *Recent Advances in 3D Gaussian Splatting* | 2403.11134 | 2024-03 | Chen & Wang (CAS + UCSB) | 3DGS, 3 functional pillars |
| 3 | *A Survey on 3D Gaussian Splatting* | 2401.03820 | 2024-01 | Dellaert et al. (derivative) | Foundational terminology |
| 4 | *Image-based Representations for Accelerated Rendering of Complex Scenes* | EG 2005 STAR | 2005 | Jeschke, Wimmer | Image-based rendering (historic analogue) |

The 2024 trio all cover 3DGS broadly; none of them focuses on
dynamic 4DGS / mobile deployment, which is the gap our survey
addresses.

## Section recipes we should borrow

### 1. Opening: motivation + 3-4 guiding questions

Reference #1 opens with a "nine technical modules" enumeration and
explicitly frames the survey as a "rapid understanding for newcomers
and methodological organisation for researchers". The
*guiding-questions* pattern (4-5 questions answered across the
survey) is the dominant convention. The questions should not be
rhetorical — every section should clearly map to one of them.

**Gap in our draft (§1):** we already list 4 questions, but they
are not labelled and the mapping to §2-§9 is implicit. *Action:*
add an explicit `Q1–Q4 → §2-§9` mapping at the end of §1.

### 2. Background: two-tier pre-requisites

Reference #1 dedicates a section to "preliminaries" (3DGS
fundamentals) and a separate section to "evaluation metrics".
Reference #2 mixes preliminaries into a single §2. The TOG
convention strongly favours separating **technique
background** from **evaluation methodology** — they serve
different audiences.

**Gap in our draft (§2 / §7):** we currently fold mobile GPU
fundamentals into §2 and datasets/metrics into §7. ✓ This matches
the reference style. Keep as-is.

### 3. Taxonomy: orthogonal axes, not just one

Reference #1 uses 9 *technical modules* (not buckets) — a method is
classified by which module it improves. Reference #2 uses 3
*functional pillars* (reconstruction / editing / applications).
Both conventions are valid; the key is to commit to one and make
sections orthogonal (no paper appears in two sections).

**Gap in our draft (§3 / §4 / §5):** we currently split by
*pipeline stage* (representation / training / rendering). This is
fine, but **D 派系 (mobile + streaming) sits awkwardly** — it
spans both training (compression for streaming) and rendering
(on-device rasterisation). The current `D → §6` mapping
collapses this; we should add a one-line note in §3 stating
"deployment-centric work is deferred to §6" to avoid confusion.

### 4. Comparison tables with quantitative rows

Both reference surveys include a **representative-work comparison
table** with columns: Method | Year | Venue | Core idea |
Performance | Code. The table appears in the *first* taxonomy
section, not the last. Numbers are cited verbatim from the paper.

**Gap in our draft (§3):** we have a 5-row qualitative table.
*Action:*
- Add `PSNR / FPS / Model size / Venue` columns.
- Add 2-3 quantitative rows (4DGS-1K, Mobile-GS, Flux-GS).
- Add a 2nd table in §5 (rendering acceleration) covering
  Mobile-GS / Flux-GS / Lumina / GS-NFS with FPS / mobile SoC /
  power columns.

### 5. Discussion: research opportunities, not summary

Reference #1's §11 is titled "Research Opportunities" and lists
**5-7 forward-looking directions**, each with: (a) what is
missing, (b) what early work exists, (c) what specific shape the
next paper should take. This is qualitatively different from a
recap. The discussion section should be **prescriptive**, not
descriptive.

**Gap in our draft (§8):** our "5 directions" are mostly
descriptive ("Feed-forward 4DGS: L2D2-GS opens this path").
*Action:* add a "Missing piece / What next paper should look
like" sub-row to each of the 5 directions.

### 6. Conclusion: explicit limitations of the survey itself

References #1 and #2 end with a "Limitations" subsection
*inside* the conclusion: scope (we only cover 2023-H1 2026),
methodology (we exclude non-English work, arXiv-only preprints
without code), and known gaps. This signals academic rigour.

**Gap in our draft (§9):** no explicit "limitations of the
survey" subsection. *Action:* add a 3-bullet limitations
paragraph before the closing line.

## Stylistic conventions worth copying

- **Active voice in the introduction** ("We present…", "We
  organise…") — academic survey style favours first-person
  plural.
- **Quantitative claims cite PDF page** (e.g. "1080p @ 30 FPS
  (p.~4)"). Our paper notes already do this; surveys should
  propagate the convention into §3-§6 prose.
- **Avoid "we" in description paragraphs** but use it freely in
  meta-paragraphs (intro, conclusion, design rationale).
- **Footnotes for venue abbreviations** on first use (e.g.
  "CVPR — IEEE/CVF Conference on Computer Vision and Pattern
  Recognition"). We have 14+ venue abbreviations in the bib; the
  intro should define the top 5 (CVPR, ICCV, ECCV, SIGGRAPH,
  TOG, ICLR, ICML).
- **No "in this paper we…" filler** — get to the first technical
  content within 2 paragraphs of the abstract.

## Visual conventions

- **Figure 1 in every survey** is a "taxonomy diagram" — a
  tree or radial layout of the section structure. Reference #1
  uses a radial diagram, #2 uses a 2D table with arrows. We do
  NOT have such a figure. *Action:* generate a one-page SVG
  taxonomy diagram (§1 mention "see Figure 1") — single effort,
  high payoff.
- **Tables use booktabs** (already adopted by acmart) with
  horizontal rules and no vertical lines. ✓ Matches.
- **Color is used sparingly** — usually to highlight the
  authors' own contribution or to mark the SOTA. Our Catppuccin
  Mocha palette is fine for the web evolution graph, but the
  PDF should stay monochrome.

## Scope differences (what NOT to copy)

- Reference #1 is 26 pages with 9 technical modules, ours is
  15-20 pages with 9 thematic sections. The "module" approach
  is harder to read but more rigorous; we are not aiming for
  26 pages in v1.
- Reference #2 includes a 4-page related-work recap; we already
  cover related work inline. Skip.
- Reference #4 (EG STAR 2005) is image-based rendering — its
  3-tier structure (acquisition / representation / rendering)
  is structurally similar to ours (representation / training /
  rendering). The 20-year-old taxonomy still works; this is
  evidence that pipeline-stage organisation is the right choice
  for our survey.

## Concrete edit list (v2 priorities)

1. **§1**: add explicit Q1-Q4 → §2-§9 mapping table.
2. **§3**: add a one-line "deployment-centric work is deferred to
   §6" note. Expand the comparison table with quantitative
   columns and 3 representative rows.
3. **§5**: add a mobile-rendering performance table (Mobile-GS /
   Flux-GS / Lumina / GS-NFS × FPS / SoC / power).
4. **§8**: for each of 5 directions, add a "missing piece / what
   next paper should look like" sub-row.
5. **§9**: add a 3-bullet "Limitations of this survey"
   paragraph.
6. **§1 (visual)**: add a one-page taxonomy diagram.

These six edits collectively lift the survey from "list of
bullets" to "field-defining review".
