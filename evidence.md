# Evidence

Test results and explanations for Sections 2.3 and 3.2, together with the reasoner results those sections depend on. A formal summary is also available in `checks/reasoner-report.md`; generated annotation-based documentation is under `docs/`. The OOPS! scan remains outstanding because the service could not be reached from the preparation environment; see `checks/oops-report.md`. Git repository creation/access remains an owner action.

## 0. Environment

| Item | Version |
|---|---|
| ROBOT (bundles the HermiT and ELK reasoners) | 1.9.11 |
| Java | OpenJDK 21.0.10 |
| Python and rdflib (SPARQL engine, no OWL reasoning) | Python 3.12.3, rdflib 7.6.0 |
| Date of runs | 13 October 2026 |

Everything below was produced by `scripts/run_checks.sh` (log in `build/run_checks.log`). Method:

1. `robot merge` joins `ontology.ttl` and `fixtures.ttl` into `build/merged.ttl`. This is the **asserted data**.
2. `robot reason --reasoner HermiT` checks consistency and satisfiability and writes `build/inferred.ttl`, with inferred subclass, equivalence and class-assertion axioms (all types, including indirect ones). This is the **inferred data**.
3. `scripts/run_cqs.py` runs every `queries/cqNN.rq` with rdflib against each file and compares with `tests/expected.json`.

Since rdflib does no OWL reasoning, reasoning-dependent queries are run on the HermiT output, and also on the asserted data so the dependency is visible.

## 1. Section 2.3: design evidence

### 1.1 Defined class classifies an individual without an asserted type

`bpu:FederalUniversity ≡ University ⊓ ∃maintainedBy.{uniao-federal}`. In `fixtures.ttl`, `bpu:ufscar` is typed only `bpu:University` and has `maintainedBy bpu:uniao-federal`.

| Individual | Asserted types | Types after HermiT |
|---|---|---|
| `ufscar` | `University` | `University`, **`FederalUniversity`** (inferred) |
| `ufmg` | `FederalUniversity` | `FederalUniversity`, `University` |
| `usp` | `StateUniversity` | `StateUniversity`, `University` |

### 1.2 Disjointness `FederalUniversity ⟂ StateUniversity`: why it matters

`tests/neg-disjoint.ttl` records a university as `StateUniversity` while it has `maintainedBy uniao-federal`. The defined class then makes it a `FederalUniversity` too.

| Run | Result |
|---|---|
| `ontology.ttl` + `tests/neg-disjoint.ttl` (with the axiom) | **Inconsistent**: HermiT reports "The ontology is inconsistent" |
| Same, with the `owl:disjointWith` line removed (`build/ontology.nodisj.ttl`) | **Consistent**. The individual is silently classified as `FederalUniversity`, `StateUniversity` and `University` |

Without the axiom the error is invisible. The same university would appear in **both** CQ6 (federal teaching load) and CQ8 (state lecturers), so the same lecturers would be counted under both spheres. The axiom turns a silent double classification into a detectable error. It is justified because the data model records one maintaining sphere per university.

### 1.3 Domain and range: where treating them as a data-entry check gives a wrong conclusion

**The place:** `bpu:maintainedBy rdfs:domain bpu:University`.

**The tempting reading.** "Only universities can have a maintainer. If someone enters a maintainer for something that is not a university, the system will reject it." That is how a domain works in a database schema or a form. In OWL it does not work that way: a domain is an **inference rule**. Any resource that appears as the subject of `maintainedBy` is *concluded* to be a `University`. Nothing is rejected, because OWL has no way to say "this resource is not a University" unless the data or another axiom says so (open-world assumption).

**The test.** `tests/demo-domain-range.ttl` adds a federal institute, typed only as `org:FormalOrganization`, with `maintainedBy uniao-federal`. Federal Institutes (*Institutos Federais*) are federal public institutions that are a separate category from universities. This is domain knowledge; I did not verify the legal basis in this session.

| Step | Result |
|---|---|
| HermiT on ontology + fixtures + demo file | **Consistent** (no rejection) |
| Types of the institute after reasoning | `FormalOrganization`, `Organization`, **`University`** (from the domain), **`FederalUniversity`** (from the defined class) |
| CQ2 on this graph | Returns three rows: the two real federal universities **plus the institute**. `run_cqs.py` reports `FAIL` against the expected two rows, and that failure is the evidence. |

**Why it is wrong.** The institute is not a university, yet the reasoner derived that it is, and a federal one, and a query result now contains it. A person who believed the domain was a check would have trusted the (silent) result.

**What I did about it.** The domain is kept because every maintained institution in the declared scope is a university, and the risk is stated in the `skos:scopeNote` on `maintainedBy`. If non-university institutions enter the scope, either widen the domain to `org:FormalOrganization` or add a closed-world rule (the optional SHACL step 4.4: a shape that requires subjects of `maintainedBy` to be typed `University`).

**Contrast: a datatype range with a facet behaves differently.** `tests/neg-weekly-hours.ttl` gives an assignment `weeklyHours 99`, outside the facet range 1 to 40. HermiT reports the ontology **inconsistent**. A datatype value outside its range cannot be repaired by inferring a new type, so it is a contradiction. Object domains and ranges produce inferences, while datatype ranges can produce inconsistencies. Neither is a form validator.

### 1.4 Other design checks

- **Functional properties.** `ofCourse`, `heldInTerm`, `assignedPerson`, `assignedOffering`, `assignmentRole` and the datatype properties are functional. The fixtures respect this and HermiT finds the model consistent.
- **Genuine is-a only.** Subclass axioms: `University`, `GovernmentBody` ⊑ `org:FormalOrganization`; `Department` ⊑ `org:OrganizationalUnit`; `StateUniversity` ⊑ `University`; `TeachingRole` ⊑ `org:Role`. Part-of, participation and maintenance are properties.

## 2. Reasoner results used by Section 3.2

| Check | Tool | Result |
|---|---|---|
| Consistency of `ontology.ttl` + `fixtures.ttl` | HermiT (ROBOT `reason`) | **Consistent** |
| Unsatisfiable classes | HermiT (ROBOT `reason` fails on any) | **None** |
| Defined-class inference (UFSCar is a `FederalUniversity`) | HermiT | **Occurs** (Section 1.1) |
| Cross-check | ELK (ROBOT `reason`) | All 11 CQs pass on the ELK output too |

These satisfy the intent of 4.1. A separate, formal 4.1 report will be written in the next step.

**Tooling gotcha, fixed.** With the ROBOT generator `PropertyAssertion` enabled, the output contained duplicate literals typed `internal:anonymous-constants`, and CQ10 returned wrong rows (`2026/1` appeared and `2026/2` twice). The generators are now `SubClass EquivalentClass ClassAssertion`, which is all the CQs need. This was a tool artefact, not a model error.

## 3. Section 3.1: fixture coverage

| CQ | Individuals that exercise it |
|---|---|
| 1 | `ana` with assignments in 2026/1 and 2026/2 (to check the term filter) |
| 2 | `ufscar` (inferred), `ufmg` (asserted), `usp` (not federal) |
| 3 | Two "Databases" courses at different universities, in the same term |
| 4 | Four departments; `ufscar-dc` has offerings in both terms |
| 5, 9 | `off-ufscar-comp-db-2026-1` has a lead and a co-lecturer |
| 6 | `ana` (8 h), `bruno` (6 h, two offerings, two roles), `carla` (4 h); `diego` is state; `eva` is an assistant |
| 7 | `COMP-OE` offered in two terms |
| 8 | `diego` at USP, a state university |
| 10 | Two terms with different dates around 2026-10-13 |
| 11 | `eva` with `teaching-assistant-role` |

## 4. Section 3.2: every CQ, expected and actual

"Asserted" means ontology + fixtures merged, with no reasoner. "Inferred" means after HermiT. Row order is not significant.

| CQ | Expected | Actual: asserted | Actual: inferred | OWL inference needed? |
|---|---|---|---|---|
| 1 | (Databases, COMP-DB, 4), (Ontology Engineering, COMP-OE, 4) | same | same | No |
| 2 | UFMG, UFSCar | **UFMG only** | UFMG, UFSCar | **Yes** |
| 3 | UFMG, UFSCar | **UFSCar only** | UFMG, UFSCar | **Yes** |
| 4 | DC-UFSCar 2, DM-UFSCar 1, DCC-UFMG 1, CC-USP 1 | **only the two UFSCar rows** | all four rows | **Yes** |
| 5 | (Ana Silva, Lead lecturer), (Bruno Costa, Co-lecturer) | same | same | No |
| 6 | (Ana Silva, 8), (Bruno Costa, 6), (Carla Souza, 4) | **Carla Souza 4 only** | all three rows | **Yes** |
| 7 | 2026/1, 2026/2 | same | same | No |
| 8 | Diego Lima | same | same | No |
| 9 | (Databases, COMP-DB, 2) | same | same | No |
| 10 | 2026/2 | same | same | No |
| 11 | (Eva Rocha, Ontology Engineering, COMP-OE) | same | same | No |

**Result: 11 of 11 CQs return the expected result on the inferred data (HermiT, and also ELK). 7 of 11 already pass on the asserted data; 4 depend on inference.**

### Explanation of the four inference-dependent results

- **CQ2.** UFSCar has no asserted `FederalUniversity` type. It appears only because of the `owl:equivalentClass` definition (University with `maintainedBy` value `uniao-federal`).
- **CQ6.** Ana Silva and Bruno Costa teach only at UFSCar, so their rows depend on the same defined-class inference as CQ2. Without it, only Carla Souza (UFMG, asserted federal) is returned.
- **CQ3.** The query asks for `a bpu:University`. UFMG is asserted only as `FederalUniversity`, so `FederalUniversity ⊑ University` (a consequence of the equivalence axiom) is needed.
- **CQ4.** Same reason as CQ3. UFMG and USP are typed with subclasses of `University`. A plain SPARQL engine does no subclass reasoning, so these departments are lost without it.

The other seven queries use only asserted triples (or property paths) and do not depend on OWL inference.

## 5. Open-world caveat on these results

- **A missing row is not a false statement.** On the inferred graph, `ASK { bpu:usp a bpu:FederalUniversity }` returns `false`. This means only that the data does not entail it. It does not prove that USP is not federal. What makes USP non-federal here is the combination of its asserted `maintainedBy` value, the disjointness axiom, and the fixture's choice to record a single maintainer.
- **Counts are counts of recorded facts.** CQ4 and CQ9 count recorded offerings and assignments. CQ9's answer, one offering with two lecturers, does not say that no other offering has two. For example, no co-lecturer is recorded for the USP offering, which does not show that it has none.
- **Closed-world checks need a closed-world tool.** If the application must reject a record (a missing required value, a wrongly typed subject of `maintainedBy`), that is the job of SHACL (optional step 4.4), not of OWL axioms.

## 6. Not done yet (next steps)

| Item | Status |
|---|---|
| 4.1 Formal reasoner report (HermiT, unsatisfiable classes, defined-class inference, fixes) | Summary added at `checks/reasoner-report.md`; profile caveat recorded |
| 4.2 OOPS! report and critical-issue list; documentation under `docs/` | HTML annotation reference generated; OOPS! scan not run, transparently recorded in `checks/oops-report.md` |
| 4.3 `README.md`, Git repository link, release/versioning and licence choices | README added; actual GitHub URL and repository access must be supplied by the project owner |
| 4.4 Optional SHACL shape and rejected fixture | Pending (optional, no marks) |
| Stable IRIs | `example.org` IRIs are placeholders and must be replaced before release |
