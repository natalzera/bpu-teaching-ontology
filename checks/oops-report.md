# OOPS! ontology pitfall scan — status and follow-up

**Status: NOT RUN.** The OOPS! web service could not be reached from the environment used to prepare this archive (network name resolution was unavailable). No findings are fabricated, and this file is not an OOPS! report.

## Required before final submission

1. Open the OOPS! ontology pitfall scanner: <https://oops.linkeddata.es/>.
2. Submit `ontology.ttl` (or a publicly reachable ontology IRI after replacing the current `example.org` placeholder).
3. Save the complete generated report or dated screenshots in this `checks/` directory.
4. Update this file with the scan date, ontology submitted, all critical issues (typically P1), and the fix or reasoned disposition for each. Include lower-priority findings if useful.

## Manual issues already known

- The ontology IRI and version IRI use `example.org` placeholders. Replace them with stable identifiers controlled by the project owner before release.
- `checks/profile-validation-2026-10-13.log` records a ROBOT OWL 2 DL profile validation failure around `xsd:date` values and datatype restrictions. Investigate and rerun that check.
- `ontology.ttl` contains a local minimal extract of external vocabulary terms. `requirements.md` documents provenance and reuse choices; verify that the extracts and licensing attributions remain appropriate before publishing.

These are manual review notes, not OOPS! findings.
