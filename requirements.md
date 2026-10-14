# Ontology Requirements Specification Document (ORSD)

**Ontology:** BPU-Teaching, an ontology of course offerings and teaching assignments at Brazilian public universities
**Namespace (placeholder):** `bpu:` = `https://example.org/bpu#`
**Ontology IRI (placeholder):** `https://example.org/bpu`
**Version IRI (placeholder):** `https://example.org/bpu/0.1.0`

> The `example.org` IRIs are placeholders. Replace them with a stable IRI (for example a w3id.org redirect) before the first release.

---

## 1. Section 1.1: Requirements and Scope

### 1.1 Purpose

The ontology gives a shared, machine-readable vocabulary for describing **who teaches which course offering, in which academic term, at which Brazilian public university**. It lets a university transparency or analytics portal integrate teaching data from different institutions and answer questions about it, including questions that depend on classifying institutions by who maintains them (federal or state).

### 1.2 Concrete task supported

> **For a given lecturer and academic term, list the course offerings they teach, with the course title, course code, and weekly hours.**
> A second task builds on it: *aggregate teaching load per lecturer across all federal universities in a term.*

The first task is CQ1, the second is CQ6. Both use the teaching-assignment pattern, and CQ6 additionally needs the inferred class `FederalUniversity`.

### 1.3 Scope

**In scope**

| Area | Detail |
|---|---|
| Institutions | Public universities maintained by the Federal Government (*federal*) or a state government (*estadual*) |
| Internal structure | Departments (academic units) that are part of a university |
| Courses | Catalogue courses (code, title, nominal workload) and the department responsible for them |
| Offerings | A course offered in a specific academic term |
| Teaching | Who is assigned to an offering, in which role (lead lecturer, co-lecturer, teaching assistant), and with how many weekly hours |
| Time | Academic terms (e.g. `2026/1`) with start and end dates |

**Out of scope**

- Private, community, and municipal institutions (not enough cases to model well in a small ontology).
- Students, enrolment, grades, attendance.
- Degree programmes and curricula (course prerequisites, programme structure).
- Timetables, rooms, buildings, campuses.
- Employment contracts, salaries, career ranks, and research output.
- Governance beyond the maintaining body (rectors, councils).

**Level of detail**

- Instance-level data for universities, departments, courses, offerings, assignments, and terms.
- Time granularity is the **academic term**, with start and end dates only (no hour-level scheduling).
- Teaching load is a whole number of **weekly hours per assignment**.
- Departments are the smallest organisational unit. Faculties or institutes between department and university are allowed but not required. Queries follow `org:subOrganizationOf` with a SPARQL `+` path (ORG declares `subOrganizationOf` as a sub-property of a transitive property, not as transitive itself).

### 1.4 Intended users and uses

| User | Use |
|---|---|
| Portal developers | Query offerings and assignments through SPARQL, and publish them as Linked Data |
| Data analysts and transparency officers | Compare teaching load and course supply across federal and state universities |
| Ontology engineers (course context) | Reuse and extend the model, and study the effect of the design choices |
| Prospective students and staff (indirect) | See which courses are offered where and when, through a front-end built on the ontology |

### 1.5 Implementation language and tooling

- **OWL 2 DL**, serialised as **Turtle** (`.ttl`).
- **SPARQL 1.1** for competency-question queries (`queries/cqNN.rq`).
- Reasoner: HermiT (via Protégé or ROBOT), with ELK as a cross-check. The ontology should stay within OWL 2 DL.
- Quality and documentation tools: OOPS!, WIDOCO.
- Optional validation: SHACL (`pyshacl`).
- Tool versions are recorded in `README.md`.

### 1.6 Sources of knowledge

- Domain knowledge of how Brazilian federal and state universities are organised (course offerings per term, departments, teaching roles).
- Public institutional data, to be consulted and cited when the fixtures are written: the INEP *Censo da Educação Superior*, the e-MEC register of institutions, and public course-offering pages of the universities.
- **The fixtures are synthetic.** University names are real. Lecturers, courses, offerings, hours, and term dates are invented for testing and do not describe real people or real schedules.
- External vocabularies are evaluated in Section 2.1 (to be added).

### 1.7 Non-functional requirements

| Requirement | Decision |
|---|---|
| Naming | Classes in `UpperCamelCase`, properties in `lowerCamelCase`, individuals in lowercase-with-hyphens (e.g. `bpu:ufscar`). English local names. |
| Natural language | Labels (`rdfs:label`) in **English (`@en`)** and **Brazilian Portuguese (`@pt-BR`)**. Definitions (`skos:definition`) in English. |
| Documentation | Every local class and property has a label and a definition. |
| Reuse | Reuse existing IRIs for generic notions (person, organisation, part-of, title). Do not redefine them locally. At least two external sources are actually used (Section 2.1). |
| Modelling style | `rdfs:subClassOf` only for genuine is-a. Part-of, participation, and maintenance are properties. Roles are modelled as role individuals plus a participation pattern, not as person subclasses. |
| Licensing | Ontology: **CC BY 4.0** (proposed). Fixtures: **CC0** (synthetic data). External terms keep their own licences (Section 2.1). |
| Versioning | Semantic version in `owl:versionIRI`, and the same version in `owl:versionInfo` and in the Git tag. |
| Logical profile | OWL 2 DL, consistent, with no unsatisfiable classes. |

### 1.8 Pre-glossary of candidate terms

Type = possible **C**lass, **I**ndividual, **P**roperty (object **OP** / datatype **DP**), or **V**alue. These are candidates. Section 2.3 settles the final model.

| Term | Type | Note |
|---|---|---|
| University | C | Public higher-education institution. Candidate for reuse or alignment with an organisation class. |
| FederalUniversity | C (defined) | A university maintained by the Federal Government. Classified by a reasoner. |
| StateUniversity | C | A university maintained by a state government. Disjoint with `FederalUniversity`. |
| Department | C | Academic unit that is part of a university. |
| Person | C | A human. Reuse candidate (FOAF). |
| Course | C | A catalogue entry such as "Databases". |
| CourseOffering | C | A course offered in one term. Distinct from `Course`. |
| AcademicTerm | C | A semester such as `2026/1`. |
| TeachingAssignment | C | Reified relation: person + offering + role + weekly hours. |
| TeachingRole | C | Kinds of role in an assignment. |
| GovernmentBody | C | An authority that maintains a university. |
| Lecturer / Professor | not a class | A *role played* by a person, not a kind of person. Captured by the assignment pattern and role individuals. |
| Student, Grade, Enrolment | rejected | Out of scope. |
| uniao-federal, estado-de-sao-paulo | I | Individuals of `GovernmentBody`. |
| lead-lecturer-role, co-lecturer-role, teaching-assistant-role | I | Individuals of `TeachingRole`. |
| ufscar, ufmg, usp | I | Universities. |
| 2026/1, 2026/2 | I | Individuals of `AcademicTerm`. |
| maintainedBy | OP | University to GovernmentBody. |
| subOrganizationOf | OP | Part-of for departments and universities. Reuse candidate (W3C ORG), transitive. |
| responsibleUnit | OP | Course to Department. |
| ofCourse | OP | CourseOffering to Course. |
| heldInTerm | OP | CourseOffering to AcademicTerm. |
| assignedPerson | OP | TeachingAssignment to Person. |
| assignedOffering | OP | TeachingAssignment to CourseOffering. |
| assignmentRole | OP | TeachingAssignment to TeachingRole. |
| name | DP | Name of a person or organisation. Reuse candidate (FOAF). |
| title | DP | Course title. Reuse candidate (Dublin Core Terms). |
| courseCode | DP | String such as `COMP-DB`. |
| termCode | DP | String such as `2026/1`. |
| startDate, endDate | DP | `xsd:date` bounds of a term. |
| weeklyHours | DP | `xsd:integer` hours per week for an assignment. |
| "Databases", "COMP-DB", `2026/1`, `4` | V | Example literal values. |

---

## 2. Section 1.2: Competency Questions

The queries use `bpu:` and the reused prefixes `foaf:` (FOAF), `org:` (W3C ORG), and `dcterms:` (Dublin Core Terms). Parameters such as the lecturer, term, or course are fixed in each query so that the result is deterministic. The query file for CQ*n* is `queries/cqNN.rq` (zero-padded). Expected answers refer to the synthetic fixtures planned for Section 3.1. They are confirmed in `evidence.md` once `fixtures.ttl` exists.

**Fixture world assumed by the expected answers**

- Universities: `ufscar` (federal, **type not asserted**, only `maintainedBy uniao-federal`), `ufmg` (federal, asserted), `usp` (state, asserted).
- Departments: UFSCar has *Departamento de Computação* and *Departamento de Matemática*. UFMG has *Departamento de Ciência da Computação*. USP has *Departamento de Ciências de Computação*.
- Terms: `2026/1` (2026-03-02 to 2026-07-11) and `2026/2` (2026-08-03 to 2026-12-12).
- Offerings: UFSCar `COMP-OE` (2026/1 and 2026/2), UFSCar `COMP-DB` (2026/1), UFSCar `MAT-LA` (2026/1), UFMG `DCC-DB` "Databases" (2026/1), USP `SCC-KR` (2026/1).
- Assignments (lead = lead lecturer, co = co-lecturer, TA = teaching assistant):
  Ana Silva: lead `COMP-OE` 2026/1 (4 h), lead `COMP-DB` 2026/1 (4 h), lead `COMP-OE` 2026/2 (4 h).
  Bruno Costa: co `COMP-DB` 2026/1 (2 h), lead `MAT-LA` 2026/1 (4 h).
  Carla Souza: lead `DCC-DB` 2026/1 (4 h).
  Diego Lima: lead `SCC-KR` 2026/1 (4 h).
  Eva Rocha: TA `COMP-OE` 2026/1 (2 h).

### CQ1: Offerings of a lecturer in a term *(core task)*

**Question:** Which course offerings does Ana Silva teach in term 2026/1, and with what course code and weekly hours?
**Answer shape:** table of (`title`, `code`, `weeklyHours`).
**Expected answer:** (`"Ontology Engineering"`, `"COMP-OE"`, 4), (`"Databases"`, `"COMP-DB"`, 4).
**Needs:**
- Classes: `TeachingAssignment`, `CourseOffering`, `Course`, `AcademicTerm`, `Person`.
- Properties: `assignedPerson`, `assignedOffering`, `ofCourse`, `heldInTerm`, `weeklyHours`, `courseCode`, `termCode`, `foaf:name`, `dcterms:title`.
**Query:** `queries/cq01.rq`

### CQ2: Federal universities *(inference)*

**Question:** Which universities are federal universities?
**Answer shape:** list of university names.
**Expected answer:** "Universidade Federal de Minas Gerais", "Universidade Federal de São Carlos". UFSCar is in the list only by inference from `maintainedBy bpu:uniao-federal`.
**Needs:**
- Classes: `FederalUniversity` (defined, `owl:equivalentClass`), `University`, `GovernmentBody`.
- Properties: `maintainedBy`, `foaf:name`.
**Query:** `queries/cq02.rq`

### CQ3: Universities offering a course in a term

**Question:** Which universities offer a course titled "Databases" in term 2026/1?
**Answer shape:** list of university names.
**Expected answer:** "Universidade Federal de São Carlos", "Universidade Federal de Minas Gerais".
**Needs:**
- Classes: `CourseOffering`, `Course`, `Department`, `University`, `AcademicTerm`.
- Properties: `ofCourse`, `heldInTerm`, `responsibleUnit`, `org:subOrganizationOf` (followed transitively), `dcterms:title`, `termCode`, `foaf:name`.
**Reasoning:** needed for the UFMG row. UFMG is asserted as `FederalUniversity` only, and the query asks for `University`, so `FederalUniversity ⊑ University` must be inferred (observed in `evidence.md`).
**Query:** `queries/cq03.rq`

### CQ4: Offerings per department in a term

**Question:** How many course offerings does each department have in term 2026/1?
**Answer shape:** table of (`department name`, `university name`, `integer count`). Row order is not significant.
**Expected answer:**

| Department | University | Count |
|---|---|---|
| Departamento de Computação | Universidade Federal de São Carlos | 2 |
| Departamento de Matemática | Universidade Federal de São Carlos | 1 |
| Departamento de Ciência da Computação | Universidade Federal de Minas Gerais | 1 |
| Departamento de Ciências de Computação | Universidade de São Paulo | 1 |

**Needs:**
- Classes: `Department`, `University`, `Course`, `CourseOffering`, `AcademicTerm`.
- Properties: `responsibleUnit`, `ofCourse`, `heldInTerm`, `org:subOrganizationOf`, `termCode`, `foaf:name`.
**Reasoning:** needed for the UFMG and USP rows (subclass inference to `University`, as for CQ3).
**Note:** the count covers only recorded offerings. Under the open-world assumption it is not a claim that no other offerings exist.
**Query:** `queries/cq04.rq`

### CQ5: Lecturers and roles for an offering *(role pattern)*

**Question:** Who teaches the offering of course `COMP-DB` in term 2026/1, and in which lecturer role (lead or co-lecturer)?
**Answer shape:** table of (`person name`, `role label`).
**Expected answer:** (`"Ana Silva"`, "Lead lecturer"), (`"Bruno Costa"`, "Co-lecturer").
**Needs:**
- Classes: `TeachingAssignment`, `TeachingRole`, `CourseOffering`, `Course`, `AcademicTerm`, `Person`.
- Properties: `assignedPerson`, `assignedOffering`, `assignmentRole`, `ofCourse`, `heldInTerm`, `courseCode`, `termCode`, `foaf:name`, `rdfs:label`.
**Query:** `queries/cq05.rq`

### CQ6: Teaching load at federal universities *(inference and aggregation)*

**Question:** What is the total weekly teaching hours per lecturer at federal universities in term 2026/1, counting lecturer roles only (lead and co-lecturer)?
**Answer shape:** table of (`person name`, `integer total hours`).
**Expected answer:** (`"Ana Silva"`, 8), (`"Bruno Costa"`, 6), (`"Carla Souza"`, 4). Diego Lima is excluded (USP is a state university). Eva Rocha is excluded (teaching-assistant role). Ana Silva's 2026/2 assignment is excluded (different term). Ana Silva and Bruno Costa teach at UFSCar, which counts as federal only by inference.
**Needs:**
- Classes: `FederalUniversity`, `Department`, `Course`, `CourseOffering`, `AcademicTerm`, `TeachingAssignment`, `TeachingRole`, `Person`.
- Properties: `maintainedBy`, `org:subOrganizationOf`, `responsibleUnit`, `ofCourse`, `heldInTerm`, `assignedPerson`, `assignedOffering`, `assignmentRole`, `weeklyHours`, `termCode`, `foaf:name`.
**Query:** `queries/cq06.rq`

### CQ7: Terms in which a course was offered

**Question:** In which terms has the course `COMP-OE` been offered?
**Answer shape:** list of term codes.
**Expected answer:** `"2026/1"`, `"2026/2"`.
**Needs:**
- Classes: `Course`, `CourseOffering`, `AcademicTerm`.
- Properties: `ofCourse`, `heldInTerm`, `courseCode`, `termCode`.
**Query:** `queries/cq07.rq`

### CQ8: Lecturers at state universities

**Question:** Which lecturers teach at a state university in term 2026/1 (lead or co-lecturer role)?
**Answer shape:** list of person names.
**Expected answer:** `"Diego Lima"`.
**Needs:**
- Classes: `StateUniversity`, `Department`, `Course`, `CourseOffering`, `AcademicTerm`, `TeachingAssignment`, `TeachingRole`, `Person`.
- Properties: `org:subOrganizationOf`, `responsibleUnit`, `ofCourse`, `heldInTerm`, `assignedPerson`, `assignedOffering`, `assignmentRole`, `termCode`, `foaf:name`.
**Note:** this is the state counterpart of CQ6. It shows why `FederalUniversity` and `StateUniversity` must be disjoint, so that no university lands in both result sets.
**Query:** `queries/cq08.rq`

### CQ9: Co-taught offerings

**Question:** Which offerings in term 2026/1 have more than one lecturer assigned (lead or co-lecturer role)?
**Answer shape:** table of (`title`, `code`, `integer number of lecturers`).
**Expected answer:** (`"Databases"`, `"COMP-DB"`, 2).
**Needs:**
- Classes: `TeachingAssignment`, `TeachingRole`, `CourseOffering`, `Course`, `AcademicTerm`.
- Properties: `assignedPerson`, `assignedOffering`, `assignmentRole`, `ofCourse`, `heldInTerm`, `termCode`, `courseCode`, `dcterms:title`.
**Note:** the count covers recorded assignments only. An offering with one recorded lecturer may still have others under the open-world assumption.
**Query:** `queries/cq09.rq`

### CQ10: Terms containing a date

**Question:** Which academic terms include the date 2026-10-13?
**Answer shape:** list of term codes.
**Expected answer:** `"2026/2"`.
**Needs:**
- Classes: `AcademicTerm`.
- Properties: `termCode`, `startDate`, `endDate`.
**Query:** `queries/cq10.rq`

### CQ11: Teaching assistants in a term

**Question:** Which persons are teaching assistants in term 2026/1, and for which course offerings?
**Answer shape:** table of (`person name`, `title`, `code`).
**Expected answer:** (`"Eva Rocha"`, `"Ontology Engineering"`, `"COMP-OE"`).
**Needs:**
- Classes: `TeachingAssignment`, `TeachingRole`, `CourseOffering`, `Course`, `AcademicTerm`, `Person`.
- Properties: `assignedPerson`, `assignedOffering`, `assignmentRole`, `ofCourse`, `heldInTerm`, `termCode`, `courseCode`, `foaf:name`, `dcterms:title`.
**Query:** `queries/cq11.rq`

---

## 3. Coverage summary

"Needs reasoning" was **observed**: the query fails on the asserted data (ontology + fixtures merged, no reasoner) and passes after HermiT. See `evidence.md`.

| CQ | Needs reasoning (observed) | Property path | Aggregation | Pattern (2.2) |
|---|---|---|---|---|
| 1 | no | no | no | teaching assignment |
| 2 | **yes**: defined class (UFSCar) | no | no | |
| 3 | **yes**: subclass inference (UFMG) | yes | no | |
| 4 | **yes**: subclass inference (UFMG, USP) | yes | yes | |
| 5 | no | no | no | teaching assignment |
| 6 | **yes**: defined class (UFSCar) | yes | yes | teaching assignment |
| 7 | no | no | no | |
| 8 | no | yes | no | teaching assignment |
| 9 | no | no | yes | teaching assignment |
| 10 | no | no | no | |
| 11 | no | no | no | teaching assignment |

Ontology-level checks (disjointness, domain/range behaviour, datatype facet, consistency) are covered by `ontology.ttl`, `fixtures.ttl`, `tests/*.ttl` and `evidence.md`.

---

# Part 2: Reuse and Ontology Design

## 4. Section 2.1: Reuse decisions

Evaluated on 13 October 2026 from the sources named below. "Not verified" marks facts I did not check in this session.

| Source | IRI | Terms evaluated | Decision |
|---|---|---|---|
| FOAF | `http://xmlns.com/foaf/0.1/` | `foaf:Person`, `foaf:name`, `foaf:Agent`, `foaf:Organization` | **Reuse IRIs** (`foaf:Person`, `foaf:name`) via a minimal extract |
| W3C ORG | `http://www.w3.org/ns/org#` | `org:FormalOrganization`, `org:OrganizationalUnit`, `org:subOrganizationOf`, `org:Role`, `org:Membership`, `org:unitOf` | **Extract a module and reuse IRIs** for the first four; **align, not reuse**, `org:Membership` |
| DCMI Metadata Terms | `http://purl.org/dc/terms/` | `dcterms:title`, `dcterms:license`, `dcterms:creator`, `dcterms:created`, `dcterms:description` | **Reuse IRIs** |
| SKOS | `http://www.w3.org/2004/02/skos/core#` | `skos:definition`, `skos:scopeNote`, `skos:closeMatch`, `skos:Concept` | **Reuse IRIs** (annotation vocabulary) |
| schema.org | `https://schema.org/` | `schema:CollegeOrUniversity`, `schema:Course`, `schema:CourseInstance`, `schema:courseCode`, `schema:instructor` | **Align** with `skos:closeMatch`; do not reuse as logical terms |
| AIISO | `http://purl.org/vocab/aiiso/schema#` | `aiiso:Institution`, `aiiso:Department`, `aiiso:Faculty` | **Reject** |
| OWL-Time | `http://www.w3.org/2006/time#` | `time:Interval` | **Reject** (no CQ needs it) |

Terms from FOAF, ORG, DCTerms and SKOS are used in `ontology.ttl`, so the requirement of at least two external sources is met four times over.

**FOAF.** Reuse `foaf:Person` for people and `foaf:name` for names of people and organisations. *Licence:* the specification states it is under a Creative Commons Attribution licence (the version is not stated on the page I read). *Maintenance:* latest specification is 0.99 ("Paddington Edition", 14 January 2014). The namespace IRI is fixed and described as stable, and the project is maintained by its original authors. The vocabulary is old but stable and very widely used, which is the right profile for a base vocabulary. *Why an extract, not an import:* `owl:imports` would pull in FOAF's full RDFS/OWL file with many unused terms and some constructs outside OWL 2 DL. The extract copies only `Person`, `Agent`, `name` and the `Person ⊑ Agent` axiom.

**W3C ORG.** The best fit for universities (`org:FormalOrganization`), departments (`org:OrganizationalUnit`) and part-of (`org:subOrganizationOf`). `bpu:TeachingRole` is a subclass of `org:Role`, a genuine is-a. *Licence:* the specification is a W3C Recommendation under W3C document rules; the Turtle file declares `dct:license` as the Open Data Commons PDDL 1.0 (public domain dedication), as I read in the file. *Maintenance:* W3C Recommendation of 16 January 2014; vocabulary version 0.8, last modification dated 2014-04-12 in the file; an errata page exists. It is frozen but stable. *Why a module:* the sandbox cannot dereference `w3.org` during reasoning, and an import would load posts, sites and change events that no CQ uses. The extract in `ontology.ttl` copies the axioms we depend on faithfully, including that `subOrganizationOf` is a sub-property of the transitive `transitiveSubOrganizationOf`, and that `org:Organization` is disjoint with `org:Role`.
*`org:Membership` (align only):* it is an n-ary relation between an agent, an organisation and a role, so it resembles `TeachingAssignment`. It cannot be reused because the second participant of our relation is a course offering, not an organisation.

**Dublin Core Terms.** Reuse for `dcterms:title` (course titles) and the ontology metadata. *Licence:* DCMI documents are licensed under CC BY 4.0, per the DCMI site. *Maintenance:* actively stewarded by DCMI. The terms are also published as ISO 15836-2:2019, and the specification page I consulted lists a 2020-01-20 release.

**SKOS.** Used only for annotation (`skos:definition`, `skos:scopeNote`, `skos:closeMatch`) and because `org:Role` is a `skos:Concept`. A W3C Recommendation (2009). *Licence:* not verified separately; W3C document rules apply.

**schema.org (align).** `schema:Course` and `schema:CourseInstance` correspond to our `Course` and `CourseOffering`, and `schema:CollegeOrUniversity` to `University`. Alignment is stated with `skos:closeMatch` annotations on our classes. Not reused because (1) schema.org does not give property domains and ranges as OWL axioms (it uses `domainIncludes`/`rangeIncludes`), so a reasoner cannot use it; (2) `schema:CourseInstance` has `instructor` but no way to carry a role or weekly hours per instructor, which our CQs need; (3) `schema:Course` is a `CreativeWork`, which makes a class hierarchy we do not want to inherit. *Licence:* I believe CC BY-SA 3.0 (share-alike), **not verified in this session**; this is another reason to align rather than copy terms into our file. *Maintenance:* actively developed; its pages show a development site and an issue tracker.

**AIISO (reject).** Describes faculties, departments and institutions. Rejected because: (1) its last version dates from 2008 (copyright Talis Information Ltd; version 2008-09-25), and the Linked Open Vocabularies entry describes it as unlikely to evolve; (2) the same registry noted in 2014 that the PURL redirection for its RDF file was broken, which is a risk for a dependency; (3) it overlaps ORG, and ORG already covers what we need (an open-organisation guide I found recommends ORG as the core with AIISO types layered on top); (4) *licence:* the RDF metadata names CC BY 2.0 UK, an old CC version. A future version could add a `skos:closeMatch` from `bpu:Department` to `aiiso:Department`.

**OWL-Time (reject).** The model needs only a start date and an end date per academic term. `time:Interval` would add classes and properties that no CQ uses. Revisit if terms need instants or intervals with Allen relations.

**Brazilian sources.** I did not evaluate a Brazilian ontology of higher education. INEP's *Censo da Educação Superior* and the e-MEC register are used only as informal data sources for the domain, and the fixtures remain synthetic.

## 5. Section 2.2: Design pattern

**Pattern: participation / n-ary relation (reified role assignment).**

**Modelling problem.** "Person X teaches offering Y" looks like one binary property, `teaches`. That cannot say in what role (lead lecturer, co-lecturer, teaching assistant) or for how many hours per week. Putting the role or the hours on the person or on the offering is wrong: a person has different roles and loads in different offerings, and an offering has many people. In OWL a binary property cannot carry attributes of the link itself. The fix is to turn the relationship into an object of its own.

**Implementation.**

| Part | Element |
|---|---|
| Reified relationship | class `bpu:TeachingAssignment` |
| Participant 1 (person) | `bpu:assignedPerson` (to `foaf:Person`), functional |
| Participant 2 (offering) | `bpu:assignedOffering` (to `bpu:CourseOffering`), functional |
| Role | `bpu:assignmentRole` (to `bpu:TeachingRole`, a subclass of `org:Role`), functional; role individuals `lead-lecturer-role`, `co-lecturer-role`, `teaching-assistant-role` |
| Attribute of the link | `bpu:weeklyHours`, `xsd:integer` restricted to 1 to 40 by a facet |

Related design choice: there is **no `Lecturer` class**. Lecturing is a role played in an assignment, not a kind of person. A `Lecturer ⊑ Person` subclass would mean a person who teaches only in one term is a different kind of thing from one who does not, and the same person would be lecturer in one offering and assistant in another. The role individuals carry that information instead.

**Second pattern (type/occurrence separation).** `Course` (catalogue entry) and `CourseOffering` (the course in one term) are separate classes linked by `ofCourse`, mirroring `schema:Course` and `schema:CourseInstance`. It solves the problem of one course being offered many times with different terms and different staff.

**Connection to competency questions.** CQ1, CQ5, CQ6, CQ8, CQ9 and CQ11 all need the role, the hours or both, and each is answerable only because the assignment is an individual that can be joined to its person, offering, role and hours. CQ6 (hours per lecturer) and CQ9 (more than one lecturer per offering) cannot be written with a plain `teaches` property.

## 6. Section 2.3: Design summary

Full axioms are in `ontology.ttl`; the evidence for each choice is in `evidence.md`.

- **Identifiers.** Ontology IRI `https://example.org/bpu`; version IRI `https://example.org/bpu/0.1.0` (placeholders).
- **Class hierarchy** (`rdfs:subClassOf` only for genuine is-a):
  - `University ⊑ org:FormalOrganization`, with `StateUniversity ⊑ University`.
  - `Department ⊑ org:OrganizationalUnit`.
  - `GovernmentBody ⊑ org:FormalOrganization`.
  - `TeachingRole ⊑ org:Role`.
  - `Course`, `CourseOffering`, `AcademicTerm` and `TeachingAssignment` are top-level classes.
  - Part-of (`org:subOrganizationOf`), participation (the assignment properties) and maintenance (`maintainedBy`) are properties, not subclasses.
- **Defined class.** `FederalUniversity ≡ University ⊓ ∃maintainedBy.{uniao-federal}`. UFSCar is typed only as `University` in `fixtures.ttl` and is classified by the reasoner.
- **Disjointness.** `FederalUniversity ⟂ StateUniversity`, because the data model records one maintaining sphere per university and the two result sets of CQ6 and CQ8 must not overlap. The main kinds of thing are also pairwise disjoint (`University`, `Department`, `GovernmentBody`, `Course`, `CourseOffering`, `AcademicTerm`, `TeachingAssignment`, `TeachingRole`).
- **Domains and ranges.** Every object and datatype property has a domain and a range. They are inference rules, not validation (see the `maintainedBy` case in `evidence.md`).
- **Facet constraint.** `weeklyHours` is an integer from 1 to 40.
- **Annotations.** Every local class and property has `rdfs:label` in `@en` and `@pt-BR` and an English `skos:definition`.
