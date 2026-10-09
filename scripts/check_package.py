"""Package integrity and hygiene checks. Standard library only. Run from the package root:  python scripts/check_package.py

  1. Every file listed in SHA256SUMS.txt exists and matches its checksum, and no file is missing from the list.
  2. No absolute or machine-specific paths in any text file.
  3. No internal study identifiers (F/V/P-numbered), e-mail addresses or tool/vendor identifiers in any text file.
  4. No CSV column that would carry study-level coder output (justifications, raw codes, coder labels).
"""
import csv
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_EXT = {".md", ".txt", ".csv", ".json", ".py", ".tex"}
ABS_PATH = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]|\\\\[A-Za-z0-9_.-]+\\|/Users/|/home/[a-z]|/mnt/[a-z]/")
INTERNAL_ID = re.compile(r"\b[FVP]\d{2,3}\b")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
TERMS = re.compile("|".join(["clau" + "de", "anthro" + "pic", "gem" + "ini", "sub-?agent", "super" + "visor", "sea" + "led", "pre-?regist",
                             "passw" + "ord", "api[_ -]?key", "secret"]), re.I)
FORBIDDEN_COLUMNS = {"justification", "raw_file", "raw_sha256", "original_code", "coded_by", "coder", "coder1", "coder2", "coder_initials", "vid"}
rows = []


def check(name, ok, detail=""):
    rows.append((name, "PASS" if ok else "FAIL", detail))


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    files = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in ("__pycache__", ".git")]
        files += [os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/") for f in fn if f not in ("SHA256SUMS.txt", ".gitattributes") and not f.endswith(".pyc")]
    listed = {}
    for line in open(os.path.join(ROOT, "SHA256SUMS.txt"), encoding="utf-8"):
        h, _, p = line.rstrip("\n").partition("  ")
        listed[p] = h
    bad = [p for p, h in listed.items() if not os.path.exists(os.path.join(ROOT, p)) or sha256(os.path.join(ROOT, p)) != h]
    check("every file in SHA256SUMS.txt exists and matches its checksum", not bad, str(bad[:5]))
    check("no file exists that is missing from SHA256SUMS.txt", sorted(files) == sorted(listed), str(sorted(set(files) ^ set(listed))[:5]))
    abs_hits, ids, terms, cols = [], [], [], []
    for rel in files:
        if os.path.splitext(rel)[1].lower() not in TEXT_EXT or rel == "scripts/check_package.py":
            continue
        text = open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace").read()
        if ABS_PATH.search(text):
            abs_hits.append(rel)
        ids += [f"{rel}: {m.group(0)}" for m in INTERNAL_ID.finditer(text)]
        terms += [f"{rel}: {m.group(0)}" for m in list(TERMS.finditer(text)) + list(EMAIL.finditer(text))]
        if rel.endswith(".csv"):
            data = list(csv.DictReader(io.StringIO(text)))
            for c in (data[0].keys() if data else []):
                if c.strip().lower() in FORBIDDEN_COLUMNS:
                    cols.append(f"{rel}: {c}")
    check("no absolute or machine-specific paths", not abs_hits, str(abs_hits))
    check("no internal study identifiers", not ids, str(ids[:5]))
    check("no e-mail addresses, tool/vendor names, internal role names or credential words", not terms, str(terms[:5]))
    check("no study-level coder-output columns in any CSV", not cols, str(cols))
    for name, status, detail in rows:
        print(f"[{status}] {name}" + (f" -- {detail}" if detail else ""))
    n = sum(1 for r in rows if r[1] == "FAIL")
    print(f"\nsummary: {len(rows) - n} passed, {n} failed")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
