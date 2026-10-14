#!/usr/bin/env python3
"""Run every queries/cqNN.rq against one RDF file and compare with tests/expected.json.

usage: run_cqs.py DATA.ttl [--json]
Exit code 0 when every CQ result equals its expected result.
"""
import glob, json, os, sys
from rdflib import Graph

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = sys.argv[1]
as_json = "--json" in sys.argv

g = Graph()
g.parse(data, format="turtle")

with open(os.path.join(root, "tests", "expected.json"), encoding="utf-8") as f:
    expected = json.load(f)

def norm(v):
    py = v.toPython() if v is not None else None
    return py if isinstance(py, (int, str)) else str(py)

report, ok_all = {}, True
for q in sorted(glob.glob(os.path.join(root, "queries", "cq*.rq"))):
    cq = os.path.basename(q)[:-3]
    res = g.query(open(q, encoding="utf-8").read())
    rows = sorted([[norm(c) for c in r] for r in res], key=lambda r: [str(x) for x in r])
    exp = sorted(expected[cq], key=lambda r: [str(x) for x in r])
    ok = rows == exp
    ok_all &= ok
    report[cq] = {"ok": ok, "actual": rows, "expected": exp}

if as_json:
    print(json.dumps(report, ensure_ascii=False, indent=1))
else:
    for cq, r in report.items():
        print(f"{cq}: {'PASS' if r['ok'] else 'FAIL'}  actual={r['actual']}" + ("" if r['ok'] else f"  expected={r['expected']}"))
sys.exit(0 if ok_all else 1)
