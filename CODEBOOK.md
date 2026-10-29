# Codebook: evidence-maturity classification

This document describes how each reviewed study was assigned to an evidence-maturity tier. It is a public summary written for readers of
the data in this package; the full rubric is `RUBRIC_V3_1.md`.

## Unit and source

One row per study. A study was classified from its own full text (at least the abstract, methods and results), never from the abstract alone,
since the design named in an abstract does not always match what was measured. Where only a scan existed, the text was recovered by optical
character recognition, or a verified open-access copy of the same study was used; confidence was capped at "medium" for such sources unless
the design and outcome were stated plainly.

## Decision sequence

Each study was passed through the questions below in order; the first question answered "yes" (or the last, for Q5) settled the tier.

| Step | Question | Result |
|---|---|---|
| Topic eligibility | Does the study substantively investigate, evaluate, design, deploy or analyse an LLM, a generative-AI system, or another AI-enabled system in which the AI component is a material part of what is being taught, tried, supported, decided or measured? Studies that merely mention AI as background, list it as a possible method, use conventional statistics, databases or business-intelligence tools, or use machine learning only as an analysis tool on a non-AI educational subject do not qualify. | If no: off topic, not placed on the tier scale |
| Q1 | Is the paper mainly a synthesis of other studies (systematic, scoping or narrative review, meta-analysis, bibliometric mapping)? | Tier **S**, reported separately from tiers 0–4 |
| Q2 | Does it report original empirical data (from people, documents, logs or system outputs)? | If no (conceptual work or an unevaluated system proposal): **Tier 0** |
| Q3 | Does the empirical evidence consist solely of how well a system, a model or its output performs (accuracy, agreement with a standard, quality ratings, benchmarks)? | If yes: **Tier 1** |
| Q4 | Is a learning or practice *outcome* measured objectively (tests, scored work, observed performance, administrative records)? Self-reported learning, satisfaction, acceptance or intention are not outcomes. | If no (surveys, interviews, document analysis, descriptive practice): **Tier 2** |
| Q5 | Is the outcome compared with a comparison or control condition (randomised, quasi-experimental, crossover, AI versus non-AI)? | If yes: **Tier 4**; if no: **Tier 3** |

## Tiers

| Tier | Label | What the evidence can support |
|---|---|---|
| 0 | No empirical evidence | only that the use is plausible |
| 1 | Technical feasibility | that the technology works well enough in the tested setting |
| 2 | Perception / descriptive practice | that people report using it, accepting it or how they practise with it |
| 3 | Outcome without comparison | that outcomes were observed alongside use |
| 4 | Comparative outcome | that outcomes differ between use and a comparison condition; whether the use caused the difference depends on the design |
| S | Secondary synthesis | reported separately; never pooled into tiers 0–4 |

Tiers 0–4 are ordinal. **They are an evidential ordering, not a quality ranking**: a careful interview study can be better scholarship than a
weak trial. S and the off-topic category sit outside the ordering.

## Design labels and the tier each implies

`data/study_classifications.csv` carries a design label for each study. Under the decision sequence the label fixes the tier, which
`scripts/reproduce_all.py` checks for all 120 studies.

| Design label | Meaning | Tier |
|---|---|---|
| `REVIEW` | Synthesis of other studies | S |
| `CONCEPTUAL`, `SYSTEM_PROPOSAL` | No original data: argument, framework, or an unevaluated system | 0 |
| `SYSTEM_EVAL` | Only the quality or performance of a system or its output is evaluated | 1 |
| `SURVEY_DESCRIPTIVE`, `SURVEY_CORRELATIONAL`, `QUALITATIVE`, `DOCUMENT_ANALYSIS`, `MIXED` | Perceptions, practices or documents; no objectively measured outcome | 2 |
| `PRE_POST_SINGLE_GROUP`, `CORRELATIONAL_OUTCOME` | Objective outcome measured, no comparison condition | 3 |
| `QUASI_EXPERIMENTAL`, `RCT` | Objective outcome compared with a comparison or control condition | 4 |

## Interpretive rules applied where the sequence is not enough

* Code what was measured, not the authors' name for the design.
* Mixed methods: the highest tier genuinely reached by any strand; several outcomes: the strongest objectively measured one.
* What is measured decides Tier 1 versus Tier 2: if it is the AI artefact or its output (whoever rates it), Tier 1; if it is a person's state,
  view or behaviour, Tier 2. Classifier or detector accuracy on learner data is Tier 1.
* A tool that is described, built or even running in practice but never evaluated is Tier 0.
* Document or policy analysis is Tier 2. Single-author reflexive essays without systematic data are Tier 0.
* Work scored on artefacts produced with and without AI is a practice outcome with a comparison (Tier 4).
* If the design cannot be determined from the text, assign the lower tier and record low confidence.

## Domains and subcategories used in the paper

The corpus manifest used four categories. The paper reports five domains: **D1** Lifelong & Informal Learning, **D2** Learner Support in
Formal Education, **D3** Instructional Support, **D4** Institutional Intelligence & Operations, **D5** Accessibility & Special Education.
`corpus_records.csv` keeps the manifest category and subcategory beside the review domain and subcategory. The mapping is: manifest categories
01, 02 and 04 become D1, D2 and D5; category 03 (Educational Leadership & Management) splits into D3 (assessment and feedback, content creation,
and the manifest's instructional-support records, plus two educator-facing records from its workflow-automation subcategory) and D4 (the
rest). The D4 split between *Academic & Administrative Operations* and *AI Governance & Institutional Policy* follows an explicit list of nine
record numbers, given in `scripts/reproduce_all.py`. Domain 4 records not on that list, including those set aside at corpus construction, are Operations by default (see the README).
After peer review, 14 studies were reclassified by applying the written domain definitions to the source texts, following a second-coder
check of a stratified sample and a source check of the outcome studies; `data/domain_reclassification.csv` lists them, and
`scripts/reproduce_all.py` applies that list after the mapping above.

## What was recorded but is not released

The coding also recorded the comparison and outcome fields, setting, sample size, confidence, the deciding question, and a short free-text
justification quoting the study. Only the tier, domain, subcategory and design label are released (see `DATA_DICTIONARY.md` and
`DATA_AVAILABILITY.md`).
