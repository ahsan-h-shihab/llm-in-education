# Data and materials availability

## Statement for the paper

*Data and materials availability.* The evidence-classification rubric, supporting research materials, and reproducibility package for this review are available at https://github.com/ahsan-h-shihab/llm-in-education.
The repository contains the rubric, the final evidence-maturity classification (domain, subcategory, tier and design label) of the 120 synthesized studies,
the corpus record table with each record's synthesis status, bibliographic identifiers of the reviewed studies, aggregate agreement statistics, a public codebook, and scripts that recompute the reported
counts and tables and regenerate the evidence-maturity figure. The reviewed papers are not redistributed; each is identified by its title and DOI and remains subject to its publisher's
terms. The coders' study-level records, including their free-text justifications, the full texts and the working materials are not publicly
released. The original lodged ratings had 22/22 exact matches. The corrected operative validation has 21/22 exact matches (95.45%) after the human coder confirmed the intended tier. The public aggregate confusion matrix supports independent recalculation of the point estimates (exact agreement, linear-weighted kappa and ordinal alpha). Exact reproduction of the original seeded bootstrap interval requires the original sample order, which is not publicly available. The procedure by which the 150-record corpus was assembled was not recorded and cannot be reproduced.

## What is and is not released

| Material | Released | Note |
|---|---|---|
| Final classification of the 120 studies (domain, subcategory, tier, design label) | Yes | `data/study_classifications.csv` |
| Corpus record table with status and exclusion category (no titles of non-synthesized records) | Yes | `data/corpus_records.csv` |
| Title, year, venue and DOI of the 120 studies | Yes | `data/study_metadata.csv` |
| Validation sampling frame, seed, sample list | No | Not needed to reproduce a reported number |
| Aggregate agreement statistics | Yes | `validation/aggregate_results.json` |
| Evidence-classification rubric | Yes | `RUBRIC_V3_1.md` |
| Public codebook | Yes | `CODEBOOK.md`; a summary of the method |
| Evidence-maturity figure and source | Yes | `figures/` |
| Other recorded fields (comparison, outcome construct and measure, setting, sample size, confidence, deciding question) | No | Not needed to reproduce the reported results; some were not validated |
| Free-text justifications, source quotations | No | Third-party text and per-study reasoning |
| Initial classification and human coder ratings at study level | No | Withheld so that the validation remains interpretable as a comparison; only aggregates are released |
| Adjudication records, coding bundles, prompts, logs, working notes | No | Internal process material |
| Reviewed papers and text derived from them | No | Third-party copyright |
| The paper's manuscript source and bibliography | No | Unpublished manuscript |

Nothing in this package implies that the reviewed papers or the coders' records are openly available.
