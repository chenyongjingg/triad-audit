# Withheld artifacts

The manuscript's Appendix A lists two artifacts that are **withheld**. This file records that decision and what it does and does not mean.

## What is withheld

| Artifact | Status | Size | Digest |
|---|---|---|---|
| frozen scoring stack (serialised) | *withheld* | 212717 B | `2db0c9f622f79fb0` |
| branch structure and response surface | *withheld* | 12.2 KB | `6f7449ec02af1f19` |

These are the only two entries in Appendix A with that status.

## What "withheld" means

> Withheld means **not published**; it does **not** mean that no such file exists.

This sentence is the whole point of listing them. An artifact that is absent and an artifact that is withheld are different claims, and a reader is entitled to know which one is being made. Publishing the size and the digest — without the artifact — lets a holder of a candidate file confirm or refute possession, while leaving the file itself undistributed.

The digest is therefore not a tease. It is the minimum disclosure that makes the withholding a checkable statement rather than an assertion of absence.

## Why these two

Both carry material that identifies the audited scoring stack at a level of detail the manuscript deliberately does not publish. The manuscript identifies the audited stack **by structure, never by name**; a serialised scoring stack and a branch structure with its response surface would each undo that in one file.

The audit itself does not depend on a reader having them. Every number in the manuscript is reported as a value, and the accounting losses are reconstructed from counts that are stated in the paper. Withholding the artifacts bounds what a reader can re-derive independently — it does not change any reported result.

## What a reader can and cannot do

**Can.** Read the checklist, run the procedure on their own pipeline, compare the seven blind dimensions against their own checks, and check the reported numbers against the stated counts.

**Cannot.** Re-run the audited stack, verify the digest by recomputation, or reproduce the response surface from this repository.

This asymmetry is disclosed rather than papered over. It is part of why the manuscript states that no second party has reproduced any number in it.

## Handling

These artifacts are **excluded from this repository** by `.gitignore`, both by name pattern and by serialisation type. See the header of that file for the reasoning, and note its central limitation: `.gitignore` matches paths and names only, so it cannot see a withheld artifact's content pasted into a document. That job belongs to `tools/check_no_leaks.py`.

If a withheld artifact is ever released, it will be a deliberate decision recorded here, with the digest and the reasoning, and not an accident of a commit.
