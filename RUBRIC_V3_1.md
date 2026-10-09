# Evidence-Maturity Coding Rubric — version 3

This rubric is the complete coding instruction. Both coders apply this same text, unchanged, to every study.
Do not adjust it while coding. Where it genuinely cannot decide a case, code `tier = UNDECIDABLE`, say why in
`justification`, and move on; do not invent a rule.

## 1. Unit of coding

Code one **study** per row, from the source document named for it.

## 2. Source and confidence

### 2.1 Source of record

Code from the **study itself**. Read at least the abstract, the methods, and the results or findings. Do not
code from the abstract alone: an abstract's design label can differ from what was actually measured (R8).

`source` records which full-text form of the study was read. It describes the reading copy only and is not a
judgment about the study.

| `source` value | Meaning |
|---|---|
| `full_text` | The study's own document, with a native text layer |
| `full_text_ocr` | The full text recovered by optical character recognition from a scanned document; the scan itself is also supplied |
| `full_text_replacement` | A verified open-access copy of the same study, supplied because the original file is unreadable |

The value is pre-filled for each study. Record it as given.

### 2.2 Confidence

`confidence` records how secure the tier assignment is: `high`, `medium` or `low`. Two rules cap it:

1. **Unclear design (R7).** When the design is unclear from the available text, code the lower tier and set
   `confidence = low`.
2. **Recovered or replacement text.** For `full_text_ocr` or `full_text_replacement`, `confidence` is at most
   `medium`, unless the design and the measured outcome are both stated plainly in running prose.

Recovered text can misorder two-column layouts and drop spaces. Verify any number that decides a tier against
the page image of the scan, and do not rely on table values read from recovered text alone.

## 3. Decision tree

Apply the questions in order, to every study, and stop at the first match.

**Q0 — Topic eligibility:** Does the study substantively investigate, evaluate, design, deploy, or analyze
an LLM, generative-AI system, or an AI-enabled system/function relevant to education?

**Adjacent AI system** means a system in which AI-based functionality is itself a material part of the
educational task, intervention, support, decision, or outcome being studied, even when an LLM is not the
sole or primary technology.

**Exclude** studies that merely mention AI/ML/LLMs as background, list them as possible or alternative
methods, or use conventional statistical, database, business-intelligence, or visualization tools without
actually studying an AI-enabled component.

→ NO: `design = OFF_TOPIC`, `tier = NA`. **Stop.**

**Applying Q0 — the adjacent-AI boundary.** Answer from what the study actually does, not from its title,
keywords or abbreviations, which can mean something else in another discipline.

| Q0 = YES (on topic) when the study… | Q0 = NO (`OFF_TOPIC`) when the study… |
|---|---|
| substantively investigates, evaluates, designs, deploys or analyzes an LLM or a generative-AI system relevant to education | mentions AI, ML or LLMs only as background, motivation or context |
| substantively studies an AI-enabled system or function whose AI-based functionality is itself a material part of the educational task, intervention, support, decision or outcome being studied — whether or not an LLM is involved, and whether or not it is the sole or primary technology | lists AI, ML or LLMs only as possible or alternative methods |
| | uses conventional statistical, database, business-intelligence or visualization tools without actually studying an AI-enabled component |

Exclude studies in which machine learning or another AI/ML technique is used only as an analytical tool by the researchers to process data about a non-AI educational subject, unless the AI-enabled method itself is the object of investigation.

A YES at Q0 says only that the study is on topic. It says nothing about its tier: continue to Q1.

**Q1 — Is the paper primarily a synthesis of other studies?**
(systematic / scoping / narrative / umbrella review, meta-analysis, bibliometric mapping)
→ YES: `design = REVIEW`, `tier = S`. Record the number of included studies. **Stop.**

**Q2 — Does the paper report original empirical data** (from people, documents, logs, or system outputs)?
→ NO: `design = CONCEPTUAL` or `SYSTEM_PROPOSAL`, `tier = 0`. **Stop.**

**Q3 — Is the only empirical data the performance or quality of a system, model or its output?**
(accuracy, agreement with a human/expert standard, output-quality ratings, benchmark scores, latency —
even when computed on real student work)
→ YES: `design = SYSTEM_EVAL`, `tier = 1`. **Stop.**

Ratings of the AI output or system count here, whoever gives them (R11). If the study also reports a person's
state, view or behaviour that is not a rating of the output, the answer is NO: go to Q4.

**Q4 — Is a learning or practice OUTCOME measured?**
Outcome = learners' knowledge/skill/performance, or educators'/institutions' practice quality, measured
**objectively** (tests, rubric-scored work, observed task performance, administrative records).
**Self-reported** learning, workload, satisfaction, acceptance or intention are NOT outcomes (→ perception).
→ NO: `design ∈ {SURVEY_CORRELATIONAL, SURVEY_DESCRIPTIVE, QUALITATIVE, DOCUMENT_ANALYSIS, MIXED}`,
`tier = 2`. **Stop.**

**Q5 — Is the outcome compared against a comparison or control condition?**
(randomised, quasi-experimental with comparison group, crossover, AI vs non-AI condition)
→ YES: `design ∈ {RCT, QUASI_EXPERIMENTAL}`, `tier = 4`.
→ NO: `design ∈ {PRE_POST_SINGLE_GROUP, CORRELATIONAL_OUTCOME}`, `tier = 3`.

## 4. Maturity tiers

| Tier | Label | Can support a claim that… |
|---|---|---|
| 0 | No empirical evidence | the use is conceivable |
| 1 | Technical feasibility | the system can produce acceptable outputs |
| 2 | Perception / descriptive practice | stakeholders accept, use, or describe it |
| 3 | Outcome, no comparison | outcomes co-occur with use |
| 4 | Comparative outcome | outcomes differ between use and a comparison condition; whether the use caused the difference depends on the design |
| S | Secondary synthesis | (reported separately; never pooled into 0–4) |
| NA | Off topic | the study fails Q0; not placed on the tier scale |

**Tiers are an evidential ordering, not a quality ranking.** A well-executed tier-2 interview study can be
better scholarship than a weak tier-4 trial. The tier records what kind of claim the evidence can carry,
nothing more.

Tiers 0–4 are **ordinal**. S and NA are separate categories outside that order.

## 5. Recorded fields (12)

| Field | Values |
|---|---|
| `design` | RCT · QUASI_EXPERIMENTAL · PRE_POST_SINGLE_GROUP · CORRELATIONAL_OUTCOME · SURVEY_CORRELATIONAL · SURVEY_DESCRIPTIVE · QUALITATIVE · DOCUMENT_ANALYSIS · MIXED · SYSTEM_EVAL · SYSTEM_PROPOSAL · CONCEPTUAL · REVIEW · OFF_TOPIC · UNRESOLVED · UNDECIDABLE |
| `comparison` | Y · N · NA |
| `outcome_construct` | none · technical · perception · behaviour · learning_or_practice |
| `outcome_measure` | objective · self_report · NA |
| `setting` | authentic_deployment · lab_or_simulated · offline_data · none |
| `n` | participants (or items/documents/plans for system and document studies), or NR |
| `tier` | 0 · 1 · 2 · 3 · 4 · S · NA · UNDECIDABLE |
| `source` | full_text · full_text_ocr · full_text_replacement (§2.1; pre-filled) |
| `venue_status` | journal · conference · extended_abstract · preprint · self_published · unknown |
| `confidence` | high · medium · low (§2.2) |
| `decisive_question` | Q0 · Q1 · Q2 · Q3 · Q4 · Q5 — which step settled the tier |
| `justification` | the sentence(s) from the study that decided it, quoted or closely paraphrased |

**`decisive_question`** is the step of the decision tree at which coding stopped: `Q0` for `OFF_TOPIC`,
`Q1` for S, `Q2` for tier 0, `Q3` for tier 1, `Q4` for tier 2, `Q5` for tier 3 or 4. Record it **before**
writing `justification`, so that the justification explains a decision already made rather than being
assembled to support one. If `tier = UNDECIDABLE`, record the step that could not be resolved.

**`venue_status`** records the publication status of the version coded. It is pre-filled; override it only if
the document itself shows a different status. It never affects the tier.

## 6. Tie-break rules

| # | Rule |
|---|---|
| **R1** | **Mixed methods:** tier = the highest tier genuinely reached by any strand. |
| **R2** | **Multiple outcomes:** code the strongest *objectively measured* outcome. |
| **R3** | **Human-rated output quality** → tier 1. *(Instance of R11.)* |
| **R4** | **Rubric-scored artifacts produced by participants with vs without AI** → practice outcome, tier 4. |
| **R5** | **Classifier/detector accuracy on learner data** → tier 1. *(Instance of R11.)* |
| **R6** | **Document/policy analysis** → tier 2 (descriptive practice evidence). |
| **R7** | **When the design is unclear from the available text** → code the lower tier and set `confidence = low`. |
| **R8** | **Measurement over label.** Code what was measured and reported, never the authors' word for the design. Record the label/measurement mismatch in `justification`. |
| **R9** | **Unevaluated systems.** A system proposed, built, or even deployed in production for which **no** performance metric, user study or outcome is reported is `design = SYSTEM_PROPOSAL`, **tier 0**. Still record `setting = authentic_deployment` where it is genuinely in use, so that "deployed but never evaluated" is visible as its own finding rather than hidden inside tier 0. |
| **R10** | **Reflexive and autoethnographic work.** A single-author reflexive essay or phenomenological interpretation without systematic data collection is `CONCEPTUAL`, tier 0. Systematic autoethnography with recorded, analysed data is `QUALITATIVE`, tier 2. State in `justification` which applies and why. |
| **R11** | **The object of measurement decides tier 1 vs tier 2.** If what is measured is the **AI artifact or output** — its quality, accuracy, or agreement with an expert standard — it is **tier 1**, *regardless of who does the rating*: students, experts, or an automated metric. If what is measured is a **person's state, view, or behaviour**, it is **tier 2**. Ask "what does the number describe: the output, or the person?" R11 does not override Q3: if a study has both kinds of data, Q3 does not apply and R1 sets the tier. |
| **R12** | **Topic-eligibility gate.** Apply Q0, exactly as defined in §3, to every study. If the answer is NO, code `design = OFF_TOPIC`, `tier = NA`, `decisive_question = Q0`, and state in `justification` what the study actually investigates. |

## 7. Coding hygiene

1. Code the studies in the order given.
2. Read the source document for each study; the minimum reading is set in §2.1.
3. Decide `decisive_question` before writing `justification` (§5).
4. Use no material other than this rubric and the study's own source document when coding.
5. Take a break roughly every 20 studies, and record the coding date for each study.
