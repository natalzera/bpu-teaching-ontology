#!/usr/bin/env bash
# Reproduce ontology reasoning and CQ checks.
# Usage: ROBOT_JAR=/path/to/robot.jar bash scripts/run_checks.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
ROBOT_JAR="${ROBOT_JAR:-$ROOT/robot.jar}"
if [[ ! -f "$ROBOT_JAR" ]]; then
  echo "ERROR: ROBOT jar not found: $ROBOT_JAR" >&2
  echo "Set ROBOT_JAR=/path/to/robot.jar" >&2
  exit 2
fi
robot() { java -jar "$ROBOT_JAR" "$@"; }
mkdir -p build
GEN="SubClass EquivalentClass ClassAssertion"

echo '== 1. Merge ontology + fixtures (asserted graph)'
robot merge --input ontology.ttl --input fixtures.ttl --output build/merged.ttl

echo '== 2. HermiT: consistency, unsatisfiable classes, inferred axioms'
robot reason --reasoner HermiT --input build/merged.ttl \
  --axiom-generators "$GEN" --include-indirect true \
  --exclude-tautologies structural --create-new-ontology false \
  --output build/inferred.ttl
echo 'HermiT completed successfully: consistent; no unsatisfiable classes reported.'

echo '== 3. CQs on asserted data (some inference-dependent CQs should fail)'
python3 scripts/run_cqs.py build/merged.ttl || true

echo '== 4. CQs on HermiT-inferred data (all must pass)'
python3 scripts/run_cqs.py build/inferred.ttl

echo '== 5. ELK cross-check (all CQs must pass)'
robot reason --reasoner ELK --input build/merged.ttl \
  --axiom-generators "$GEN" --include-indirect true \
  --exclude-tautologies structural --create-new-ontology false \
  --output build/elk.inferred.ttl
python3 scripts/run_cqs.py build/elk.inferred.ttl

echo '== 6. Negative tests must be inconsistent'
for t in neg-disjoint neg-weekly-hours; do
  if [[ "$t" == 'neg-disjoint' ]]; then base=ontology.ttl; else base=build/merged.ttl; fi
  robot merge --input "$base" --input "tests/$t.ttl" --output "build/$t.merged.ttl"
  if robot reason --reasoner HermiT --input "build/$t.merged.ttl" --output "build/$t.out.ttl" >"build/$t.log" 2>&1; then
    echo "ERROR: $t was expected to be inconsistent, but the reasoner accepted it." >&2
    exit 1
  else
    if grep -qi 'inconsistent' "build/$t.log"; then
      echo "$t: expected inconsistency confirmed"
    else
      echo "ERROR: $t failed for a reason other than a reported inconsistency; inspect build/$t.log" >&2
      cat "build/$t.log" >&2
      exit 1
    fi
  fi
done

echo '== 7. Domain-inference demonstration (must remain consistent; CQ2 gains an unintended row)'
robot merge --input build/merged.ttl --input tests/demo-domain-range.ttl --output build/demo.merged.ttl
robot reason --reasoner HermiT --input build/demo.merged.ttl \
  --axiom-generators "$GEN" --include-indirect true \
  --exclude-tautologies structural --create-new-ontology false \
  --output build/demo.inferred.ttl
python3 scripts/run_cqs.py build/demo.inferred.ttl > build/demo-cqs.log || true
grep '^cq02:' build/demo-cqs.log

echo '== All required reasoning checks completed.'
