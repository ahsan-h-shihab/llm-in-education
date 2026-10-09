# Data dictionary

Domains: **D1** Lifelong & Informal Learning · **D2** Learner Support in Formal Education · **D3** Instructional Support ·
**D4** Institutional Intelligence & Operations · **D5** Accessibility & Special Education. Tiers are defined in `CODEBOOK.md`.
All files are UTF-8 CSV with a header row, unless noted.

## data/corpus_records.csv (150 rows, one per corpus record)

| Column | Meaning |
|---|---|
| `record_id` | Record number from the corpus numbering (text: some are `1.1-145` or `1.2`); unique |
| `manifest_category`, `manifest_subcategory` | The four-category scheme of the original corpus manifest |
| `review_domain` | D1–D5, derived from the manifest category (`CODEBOOK.md`) |
| `review_subcategory` | Subcategory within the review domain. For Domain 4, the nine records on the taxonomy's explicit Governance list are Governance and every other record is Operations by default, including the 16 set aside at corpus construction |
| `status` | `synthesized` (120) · `synthesized_duplicate_record` (1, a second record of an article already counted) · `excluded_topic_eligibility` (9) · `excluded_corpus_integrity` (2) · `set_aside_at_corpus_construction` (18) |
| `study_id` | Public study identifier `S001`–`S120` (assigned in corpus order; shared by the two records of the duplicated article); empty for records without a classification |
| `duplicate_of` | `record_id` of the record that the duplicate repeats |
| `exclusion_category` | Category-level reason for any record not classified or counted separately |
| `exclusion_basis` | Where the reason comes from: *post-hoc reconstruction; not a contemporaneous screening record* (the 15 general-purpose set-asides), *verifiable file property* (3 unreadable), *decision recorded at classification (topic-eligibility question)* (9), *decision recorded by the authors* (2), *verified: same article…* (the duplicate) |

## data/study_classifications.csv (120 rows, one per synthesized study)

| Column | Meaning |
|---|---|
| `study_id`, `record_id` | Identifiers as above |
| `review_domain`, `review_subcategory` | Domain and subcategory used in the paper |
| `evidence_tier` | `0`, `1`, `2`, `3`, `4` or `S` (secondary synthesis): the **final classification**. For the validation sample it is the tier on which the initial classification and the independent human coding agreed. It is not a coder-specific score |
| `design` | Design label (see `CODEBOOK.md`); determines the tier. Not separately validated apart from the tier |

The other recorded fields (comparison, outcome construct and measure, setting, sample size, confidence, deciding question) and the free-text
justification are not released.

## data/study_metadata.csv (120 rows)

`study_id`, `record_id`, `title`, `year`, `venue`, `doi` (empty where the source bibliography has none; three studies).

## validation/aggregate_results.json

Aggregate statistics only: the reported sampling design (sizes only), and for the 22 studies on the 0–4 scale in the validation sample: linear-weighted
κ, Krippendorff's ordinal α, raw agreement, the bootstrap interval (10,000 resamples, seed 20261004), and the 5 × 5 agreement table; the derived
outcome table (Tier 3/4 versus Tiers 0–2); agreement on secondary-synthesis status and on topic eligibility for all 30 studies; agreement on the
deciding question and the field-level raw agreement.

## results/reported_results.json

The numbers as stated in the paper: the record-count chain, tier counts, headline shares, and the two summary tables (corpus structure and
evidence maturity by domain and subcategory). Used by `scripts/reproduce_all.py` as expected values.

## figures/

`evidence_maturity_by_domain.tex` (standalone TikZ source) and `.png` (rendered from the `.tex`).

## Provenance

Every file was written for this package from the project's private working records; none is a copy of an internal document. `corpus_records.csv`
follows from the corpus manifest, the final classification table and the recorded exclusion decisions; `study_classifications.csv` keeps only domain,
subcategory, tier and design label (each equals the private final value, checked cell by cell; study ids were reassigned); `study_metadata.csv` comes from
the verified bibliography (title, year, venue, DOI only); `aggregate_results.json` keeps aggregate values of the reliability output only; `reported_results.json`
was parsed from the paper's two summary tables and headline statements (numbers only); the figure source is the project's figure script output, which
`scripts/make_figure.py` regenerates byte for byte. The private records themselves are preserved by the authors and are not released.
