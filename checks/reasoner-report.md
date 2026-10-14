# Section 4.1 — Reasoner report

**Recorded run date:** 2026-10-13  
**Reasoner workflow:** ROBOT 1.9.11 + HermiT; ELK used as a cross-check.  
**Source log:** [`reasoner-and-cq-run-2026-10-13.log`](reasoner-and-cq-run-2026-10-13.log), [`control-tests-2026-10-13.log`](control-tests-2026-10-13.log).

## Results

- Ontology merged with `fixtures.ttl`: **consistent** according to HermiT.
- Unsatisfiable classes: **none reported** by the recorded HermiT run.
- Defined-class inference: **confirmed**. `bpu:ufscar` is asserted as `bpu:University` and maintained by `bpu:uniao-federal`; HermiT infers `bpu:FederalUniversity` from the `owl:equivalentClass` definition.
- Competency queries: all **11/11 pass** against the HermiT-inferred graph. The ELK cross-check log records all 11 passing as well.
- Negative disjointness test: the combined ontology and `tests/neg-disjoint.ttl` is inconsistent, as intended. Removing the disjointness axiom makes that negative test consistent and silently classifies the same individual as both federal and state university.
- Datatype facet test: `tests/neg-weekly-hours.ttl` is inconsistent because the weekly-hours value violates the declared 1–40 range.

## OWL 2 DL profile caveat

The archived `profile-validation-2026-10-13.log` records a ROBOT OWL 2 DL profile validation failure involving `xsd:date` literals used with datatype restrictions. Do **not** claim strict OWL 2 DL profile compliance based on this run. Review the datatype restriction and/or the validation command, then rerun profile validation with the exact command recorded in the working notes. The reasoner consistency and CQ results above are separate results and do not erase this profile warning.

## Reproduction

From the repository root, with Java and ROBOT 1.9.11 available:

```bash
ROBOT_JAR=/path/to/robot.jar bash scripts/run_checks.sh
```

The archived logs are evidence of the recorded run; rerunning the command is recommended for fresh evidence.
