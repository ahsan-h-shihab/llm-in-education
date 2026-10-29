"""Recompute the reported results from the released data and compare them with the values reported in the paper.

Standard library only. Run from the package root:   python scripts/reproduce_all.py

Sections
  1. Domain / subcategory layer re-derived from the corpus manifest categories plus the post-review reclassification list
     (data/domain_reclassification.csv, 14 studies).
  2. Record-count chain, tier counts and the two summary tables, recomputed from data/ and compared with results/reported_results.json.
  3. The reported sampling design (the draw itself cannot be replayed: its inputs are not released).
  4. Aggregate agreement statistics, recomputed from the released aggregate agreement table (NOT from study-level codes, which are withheld).
Each check prints PASS, FAIL or NOT TESTABLE. Exit status 1 if any check FAILED.
"""
import csv
import json
import math
import os
import random
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASS, FAIL, NT = "PASS", "FAIL", "NOT TESTABLE"
ROWS = []


def read_csv(rel):
    with open(os.path.join(ROOT, *rel.split("/")), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_json(rel):
    with open(os.path.join(ROOT, *rel.split("/")), encoding="utf-8") as f:
        return json.load(f)


def check(name, ok, detail=""):
    ROWS.append((name, PASS if ok else FAIL, detail))
    return ok


def not_testable(name, detail):
    ROWS.append((name, NT, detail))


DOMAIN_NAME = {"D1": "Lifelong & Informal Learning", "D2": "Learner Support in Formal Education", "D3": "Instructional Support",
               "D4": "Institutional Intelligence & Operations", "D5": "Accessibility & Special Education"}
OPS, GOVN = "Academic & Administrative Operations", "AI Governance & Institutional Policy"
GOVERNANCE_RECORDS = {"31", "39", "50", "77", "78", "80", "81", "82", "83"}   # explicit list used by the review (see CODEBOOK.md)
TIERS = ["T0", "T1", "T2", "T3", "T4", "S"]
DESIGN_TIER = {"REVIEW": "S", "CONCEPTUAL": "0", "SYSTEM_PROPOSAL": "0", "SYSTEM_EVAL": "1", "SURVEY_CORRELATIONAL": "2", "SURVEY_DESCRIPTIVE": "2",
               "QUALITATIVE": "2", "DOCUMENT_ANALYSIS": "2", "MIXED": "2", "PRE_POST_SINGLE_GROUP": "3", "CORRELATIONAL_OUTCOME": "3",
               "QUASI_EXPERIMENTAL": "4", "RCT": "4"}     # CODEBOOK.md: the tier each design label implies under the decision sequence


def domain_of(rid, category, subcategory):
    if rid in ("45", "55"):     # two records of the manifest's workflow-automation subcategory that are educator-facing
        return "D3"
    d = {"01": "D1", "02": "D2", "04": "D5"}.get(category[:2])
    if d:
        return d
    return "D3" if subcategory in ("Instructional Support", "Content Creation", "Assessment & Feedback") else "D4"


def layer(rid, category, subcategory):
    d = domain_of(rid, category, subcategory)
    if rid == "45":
        return d, "Teaching Practice & Rehearsal"
    if rid == "55":
        return d, "Content Creation"
    if d == "D3":
        return d, {"Instructional Support": "Teaching Practice & Rehearsal"}.get(subcategory, subcategory)
    if d == "D4":
        return d, GOVN if rid in GOVERNANCE_RECORDS else OPS
    return d, subcategory


RECLASS = {r["record_id"]: r for r in read_csv("data/domain_reclassification.csv")}


def final_layer(rid, category, subcategory):
    """Manifest-derived layer, then the explicit post-review reclassification list."""
    d, s = layer(rid, category, subcategory)
    if rid in RECLASS:
        x = RECLASS[rid]
        assert (d, s) == (x["original_domain"], x["original_subcategory"]), rid
        return x["revised_domain"], x["revised_subcategory"]
    return d, s


def tier_counts(rows):
    c = Counter(("S" if r["evidence_tier"] == "S" else "T" + r["evidence_tier"]) for r in rows)
    out = {k: c.get(k, 0) for k in TIERS}
    out["N"] = len(rows)
    out["Outcome"] = out["T3"] + out["T4"]
    return out


# ------------------------------------------------------------------------------------------------ 1 + 2
def section_counts():
    recs, cls = read_csv("data/corpus_records.csv"), read_csv("data/study_classifications.csv")
    meta, R = read_csv("data/study_metadata.csv"), read_json("results/reported_results.json")

    bad_dom = bad_sub = 0
    for r in recs:
        d, s_ = final_layer(r["record_id"], r["manifest_category"], r["manifest_subcategory"])
        bad_dom += d != r["review_domain"]
        bad_sub += s_ != r["review_subcategory"]
    check("1. domain re-derived from manifest categories and the reclassification list for all 150 records", bad_dom == 0, f"{bad_dom} mismatches")
    check("1. subcategory re-derived from the manifest, the explicit Governance list and the reclassification list for all 150 records", bad_sub == 0, f"{bad_sub} mismatches")
    check("1. reclassification list: 14 synthesized records, each with its manifest-derived original label",
          len(RECLASS) == 14 and all(any(r["record_id"] == k and r["status"] == "synthesized" for r in recs) for k in RECLASS))
    gov_ids = {r["record_id"] for r in recs if r["review_subcategory"] == GOVN}
    check("1. the Governance subcategory is exactly the nine records on the explicit list", gov_ids == GOVERNANCE_RECORDS, str(sorted(gov_ids)))

    # accounting chain
    st = Counter(r["status"] for r in recs)
    A = R["accounting_chain"]
    dup = st["synthesized_duplicate_record"]
    check("2. 150 records", len(recs) == A["records"] == 150)
    check("2. 149 unique studies (150 records, one record repeats another)", len(recs) - dup == A["unique_studies_in_corpus"] == 149)
    check("2. 121 synthesized records", st["synthesized"] + dup == A["synthesized_records"] == 121, str(dict(st)))
    check("2. 120 synthesized unique studies", len({r["study_id"] for r in cls}) == len(cls) == A["synthesized_unique_studies"] == 120)
    check("2. 29 records not synthesized = 18 set aside at corpus construction + 2 corpus integrity + 9 topic eligibility",
          len(recs) - st["synthesized"] - dup == A["records_not_synthesized"] == 29 and
          (st["set_aside_at_corpus_construction"], st["excluded_corpus_integrity"], st["excluded_topic_eligibility"]) == (18, 2, 9))
    q0 = Counter(r["exclusion_category"] for r in recs if r["status"] == "excluded_topic_eligibility")
    check("2. topic-eligibility exclusions: 3 no AI-enabled system + 6 AI outside education",
          (q0["topic eligibility: no AI-enabled system"], q0["topic eligibility: AI outside education"]) == (3, 6), str(dict(q0)))
    eb = Counter(r["exclusion_basis"] for r in recs if r["status"] not in ("synthesized",))
    check("2. basis of the 30 non-synthesized-or-duplicate records: 15 post-hoc reconstruction, 3 verifiable file property, 9 classification-time, 2 authors' decision, 1 verified duplicate",
          sorted(eb.values()) == [1, 2, 3, 9, 15] and eb["post-hoc reconstruction; not a contemporaneous screening record"] == 15, str(dict(eb)))
    base = [r for r in recs if r["status"] == "synthesized_duplicate_record"][0]
    orig = [r for r in recs if r["record_id"] == base["duplicate_of"]][0]
    check("2. the duplicate record shares the study_id of the record it repeats", base["study_id"] == orig["study_id"], f"record {base['record_id']} repeats {orig['record_id']}")
    check("2. every classified study matches exactly one 'synthesized' record",
          sorted(r["study_id"] for r in recs if r["status"] == "synthesized") == sorted(r["study_id"] for r in cls))
    check("2. study_metadata.csv covers the 120 studies", {m["study_id"] for m in meta if m["study_id"]} >= {r["study_id"] for r in cls})

    # tiers and headline statements
    T = tier_counts(cls)
    prim = sum(T[k] for k in TIERS[:5])
    check("2. 86 primary studies + 34 secondary syntheses", (prim, T["S"]) == (A["primary_studies"], A["secondary_syntheses"]) == (86, 34))
    check("2. tier distribution", {k: T[k] for k in TIERS} == R["tiers_all_studies"], str({k: T[k] for k in TIERS}))
    check("2. every study's tier is the tier implied by its design label (CODEBOOK.md), for all 120 studies",
          all(DESIGN_TIER.get(r["design"]) == r["evidence_tier"] for r in cls), str(Counter((r["design"], r["evidence_tier"]) for r in cls if DESIGN_TIER.get(r["design"]) != r["evidence_tier"])))
    H = R["headline"]
    check("2. outcome evidence (T3+T4) = 25 of 86; comparative (T4) = 20 of 86",
          (T["Outcome"], T["T4"], prim) == (H["outcome_T3_or_T4"], H["comparative_T4"], H["primary_studies"]))
    pct = lambda n: round(100 * n / prim, 1)
    sh = H["share_of_primary"]
    check("2. percentage shares of the primary studies",
          (pct(T["T2"]), pct(T["T1"]), pct(T["T4"]), pct(T["T0"]), pct(T["T3"]), pct(T["Outcome"])) ==
          (sh["T2"], sh["T1"], sh["T4"], sh["T0"], sh["T3"], sh["outcome_T3_T4"]))
    byd, sub = defaultdict(list), defaultdict(list)
    for r in cls:
        byd[r["review_domain"]].append(r)
        sub[(r["review_domain"], r["review_subcategory"])].append(r)
    D = {d: tier_counts(byd[d]) for d in DOMAIN_NAME}
    check("2. D1 2 of 9; D2 13 of 24 primary studies with outcome evidence",
          (D["D1"]["Outcome"], D["D1"]["N"] - D["D1"]["S"], D["D2"]["Outcome"], D["D2"]["N"] - D["D2"]["S"]) == (2, 9, 13, 24))
    af = tier_counts(sub[("D3", "Assessment & Feedback")])
    check("2. D3: 8 comparative studies, 1 T3; 6 of the comparative studies in Assessment & Feedback", (D["D3"]["T4"], D["D3"]["T3"], af["T4"]) == (8, 1, 6))
    check("2. D4: 0 of 20 (T2 11, T1 5, T0 4)", (D["D4"]["Outcome"], D["D4"]["N"] - D["D4"]["S"], D["D4"]["T2"], D["D4"]["T1"], D["D4"]["T0"]) == (0, 20, 11, 5, 4))
    check("2. D5: 1 of 7 primary studies; 9 of 16 are secondary syntheses", (D["D5"]["Outcome"], D["D5"]["N"] - D["D5"]["S"], D["D5"]["S"], D["D5"]["N"]) == (1, 7, 9, 16))
    gaps = sorted(s for (d, s), rows in sub.items() if tier_counts(rows)["Outcome"] == 0)
    check("2. six subcategories without outcome evidence", gaps == sorted(R["subcategories_without_outcome_evidence"]), str(gaps))

    # Table 2
    bad = []
    for d, name in DOMAIN_NAME.items():
        for s, row in R["table2_evidence_maturity"][name].items():
            calc = D[d] if s == "TOTAL" else tier_counts(sub[(d, s)])
            if calc != {k: row[k] for k in TIERS + ["N", "Outcome"]}:
                bad.append((d, s))
    check("2. evidence-maturity table: 14 subcategory rows and 5 domain totals", not bad, str(bad) if bad else "19 rows compared")
    check("2. evidence-maturity table: all-domains row", T == {k: R["table2_evidence_maturity"]["ALL"][k] for k in TIERS + ["N", "Outcome"]})

    # Table 1
    t1, bad1 = R["table1_corpus_structure"]["domains"], []
    for d, name in DOMAIN_NAME.items():
        drec = [r for r in recs if r["review_domain"] == d]
        syn = sum(1 for r in drec if r["status"] in ("synthesized", "synthesized_duplicate_record"))
        if (len(drec), syn) != (t1[name]["records"], t1[name]["synthesized"]):
            bad1.append((d, len(drec), syn))
    check("2. corpus-structure table: records and records synthesized per domain (13/12, 35/35, 33/31, 47/27, 22/16)", not bad1, str(bad1))
    for d in ("D1", "D2", "D3", "D5"):
        c = Counter(r["review_subcategory"] for r in recs if r["review_domain"] == d)
        check(f"2. corpus-structure table: records per subcategory, {d}", dict(c) == t1[DOMAIN_NAME[d]]["records_by_subcategory"], str(dict(c)))
    d4 = [r for r in recs if r["review_domain"] == "D4"]
    c4 = Counter(r["review_subcategory"] for r in d4)
    rep = t1[DOMAIN_NAME["D4"]]["records_by_subcategory"]
    check("2. Domain 4, all 47 records: Operations / Governance equals the reported 38 / 9", (c4[OPS], c4[GOVN]) == (rep[OPS], rep[GOVN]) == (38, 9), str(dict(c4)))
    sy = Counter(r["review_subcategory"] for r in d4 if r["status"] in ("synthesized", "excluded_topic_eligibility", "excluded_corpus_integrity"))
    check("2. Domain 4 records synthesized before the topic-eligibility and integrity exclusions (31 records): 22 Operations / 9 Governance", (sy[OPS], sy[GOVN]) == (22, 9), str(dict(sy)))
    sa = [r for r in d4 if r["status"] == "set_aside_at_corpus_construction"]
    check("2. Domain 4 records set aside at corpus construction (16 records) are Operations by the default rule", len(sa) == 16 and all(r["review_subcategory"] == OPS for r in sa))
    uq = Counter(r["review_subcategory"] for r in cls if r["review_domain"] == "D4")
    check("2. Domain 4 unique final studies (27 studies, not records): 20 Operations / 7 Governance", (uq[OPS], uq[GOVN]) == (20, 7), str(dict(uq)))


# ------------------------------------------------------------------------------------------------ 3
def section_sampling():
    A = read_json("validation/aggregate_results.json")["sampling"]
    check("3. reported sampling design is internally consistent: 30 studies = 6 per domain from a frame of 99 (18/23/22/21/15)",
          A["stratified_random_sample_size"] == 6 * 5 == 30 and A["per_domain"] == 6 and sum(A["frame_by_domain"].values()) == A["frame_size"] == 99)
    not_testable("3. the validation sample draw", "the sampling frame, seed and sample list are not released (not needed to reproduce a reported number); the draw cannot be replayed")


# ------------------------------------------------------------------------------------------------ 4
def weighted_kappa(a, b, k=5):
    O = [[0.0] * k for _ in range(k)]
    for x, y in zip(a, b):
        O[x][y] += 1
    n = sum(map(sum, O))
    if n == 0:
        return float("nan")
    rows, cols = [sum(r) for r in O], [sum(O[i][j] for i in range(k)) for j in range(k)]
    W = [[abs(i - j) / (k - 1) for j in range(k)] for i in range(k)]
    de = sum(W[i][j] * rows[i] * cols[j] / n for i in range(k) for j in range(k))
    num = sum(W[i][j] * O[i][j] for i in range(k) for j in range(k))
    return float("nan") if de == 0 else 1 - num / de


def alpha_ordinal(a, b, k=5):
    o = [[0.0] * k for _ in range(k)]
    for x, y in zip(a, b):
        o[x][y] += 1
        o[y][x] += 1
    nc = [sum(r) for r in o]
    N = sum(nc)

    def delta2(c, g):
        lo, hi = min(c, g), max(c, g)
        return (sum(nc[lo:hi + 1]) - (nc[c] + nc[g]) / 2) ** 2

    do = sum(o[c][g] * delta2(c, g) for c in range(k) for g in range(k))
    de = sum(nc[c] * nc[g] * delta2(c, g) for c in range(k) for g in range(k)) / (N - 1)
    return float("nan") if de == 0 else 1 - do / de


def percentile(vals, q):
    s = sorted(vals)
    pos = (len(s) - 1) * q / 100
    lo = int(math.floor(pos))
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def section_aggregate():
    A = read_json("validation/aggregate_results.json")
    P = A["primary"]
    tab = P["table_5x5"]
    ta, tb = [], []
    for i in range(5):
        for j in range(5):
            ta += [i] * tab[str(i)][str(j)]
            tb += [j] * tab[str(i)][str(j)]
    check("4. the aggregate agreement table holds 22 pairs", len(ta) == P["n_studies"] == 22)
    check("4. the table is diagonal: all 22 pairs agree", all(x == y for x, y in zip(ta, tb)))
    k = weighted_kappa(ta, tb)
    check("4. linear-weighted kappa on tiers 0-4 equals the reported value", math.isclose(k, P["linear_weighted_kappa"]), f"{k:.4f}")
    check("4. Krippendorff's ordinal alpha equals the reported value", math.isclose(alpha_ordinal(ta, tb), P["krippendorff_alpha_ordinal"]))
    check("4. raw exact agreement equals the reported value", sum(x == y for x, y in zip(ta, tb)) / len(ta) == P["raw_exact_agreement"])
    rng, boots, undefined = random.Random(P["bootstrap_seed"]), [], 0
    for _ in range(P["bootstrap_resamples"]):
        ii = [rng.randrange(len(ta)) for _ in ta]
        kb = weighted_kappa([ta[i] for i in ii], [tb[i] for i in ii])
        undefined += math.isnan(kb)
        if not math.isnan(kb):
            boots.append(kb)
    ci = [percentile(boots, 2.5), percentile(boots, 97.5)]
    check("4. percentile bootstrap interval and number of undefined resamples equal the reported values (degenerate [1, 1])",
          ci == P["bootstrap_95ci"] and undefined == P["bootstrap_undefined_resamples"], f"{ci}, {undefined} undefined")
    q = A["secondary_derived_outcome_table"]
    da = ["T3/T4" if x >= 3 else "T0-T2" for x in ta]
    check("4. derived outcome table (T3/T4 vs T0-T2) equals the reported counts",
          (da.count("T3/T4"), da.count("T0-T2")) == (q["both_T3_T4"], q["both_T0_T2"]) and q["disagree"] == 0)
    not_testable("4. recomputation from the two coders' study-level data", "study-level codes are withheld; the values above are reproduced from the aggregate table only, "
                 "which is diagonal, so they do not depend on study order and cannot reveal sensitivity to any disagreement")
    not_testable("4. field-level, topic-eligibility and decision-question agreement tables", "need study-level codes; the aggregate values are reported as supplied")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    section_counts()
    section_sampling()
    section_aggregate()
    for name, status, detail in ROWS:
        print(f"[{status}] {name}" + (f" -- {detail}" if detail else ""))
    n = Counter(s for _, s, _ in ROWS)
    print(f"\nsummary: {n[PASS]} passed, {n[FAIL]} failed, {n[NT]} not testable")
    return 1 if n[FAIL] else 0


if __name__ == "__main__":
    sys.exit(main())
