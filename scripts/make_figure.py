"""Regenerate the evidence-maturity figure from data/study_classifications.csv and compare it with the released figure source.

Standard library only. Run from the package root:   python scripts/make_figure.py [--compile] [output_dir]
Writes the TikZ sources to output_dir (default: a temporary directory), never into the package. With --compile it also runs pdflatex
(needs tikz, standalone and newtx). Checks: the regenerated standalone source is byte-identical to figures/evidence_maturity_by_domain.tex.
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
import csv, sys, tempfile
from collections import Counter
_rows = list(csv.DictReader(open(os.path.join(OUT, "data", "study_classifications.csv"), encoding="utf-8", newline="")))
N = {"ALL|ALL": dict(Counter(r["evidence_tier"] for r in _rows))}
for _d in ("D1", "D2", "D3", "D4", "D5"):
    N[_d + "|ALL"] = dict(Counter(r["evidence_tier"] for r in _rows if r["review_domain"] == _d))
DOM = [("D1", "Lifelong \\& Informal\\\\Learning", "orange"), ("D2", "Learner Support in\\\\Formal Education", "blue"),
       ("D3", "Instructional\\\\Support", "green"), ("D4", "Institutional Intelligence\\\\\\& Operations", "purple"),
       ("D5", "Accessibility \\&\\\\Special Education", "teal")]
TIERS = ["0", "1", "2", "3", "4"]
TIERNAME = ["no empirical evidence", "technical feasibility", "perception / descriptive", "outcome, no comparison",
            "comparative outcome"]
TEXTCOL = ["black", "black", "white", "white", "white"]    # legible on ramp steps 250, 350, 450, 550, 650
U = 0.21               # cm per study
X0, ROW = 3.75, 0.95   # bar origin x; row pitch
BOXX, BOXW = 1.65, 3.3
GAP = 0.025            # ~0.7 pt surface gap between stacked segments
XR = X0 + 25 * U + 0.15
COLS = {"out": XR + 0.75, "s": XR + 2.0, "tot": XR + 3.05}
body = []
a = body.append
a(r"\begin{tikzpicture}[x=1cm,y=1cm,font=\footnotesize]")
# legend: each item placed from the previous item's real width
prev = None
for i, t in enumerate(TIERS):
    # two legend rows (Tiers 0-2, Tiers 3-4) so the figure fits the IEEE text width
    pos = ("at (0,0.98)" if prev is None else "at (0,0.62)" if t == "3" else f"at ([xshift=9pt]{prev}.east)")
    a(rf"\node[anchor=west, inner sep=0pt, minimum width=8pt, minimum height=6pt, fill=tier{t}, rounded corners=0.6pt] (sw{t}) {pos} {{}};")
    a(rf"\node[anchor=west, inner sep=1pt] (lg{t}) at ([xshift=2pt]sw{t}.east) {{\footnotesize Tier {t}: {TIERNAME[i]}}};")   # 8 pt for print legibility
    prev = f"lg{t}"
top = -0.15
a(rf"\node[anchor=south west, inner sep=1pt, text=inkmuted] at ({X0:.2f},{top:.2f}) {{\scriptsize Primary studies (Tiers 0--4)}};")
a(rf"\node[anchor=south, inner sep=1pt, text=inkmuted, align=center] at ({COLS['out']:.2f},{top:.2f}) {{\scriptsize Outcome\\[-2pt]\scriptsize (T3+T4)}};")
a(rf"\node[anchor=south, inner sep=1pt, text=inkmuted, align=center] at ({COLS['s']:.2f},{top:.2f}) {{\scriptsize Secondary\\[-2pt]\scriptsize syntheses}};")
a(rf"\node[anchor=south, inner sep=1pt, text=inkmuted] at ({COLS['tot']:.2f},{top:.2f}) {{\scriptsize Total}};")
ybot = -0.6 - ROW * 4 - 0.42
for v in range(0, 26, 5):
    x = X0 + v * U
    a(rf"\draw[gridcol, line width=0.3pt] ({x:.2f},{top - 0.05:.2f}) -- ({x:.2f},{ybot:.2f});")
    a(rf"\node[anchor=north, text=inkmuted, inner sep=1.5pt] at ({x:.2f},{ybot:.2f}) {{\footnotesize {v}}};")   # 8 pt tick labels
for i, (d, name, col) in enumerate(DOM):
    y = -0.6 - i * ROW
    c = N[f"{d}|ALL"]
    g = lambda t: c.get(t, 0)
    prim = sum(g(t) for t in TIERS)
    a(rf"\node[draw={col}border, fill={col}fill, line width=0.7pt, rounded corners=3pt, minimum width={BOXW}cm, minimum height=0.72cm, align=center, font=\footnotesize\bfseries] at ({BOXX},{y:.2f}) {{{name}}};")
    x = X0
    for j, t in enumerate(TIERS):
        n = g(t)
        if not n:
            continue
        w = n * U
        a(rf"\fill[tier{t}, rounded corners=0.8pt] ({x + GAP:.3f},{y - 0.24:.2f}) rectangle ({x + w - GAP:.3f},{y + 0.24:.2f});")
        if n >= 2:                                   # label only where it fits with padding
            a(rf"\node[text={TEXTCOL[j]}, inner sep=0pt] at ({x + w / 2:.3f},{y:.2f}) {{\scriptsize {n}}};")
        x += w
    a(rf"\node[anchor=west, inner sep=1pt] at ({x + 0.06:.2f},{y:.2f}) {{\scriptsize {prim}}};")
    o = g("3") + g("4")
    a(rf"\node[inner sep=1pt] at ({COLS['out']:.2f},{y:.2f}) {{\footnotesize\textbf{{{o}}} of {prim}}};")
    a(rf"\node[inner sep=1pt] at ({COLS['s']:.2f},{y:.2f}) {{\footnotesize {g('S')}}};")
    a(rf"\node[inner sep=1pt] at ({COLS['tot']:.2f},{y:.2f}) {{\footnotesize {sum(c.values())}}};")
A = N["ALL|ALL"]
ga = lambda t: A.get(t, 0)
ya = -0.6 - 5 * ROW + 0.05
a(rf"\draw[gridcol, line width=0.4pt] ({XR + 0.1:.2f},{ya + 0.38:.2f}) -- ({XR + 3.5:.2f},{ya + 0.38:.2f});")
a(rf"\node[anchor=east, inner sep=1pt, font=\footnotesize\bfseries] at ({XR + 0.12:.2f},{ya:.2f}) {{All}};")
a(rf"\node[inner sep=1pt] at ({COLS['out']:.2f},{ya:.2f}) {{\footnotesize\textbf{{{ga('3') + ga('4')}}} of {sum(ga(t) for t in TIERS)}}};")
a(rf"\node[inner sep=1pt] at ({COLS['s']:.2f},{ya:.2f}) {{\footnotesize {ga('S')}}};")
a(rf"\node[inner sep=1pt] at ({COLS['tot']:.2f},{ya:.2f}) {{\footnotesize {sum(A.values())}}};")
a(r"\end{tikzpicture}")
COLORS = r"""\definecolor{tier0}{HTML}{86B6EF}\definecolor{tier1}{HTML}{5598E7}\definecolor{tier2}{HTML}{2A78D6}
\definecolor{tier3}{HTML}{1C5CAB}\definecolor{tier4}{HTML}{104281}
\definecolor{gridcol}{HTML}{E4E3DF}\definecolor{inkmuted}{HTML}{5F5E5A}
\definecolor{orangeborder}{RGB}{181,133,84}\definecolor{orangefill}{RGB}{245,229,210}
\definecolor{blueborder}{RGB}{72,98,220}\definecolor{bluefill}{RGB}{227,237,248}
\definecolor{greenborder}{RGB}{74,166,74}\definecolor{greenfill}{RGB}{226,241,226}
\definecolor{purpleborder}{RGB}{132,94,194}\definecolor{purplefill}{RGB}{236,230,247}
\definecolor{tealborder}{RGB}{43,140,140}\definecolor{tealfill}{RGB}{223,242,242}
"""
D = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.path.join(tempfile.gettempdir(), "evidence_figure_regenerated")
os.makedirs(D, exist_ok=True)
open(os.path.join(D, "evidence_maturity_by_domain_body.tex"), "w", encoding="utf-8", newline="\n").write("\n".join(body) + "\n")
doc = (r"\documentclass[border=6pt]{standalone}" + "\n" + r"\usepackage{newtxtext}\usepackage{xcolor}\usepackage{tikz}" + "\n"
       + COLORS + r"\begin{document}" + "\n" + "\n".join(body) + "\n" + r"\end{document}" + "\n")
open(os.path.join(D, "evidence_maturity_by_domain.tex"), "w", encoding="utf-8", newline="\n").write(doc)
open(os.path.join(D, "tier_colors.tex"), "w", encoding="utf-8", newline="\n").write(COLORS)
print("regenerated sources written to the output directory")

import shutil, subprocess
ok = open(os.path.join(D, "evidence_maturity_by_domain.tex"), "rb").read() == open(os.path.join(OUT, "figures", "evidence_maturity_by_domain.tex"), "rb").read()
print(("[PASS]" if ok else "[FAIL]") + " regenerated figure source is byte-identical to figures/evidence_maturity_by_domain.tex")
status = 0 if ok else 1
if "--compile" in sys.argv:
    exe = shutil.which("pdflatex")
    if exe:
        r = subprocess.run([exe, "-interaction=nonstopmode", "-halt-on-error", "evidence_maturity_by_domain.tex"], cwd=D, capture_output=True, text=True)
        print(("[PASS]" if r.returncode == 0 else "[FAIL]") + " pdflatex compiles the regenerated standalone figure")
        status = status or r.returncode
    else:
        print("[NOT TESTABLE] compile: pdflatex not found")
sys.exit(status)
