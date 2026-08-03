# REPORT.md

## 1. Control flow graph of `to_roman`

Source: `src/roman/converter.py`, `to_roman(n)`, lines 40-53 (after the unit-level fix that
corrected the `(5, "IV")` entry to `(4, "IV")` in `_PAIRS`).

Basic blocks:

| Node   | Statement                                              | Line(s) |
|--------|---------------------------------------------------------|---------|
| N1     | `if not isinstance(n, int) or isinstance(n, bool):`      | 41      |
| N2     | `raise RomanError("value must be an integer")`           | 42      |
| N3     | `if n < _MIN_VALUE:`                                     | 43      |
| N4     | `raise RomanError("value must be >= 1")`                 | 44      |
| N5     | `if n > _MAX_VALUE:`                                     | 45      |
| N6     | `raise RomanError("value must be <= 3999")`              | 46      |
| N7     | `out = []` ; `remaining = n`                             | 47-48   |
| N8     | `for value, symbol in _PAIRS:`                           | 49      |
| N9     | `while remaining >= value:`                              | 50      |
| N10    | `out.append(symbol)` ; `remaining -= value`               | 51-52   |
| N11    | `return "".join(out)`                                    | 53      |
| EXIT   | single sink (all `raise` and the `return` converge here) | -       |

### Graph (ASCII)

```
                +------------------------------+
                |             N1               |
                |  not isinstance | isinstance  |
                |     (n, int)    |  (n, bool)  |
                +------------------------------+
                   T |                    | F
                     v                    v
                  +------+           +----------+
                  |  N2  |           |    N3    |
                  |raise |           | n < MIN? |
                  +--+---+           +----+-----+
                     |               T |    | F
                     |                 v    v
                     |            +------+  +----------+
                     |            |  N4  |  |    N5    |
                     |            |raise |  | n > MAX? |
                     |            +--+---+  +----+-----+
                     |               |     T |     | F
                     |               |       v     v
                     |               |    +------+ +--------+
                     |               |    |  N6  | |   N7   |
                     |               |    |raise | | out=[] |
                     |               |    +--+---+ |remain=n|
                     |               |       |      +---+----+
                     |               |       |          |
                     |               |       |          v
                     |               |       |     +----------+
                     |               |       |  +->|    N8    |<-------+
                     |               |       |  |  | for pair |        |
                     |               |       |  |  +----+-----+        |
                     |               |       |  |   more| no more      |
                     |               |       |  |  pairs|  pairs       |
                     |               |       |  |       v              |
                     |               |       |  |  +----------+        |
                     |               |       |  +--| N9 while |        |
                     |               |       |     |remain>=v |        |
                     |               |       |     +----+-----+        |
                     |               |       |    T |     | F          |
                     |               |       |      v     +-----------+
                     |               |       |  +------+
                     |               |       |  | N10  |
                     |               |       |  |append|
                     |               |       |  |remain|
                     |               |       |  |-=val |
                     |               |       |  +--+---+
                     |               |       |     |
                     |               |       |     +---> (back to N9)
                     |               |       |
                     |               |       |          loop exhausted
                     |               |       |               |
                     |               |       |               v
                     |               |       |          +--------+
                     |               |       |          |  N11   |
                     |               |       |          | return |
                     |               |       |          +---+----+
                     v               v       v              v
                  +-----------------------------------------+
                  |                  EXIT                    |
                  +-----------------------------------------+
```

### Nodes and edges

N = 12 (N1..N11 + EXIT)

Edges (E = 16):

1. N1 → N2 (T)
2. N1 → N3 (F)
3. N2 → EXIT
4. N3 → N4 (T)
5. N3 → N5 (F)
6. N4 → EXIT
7. N5 → N6 (T)
8. N5 → N7 (F)
9. N6 → EXIT
10. N7 → N8
11. N8 → N9 (more pairs)
12. N8 → N11 (no more pairs)
13. N9 → N10 (T)
14. N9 → N8 (F, back to outer for-loop)
15. N10 → N9 (back-edge, same pair)
16. N11 → EXIT

### Cyclomatic complexity V(G)

```
V(G) = E - N + 2 = 16 - 12 + 2 = 6
```

Cross-check with the predicate-count formula: predicate nodes are N1, N3, N5, N8, N9 (5 decision
points), and `V(G) = predicates + 1 = 5 + 1 = 6`. Both methods agree: **V(G) = 6**.

### Basis set of paths

Six linearly independent paths (baseline + one flipped decision per path), chosen to match
meaningful test scenarios rather than an arbitrary traversal order:

| # | Path (edges) | Scenario | Feasible? |
|---|---|---|---|
| 1 | N1(T) → EXIT | `n` is not an `int` (or is a `bool`) | yes — `to_roman("x")`, `to_roman(True)` |
| 2 | N1(F) → N3(T) → EXIT | `n < 1` | yes — `to_roman(0)` |
| 3 | N1(F) → N3(F) → N5(T) → EXIT | `n > 3999` | yes — `to_roman(4000)` |
| 4 | N1(F) → N3(F) → N5(F) → N7 → [N8 → N9(F)]×13 → N11 → EXIT | every pair rejected, loop body never runs | **no** — for any `n` in `1..3999`, the `(1, "I")` pair always satisfies `remaining >= value` at least once, so N9 is always taken True at least once before the for-loop can finish |
| 5 | N1(F) → N3(F) → N5(F) → N7 → N8 → N9(T) → N10 → N9(F) → N8 → ... → N11 → EXIT | a value that enters a `while` body exactly once per matching pair (e.g. `n=1`, only `(1,"I")` matches, once) | yes — `to_roman(1) == "I"` |
| 6 | N1(F) → N3(F) → N5(F) → N7 → N8 → N9(T) → N10 → N9(T) → N10 → N9(T) → N10 → N9(F) → N8 → ... → N11 → EXIT | the `N10 → N9` back-edge is taken more than once for the same pair (e.g. `n=3`, `(1,"I")` matches three times) | yes — `to_roman(3) == "III"` |

Path 4 is a structurally valid independent path in the graph but is **data-infeasible**: the graph
alone cannot express the invariant that `_PAIRS` always contains `(1, "I")` and every `n >= 1` must
consume at least one `"I"`-equivalent unit somewhere. This is expected — basis-path analysis
guarantees graph coverage, not test-data feasibility; the true test suite substitutes path 4 with
whichever feasible path is closest to it in decision content.

### Definition-use table

`c-use` = computational use (value is used in an expression/assignment). `p-use` = predicate use
(value is used in a branch condition).

| Variable | Defined at | Used at | Use type |
|---|---|---|---|
| `n` (parameter) | N1 (function entry) | N1, N3, N5 | p-use |
| `n` (parameter) | N1 (function entry) | N7 (`remaining = n`) | c-use |
| `remaining` | N7 (`remaining = n`) | N9 (`remaining >= value`) | p-use |
| `remaining` | N7, then redefined at N10 each iteration | N10 (`remaining -= value`) | c-use (and redefinition) |
| `value` | N8 (for-loop unpack, redefined every outer iteration) | N9 (`remaining >= value`) | p-use |
| `value` | N8 | N10 (`remaining -= value`) | c-use |
| `symbol` | N8 (for-loop unpack) | N10 (`out.append(symbol)`) | c-use |
| `out` | N7 (`out = []`) | N10 (`out.append(symbol)`) | c-use |
| `out` | N7 | N11 (`"".join(out)`) | c-use |

## 2. Integration finding

`add_roman` and `subtract_roman` (`src/roman/converter.py:109-114`) are pure integration points per
spec section 7: each is one line that composes `from_roman`, an arithmetic operator, and `to_roman`.
Neither function has logic of its own — its correctness depends entirely on the two units it wires
together being correct **for the specific values that composition produces**.

**Defect found:** `to_roman(4)` returned `"IIII"` instead of `"IV"`. The cause was a data error in the
`_PAIRS` table (`src/roman/converter.py:16-17`): it contained the value `5` twice —
`(5, "V")` followed by `(5, "IV")` — instead of `(5, "V")` followed by `(4, "IV")`. Since the greedy
loop in `to_roman` only appends `"IV"` when `remaining >= 4`, and the table never listed the value 4,
that branch could never be taken; `to_roman(4)` fell through to the `(1, "I")` pair and repeated it
four times.

This surfaced through `add_roman("II", "II")`: `from_roman("II")` correctly returns `2` for each
operand (unit-correct), `2 + 2 = 4` (correct arithmetic), but `to_roman(4)` — called only as a
consequence of *this specific composition* — returned `"IIII"`. The mandatory example in
SPECIFICATION.md section 7, `add_roman("II", "II") == "IV"`, failed.

**Why the unit tests of `to_roman` and `from_roman` alone did not detect it:** branch coverage
measures which *lines/branches* executed, not which *input values* passed through them. The 15
inherited unit tests and the ones added for `to_roman` in Part 3 exercised `n` = 1, 2, 3, 5, 10, 50,
100, 500, 1000, 3999, plus the invalid cases (non-int, bool, 0, 4000) — every one of those already
reached 100% branch coverage of `to_roman` without ever calling `to_roman(4)`. The while-loop body at
N10 (see section 1) is the same line regardless of which pair from `_PAIRS` is being matched, so a
coverage tool reports it "covered" the moment *any* pair triggers it — it cannot tell you that the
specific `(4, "IV")` row was never reachable. The bug was a **data defect** (a wrong tuple in a lookup
table), not a missing branch, so no amount of statement or branch coverage of `to_roman` in isolation
could have found it. It only became visible once a *composition* (`add_roman`) produced the exact
input value that the missing table row was responsible for.

The fix — correcting `(5, "IV")` to `(4, "IV")` in `_PAIRS` — was committed as
`fix: correct value for IV in _PAIRS and add tests for add_roman and subtract_roman functions`
(`78f4276`), before the formal integration tests in `tests/test_integration.py` were written. As a
result, those two tests (`test_add_roman_result_accepted_by_is_valid_roman`,
`test_subtract_roman_result_accepted_by_is_valid_roman`) pass today — they document and lock in the
composition contract (result must round-trip through `is_valid_roman`) rather than re-discover the
already-fixed defect.

## 3. Acceptance criteria

Three criteria in Given/When/Then form, each traced to a specific rule in SPECIFICATION.md, implemented
in `tests/test_acceptance.py`. They were written and run **after** the unit suite was green and branch
coverage of `src/roman/converter.py` already stood at 100% (see section 4).

**Criterion 1 — whitespace trimming (spec section 3):**
> Given a roman numeral string surrounded by leading and trailing blank spaces,
> When `from_roman` is called with that string,
> Then it returns the numeral's value, because "leading and trailing whitespace is tolerated".

Test: `test_from_roman_trims_surrounding_whitespace` — `from_roman("  IV  ") == 4`.

**Criterion 2 — canonical form validation (spec section 4):**
> Given `"IIII"`, which represents the value 4 but is not written in canonical form,
> When `is_valid_roman` is called with that string,
> Then it returns `False`, because "the canonical form of 4 is IV".

Test: `test_is_valid_roman_rejects_non_canonical_form` — `is_valid_roman("IIII") is False`.

**Criterion 3 — total input safety (spec section 6):**
> Given an input that is not a string, for example `None`,
> When `is_valid_roman` is called with that input,
> Then it returns `False` without raising any exception, because "it never raises, for any type of
> input".

Test: `test_is_valid_roman_never_raises_on_non_string` — `is_valid_roman(None) is False`.

### Results against the code that already reported 100% branch coverage

| Criterion | Result | Defect |
|---|---|---|
| 1 — whitespace trimming | **FAILED** | `from_roman` did `text = s.upper()` with no `.strip()`; any leading/trailing space was treated as an invalid character and raised `RomanError` instead of being ignored. |
| 2 — canonical form | **FAILED** | `from_roman`/`is_valid_roman` accepted any string that summed to a value in range, with no check that the string was the canonical spelling of that value; `is_valid_roman("IIII")` returned `True`. |
| 3 — non-string safety | PASSED | `is_valid_roman` already wrapped `from_roman` in `try/except RomanError`, and `from_roman` already raised `RomanError` (not some other exception) for non-`str` input. |

### Why coverage could not reveal this

Both failing criteria are **missing-behaviour defects**, not unreached-branch defects. Coverage — even
at 100% branch coverage, which this codebase already had before these tests were written — can only
tell you that every line and every branch *that exists in the code* was executed by some test. It
cannot tell you that a line the specification requires was never written at all. `from_roman` never
contained a `.strip()` call, so there was no branch to miss: the "trim whitespace" behaviour simply
did not exist anywhere in the control-flow graph for coverage to report on. Likewise there was no
canonical-form check to execute or skip — the five rules of spec section 4 were never encoded, so no
test, however thorough at the unit level, could drive coverage of logic that is absent. Acceptance
tests catch this class of defect precisely because they are derived from the specification
independently of the implementation, rather than from reading the code and exercising its existing
paths.
