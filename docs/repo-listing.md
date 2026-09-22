# Repository listing metadata

The text a hosting platform asks for when the repository is published — kept here rather than typed into a web form, so that it is version-controlled and reviewable like everything else. A description that only exists in a web form cannot be diffed, and cannot be checked against the discipline the rest of the repository follows.

---

## Description

### Primary (recommended)

```
TRIAD: a three-layer response integrity audit for deployability. It asks
whether a guardrail's reported operating point is produced by the evaluation
apparatus rather than by the guardrail. Companion repository to an unpublished
manuscript. Scaffold release -- the checklist and the procedure; the audited
stack is withheld.
```

As a single line, for pasting:

```
TRIAD: a three-layer response integrity audit for deployability — is a guardrail's reported operating point produced by the evaluation apparatus, rather than by the guardrail?  Companion repo to an unpublished manuscript. Scaffold release: checklist and procedure; the audited stack is withheld.
```

**Character count:** 295 (measured, not estimated). GitHub's field accepts more than this, but the listing truncates well before the limit, so the first sentence is written to stand alone.

### Short alternative

```
Is a guardrail's reported operating point produced by the evaluation apparatus?  TRIAD — a three-layer response integrity audit. Scaffold release.
```

**Character count:** 146 (measured). Use this if the description will be displayed in a narrow column.

### Sentence-by-sentence rationale

| Sentence | Why it is there |
|---|---|
| "TRIAD: a three-layer response integrity audit for deployability." | Names the artefact and expands the acronym. A reader who sees only this line still knows what the repository is. |
| "It asks whether a guardrail's reported operating point is produced by the evaluation apparatus rather than by the guardrail." | The actual contribution, in the paper's own framing. This is the sentence that makes the repository findable by someone with the problem rather than the keyword. |
| "Companion repository to an unpublished manuscript." | Provenance. A reader needs to know a paper exists and where the claims are argued in full. It names no venue, deliberately: the intended journal can change before publication, and a description that pins one either goes stale or sends a reader to a venue the paper never reached. |
| "Scaffold release -- the checklist and the procedure; the audited stack is withheld." | The honest status line. Without it the description implies a completeness the repository does not have. |

### What the description deliberately does not say

- **No "state-of-the-art", no "superior to", no "outperforms".** TRIAD is an audit procedure, not a detector, so a comparison to another method would be a category error and would contradict the manuscript. The same discipline governs `README.md` and `docs/scope.md`.
- **No journal name, and no submission status.** The intended venue can change before publication. A description that pins one either goes stale or misdirects, and a reader who follows it learns something that was never true.
- **No name for the audited stack.** It is identified by structure, never by name — see `docs/scope.md` and `.gitignore` section 2.
- **No "reproducible" or "fully open".** The code is not released yet, and two artifacts are withheld. Claiming reproducibility here would be the exact failure the paper is written about.

---

## Topics

Platform topic tags, in the order they should be entered. Lowercase and hyphenated, as those fields require.

```
audit
evaluation-validity
measurement
reproducibility
guardrails
machine-learning
ai-safety
research-software
checklist
```

A note on ordering: these are entered in priority order, because a platform that silently drops the excess keeps the first ones. `audit`, `evaluation-validity` and `measurement` are the ones that describe what this is; `machine-learning` and `ai-safety` are there for reach and are placed after, so that a truncation costs reach rather than accuracy.

---

## Other one-line uses

**Companion-paper footnote, or the "Code availability" line of a manuscript:**

```
The TRIAD checklist and procedure are available at https://github.com/chenyongjingg/triad-audit.
```

**In a Zenodo or archive deposit description**, the same primary text is used unchanged, so that the repository and the deposit do not drift apart in the record.

---

## Placeholder resolved

The `OWNER` token that stood in `CITATION.cff` and in the footnote above has been replaced with the actual account, `chenyongjingg`. It was left as a visible token rather than a plausible-looking guess for the reason given below, and this section is kept rather than deleted so the resolution is on the record.

Every field is now filled:

| Field | Value | Source |
|---|---|---|
| License | MIT | settled by the authors |
| Copyright holder | Yongjin Chen, Ziying Xue, Songze Zhu | `main.tex` `\author` |
| Repository name | `triad-audit` | settled by the authors |
| Repository owner | `chenyongjingg` | the hosting account, supplied by the authors |
| Version | `0.1.0-scaffold` | this release |

**Why the token was not guessed.** A hosting account name cannot be derived from the manuscript, so it was recorded as a visible token instead of an invented one. A broken `repository-code` fails silently in most viewers, which is how a placeholder reaches production; a token that is obvious in a diff does not. The distinction is not stylistic — one is detectable, the other is not.
