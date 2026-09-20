# triad-audit

**TRIAD** — a three-layer *Response Integrity Audit for Deployability*: a procedure for asking whether a guardrail's reported operating point is produced by the evaluation apparatus rather than by the guardrail.

This repository accompanies the manuscript *Auditing the Deployability Boundary: Is a Guardrail's Reported Operating Point Produced by the Evaluation Apparatus?* It holds the audit checklist and the procedure in a form that can be run on a pipeline other than the one audited in the paper.

> **Status: scaffold only.** The checklist, the procedure and the recorded numbers below are transcribed from the manuscript. The executable code that produced them is **not yet released** — see [What is not here](#what-is-not-here). Nothing in this repository runs yet.

---

## TRIAD in one paragraph

TRIAD is an **audit procedure, not a detector**. It does not score a defence, rank it, or compare it to another defence; it reports how much of a reported number survives when the apparatus that produced it is examined. Three layers, each with the question it asks:

| Layer | Question | Section |
|---|---|---|
| **I — Response integrity** | Does a component of the response actually change the output? | §5 |
| **II — Boundary stability** | Does the reported boundary characterise the threat, or the audited object? | §6 |
| **III — Accounting integrity** | Do the counts correspond to distinct content, and where did the difference go? | §7 |

The layers **compose by cancellation, not by aggregation** — a clean reading at one layer does not offset a finding at another, and the layers are not summed into a score.

Each check returns one of three verdicts:

- **`clean`** — the check passes on its anchor and on every orthogonal dimension tested.
- **`blind`** — the check passes on its anchor and fails, or would fail, on an orthogonal dimension. The action is to disclose and add the orthogonal check.
- **`untraceable`** — a silent discard path exists and the difference cannot be reconstructed from the artifacts. The action is to disclose and add a trace.

---

## The checklist

Seven checks, transcribed from Table 2 of the manuscript. The middle pair is the content: **what a check anchors on** and **what it cannot see**.

| L | Audit question | Conventional check (anchor dimension) | Blind dimension | Instance in this work | Prescription |
|---|---|---|---|---|---|
| I | Does a component actually change the output? | structural reading: the component exists and its feature specification is non-empty (**existence**) | *activity of the input*: existing is not the same as varying | a branch declares zero features and still occupies a slot; a fixed quantity zeroes two of three terms | run a finite difference ∂ŷ/∂(branch input) per component; never substitute "the component is present" |
| I | the same | finite differences under a per-branch perturbation (**unit-level**) | *the evaluation path*: the perturbation must propagate through the arguments the evaluation actually passes | no call site passes the audio input, so all nine acoustic features fill with a constant | apply the perturbation **at the evaluation entry point**; a unit test with complete arguments does not substitute |
| II | Does the boundary characterise the threat or the audited object? | reproduce across configurations and see whether the boundary moves (**configuration**) | *single-variable*: two factors moved at once cannot be attributed | a 2×2 over model and calibration prior; one pair changes only the prior | flip one factor at a time and **report the quantities held fixed** (here: the fixed-threshold reading is identical to the digit) |
| II | the same | order perturbation: replay under different arrival orders (**order**) | *composition of the denominator*: a pooled rate is not comparable across different segment mixes | a framed share of 69.6% against 48.6% inflates a pooled ratio | normalise within segment for any cross-pool comparison, and report the composition and the dropped counts alongside |
| III | Do the counts correspond to distinct content? | threshold-style completeness: whether the count meets its target (**count**) | *content and de-duplication*: meeting the row target is not the same as distinct texts | 300 rows are 30 texts repeated ten times, so held-out text overlap is 28/28 | everywhere a set is declared, report the row count **and** the distinct-text count as two separate numbers |
| III | Where did the difference go? | reconciliation of declared against evaluated counts (**count**) | *trace of the discarding action*: a silent `continue` leaves no trace | 1050 → 560 (loss 490); 2800 → 2607 (loss 193) | every silent discard path (`continue`, `except: return`, an `if` guard on a field) must leave a trace with a reason and a count |
| III | Has a known fact taken effect? | recording: whether the structural fact was written into an artifact or a comment (**record**) | *propagation into the invariant*: recorded is not the same as used to constrain the design | a tenfold repetition structure was recorded twice and never reached the held-out construction | a recorded fact must be bound to the invariant it constrains; a note in the margin is not in effect |

A machine-readable copy is at [`checklist/checklist.csv`](checklist/checklist.csv).

---

## How to run it

The checklist is executable in six steps — three about collecting numbers, three about interrogating them.

1. **Enumerate the declared quantities.** List every declared count at every stage boundary: artifact fields, log lines, progress-bar totals.
2. **For each, obtain the evaluated quantity.** Not the number written in the artifact, but the number of rows that actually enter the next stage's computation. A mismatch is a candidate defect.
3. **For each mismatch, locate the discard point and check for a trace.** Search the code for the three silent forms: `continue`, `except: return False/None`, and a truthiness guard on a field.
   > A defect is a discard with no trace, **whatever its size**: detection is a question about the record, and size does not enter it. Materiality is a separate question, and the audit keeps the two apart rather than folding them together.
4. **For each threshold-style check, ask what its blind dimension is.** If the check asks whether there are enough rows, change to an orthogonal dimension: content (distinct texts), stratification (per-subgroup denominators), or composition (segment mix). If the result is unchanged under the new dimension, that dimension is not the defect surface; if it changes, the check passed on its anchor and is blind on the dimension that moved.
5. **For each known fact, ask whether it is bound to an invariant.** Count its appearances in artifacts, comments and notes, then look for its use in the construction code. Recorded and unused is equivalent to undiscovered.
6. **For each quantity held fixed, ask whether the comparison is single-variable.** List every factor that was constant; if two or more moved, the comparison cannot be attributed. Report the fixed quantities, because their being fixed is what licenses the attribution.

---

## Numbers recorded in the manuscript

These are the audit's findings on the case study. They are reproduced here as a **transcription of the paper**, not as output of any code in this repository.

| Finding | Value |
|---|---|
| In-segment FPR movement when the calibrator's initial quantile is flipped | 1.48× → 4.65× |
| Fixed-threshold reading under the same flip | bit-identical |
| In-segment FPR movement when the evaluated model is changed | 3.52× |
| Fixed-threshold reading under the same change | 3.3% |
| Fresh out-of-sample benign corpus — online calibration | 0.0 |
| Fresh out-of-sample benign corpus — fixed threshold | 0.5805 |
| Decisions reproduced by a single length cut | 94.49%, over a plateau of cut values |
| Input channels with identically zero finite differences at the probed base point | three |
| Threshold-crossing length, punctuation density varied | 934 → 1137 characters |
| Accounting losses reconstructed from artifacts | 490 rows, 193 rows, and a 28/28 content overlap |

---

## What is not here

This is a **partial** release, and the omissions are deliberate rather than pending.

**Withheld artifacts.** The manuscript's Appendix A lists two artifacts that are withheld: a frozen scoring stack (serialised) and a branch structure and response surface. They are published **by size and digest only**. *Withheld means not published; it does not mean that no such file exists.* See [`docs/withheld-artifacts.md`](docs/withheld-artifacts.md).

**Never in this repository.** The audited scoring stack is identified in the paper by structure, not by name. This repository does not name it, and `.gitignore` plus [`tools/check_no_leaks.py`](tools/check_no_leaks.py) enforce that mechanically. The enforcement runs before a commit, not after.

**Not yet released.** The scripts that produced the numbers above, and the environment pinning that would let a third party re-run them. Until they land, the numbers above are a reading of the paper.

**Not claimed.** No second party has reproduced any number in this paper. The audit reported in the manuscript was designed and executed by the authors of the audited stack: it is a **first-party, read-only audit of artifacts frozen before the audit began**, and it does not satisfy the independence condition that the auditing framework cited in the manuscript's §2 treats as load-bearing.

---

## Repository layout

```
checklist/    the seven checks, machine-readable
docs/         scope, withheld artifacts, repository listing metadata
tools/        check_no_leaks.py — pre-commit identifier scan
```

---

## Citing

See [`CITATION.cff`](CITATION.cff).

---

## License

MIT — see [`LICENSE`](LICENSE).
