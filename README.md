# BPU-Teaching — Brazilian Public University Teaching Ontology

A small OWL 2 ontology for course offerings, academic terms, departments, and teaching assignments at Brazilian public universities. The submission archive is self-contained; the fixtures are synthetic.

## Contents

- `requirements.md` — ORSD, scope, glossary, 11 competency questions, reuse decisions, and design pattern.
- `ontology.ttl` — OWL ontology (Turtle), annotations, ontology/version IRIs, class definitions, domains/ranges, and constraints.
- `fixtures.ttl` — synthetic test data.
- `queries/cq01.rq` … `queries/cq11.rq` — one SPARQL query per competency question.
- `evidence.md` — CQ expected/actual results and modelling explanations.
- `runner.py` — generic PyOxigraph command-line query runner; this is separate from the OWL reasoning workflow.
- `scripts/run_cqs.py` — evaluates CQs against a supplied Turtle graph and compares results to `tests/expected.json`.
- `scripts/run_checks.sh` — reproducible ROBOT/HermiT/ELK check workflow.
- `tests/` — expected results and negative/domain-range demonstration fixtures.
- `checks/` — dated logs and generated reasoner outputs available from the recorded run.
- `docs/index.html` — generated, human-readable documentation from ontology annotations.

## Requirements

- Python 3.10+ (tested with Python 3.12.3)
- `rdflib` (tested with 7.6.0)
- Java 11+ (tested with OpenJDK 21.0.10)
- ROBOT 1.9.11 (`robot.jar`) for OWL reasoning and profile checks
- Optional: PyOxigraph for `runner.py`

## Run the competency queries

From the repository root:

```bash
python -m pip install rdflib==7.6.0
python scripts/run_cqs.py checks/inferred.ttl
```

The inferred graph is included as a convenience for offline grading, but it should be regenerated from the source ontology and fixtures before treating it as fresh evidence. To check asserted data only:

```bash
python scripts/run_cqs.py checks/merged.ttl
```

Four CQs are expected to require OWL inference, so they will not all pass against asserted-only triples.

## Reproduce the reasoner workflow

Download ROBOT 1.9.11 from its official project releases and place `robot.jar` at the repository root, or set `ROBOT_JAR` to its full path. Then run:

```bash
ROBOT_JAR=/path/to/robot.jar bash scripts/run_checks.sh
```

The script merges the ontology and fixtures, runs HermiT and ELK, checks all CQs on asserted and inferred graphs, and runs negative/domain-range demonstrations. Fresh outputs are written to `build/`. The reasoner logs included under `checks/` document the recorded 2026-10-13 run. Re-run the workflow to create fresh local results.

## Generic runner.py

`runner.py` is a separate generic PyOxigraph utility. Install it with:

```bash
python -m pip install pyoxigraph
```

Examples:

```bash
# Query one RDF/Turtle file
python runner.py fixtures.ttl queries/cq01.rq

# Load ontology + fixtures into the default graph and query
python runner.py --data ontology.ttl --data fixtures.ttl queries/cq01.rq

# Load a file into a named graph
python runner.py --graph fixtures.ttl https://example.org/graph/fixtures queries/cq01.rq
```

**Important:** `runner.py` does not perform OWL reasoning. Its SPARQL results should not be used to claim the inference-dependent CQs pass unless you explicitly load reasoner-generated data. `scripts/run_checks.sh` is the intended OWL-aware evaluation path.

## Documentation and OOPS!

Open `docs/index.html` locally in a browser. It is a lightweight HTML reference generated from the ontology annotations, not a claim that WIDOCO was run. The OOPS! assessment is not yet completed: `checks/oops-report.md` records this limitation and the exact remaining action. Run the ontology through the OOPS! web service and save its report or dated screenshots in `checks/`, then update that file and the critical-issue table before submission.

## Repository, versioning, and licence

- Project repository: `[https://github.com/<YOUR_GITHUB_USERNAME>/bpu-teaching-ontology](https://github.com/natalzera/bpu-teaching-ontology)`;
- Ontology version: `0.1.0`; the ontology IRI is currently `https://example.org/bpu` and version IRI `https://example.org/bpu/0.1.0`;
- Project licence: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/), as declared in the ontology metadata. Keep the attribution and source-vocabulary licence notes in `requirements.md`.
- Suggested release process: commit source files, tag `v0.1.0`, and attach this ZIP to the release. Increment the patch version for corrections that do not change the model's intended meaning; increment minor/major versions for compatible/incompatible modelling changes.
