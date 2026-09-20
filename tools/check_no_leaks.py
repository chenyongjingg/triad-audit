#!/usr/bin/env python3
"""Pre-commit identifier scan for the triad-audit repository.

WHY THIS EXISTS
---------------
The audited scoring stack is identified in the manuscript by structure and
never by name.  The thing that must not escape is therefore a STRING, not a
filename -- a stray mention in a docstring, a comment, a log excerpt pasted
into a README.

Two properties of git make this sharper than ordinary tidiness:

  * `.gitignore` filters by path and name.  It cannot read a file.
  * Git history is public in a way a working tree is not.  A string that
    reaches a commit stays reachable after the next commit removes it,
    because the earlier object remains in the pack.

So this runs BEFORE the commit, not after it.  A failure here means: fix the
file, do not relax the rule.

WHERE THE NEEDLES LIVE
----------------------
They are NOT hardcoded in this file, and that is deliberate.  An enforcement
mechanism that spells out the identifier it is protecting has leaked it --
once in the `.gitignore` pattern, once in this docstring.  The list lives in
`.leaks.local`, which is untracked:

    [content]
    <identifier one>
    <identifier two>

    [path]
    <filename fragment>

`tools/leaks.local.example` shows the shape.  If `.leaks.local` is absent the
scan **fails closed** with exit 2 rather than reporting a cheerful pass: an
enforcement mechanism that silently does nothing when unconfigured is worse
than no mechanism, because it manufactures confidence.

USAGE
-----
    python tools/check_no_leaks.py              # whole tree -- the pre-PUSH gate
    python tools/check_no_leaks.py --staged     # `git diff --cached` -- pre-COMMIT
    python tools/check_no_leaks.py --self-test  # prove the scanner can fail

Exit 0 clean, 1 violation, 2 setup error (including: unconfigured).

SCOPE, WHICH IS EASY TO GET WRONG
---------------------------------
`--staged` and the default mode are not interchangeable, and the difference
bites precisely when it matters.  `--staged` sees only what changed since
HEAD, so before a push it scans the files you just edited and stays blind to
everything committed earlier -- which is most of what is about to be
published.  A run that reported "1 file scanned, PASS" was mistaken for a
clean bill of health on an eleven-file release.

Use the default (whole tree) before publishing.  If in doubt, scan the
artifact rather than the tree: download what was actually published, as
tools/ is not the only thing that can be out of date.

Stdlib only, so this runs anywhere a commit can.
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
import tempfile

NEEDLE_FILE = ".leaks.local"

# Used only by --self-test.  Synthetic on purpose: it must match nothing real.
SELFTEST_NEEDLE = "zz-forbidden-token-demo-zz"

# Text-ish extensions worth reading.  Anything else is skipped rather than
# guessed at: the point is a reliable scan, not an exhaustive one.
TEXT_SUFFIXES = {
    ".md", ".txt", ".csv", ".tsv", ".json", ".yaml", ".yml", ".toml",
    ".py", ".sh", ".cff", ".cfg", ".ini", ".tex", ".bib", ".bst", ".cls",
    ".rst", ".html", ".xml",
}

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules",
             ".pytest_cache", "build", "dist"}

# Files that must contain the needles by construction.
#
# Only the needle file itself is exempt, and it has to be: it holds the list.
# It is untracked, so it cannot be committed anyway.
#
# This scanner is deliberately NOT exempt and does not exempt itself.  An
# earlier revision did, reasoning that a tool must contain the strings it
# looks for.  That was true when the list was hardcoded here; once the list
# moved to .leaks.local the exemption was vestigial -- and it immediately hid
# a real leak, the token spelled out in a docstring in this very file.  An
# exemption that outlives its reason is how a scan quietly stops scanning.
SELF_EXEMPT = {NEEDLE_FILE}


def parse_needle_file(path: pathlib.Path):
    """Parse the [content] / [path] sections.  Returns (content, paths)."""
    content, paths, section = [], [], "content"
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip().lower()
            continue
        (paths if section == "path" else content).append(line)
    return content, paths


def fold(s: str) -> str:
    """Case-fold for matching: the same token in any capitalisation is one leak.

    Do not write an example using a real identifier here.  This docstring is
    the file's own worst offender: an earlier revision illustrated the point
    with the actual token, twice, in the one file whose job is to catch it.
    A generic description makes the same point and cannot leak.
    """
    return s.lower()


def iter_files(root: pathlib.Path):
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def scan_text(p: pathlib.Path, root: pathlib.Path, needles):
    rel = p.relative_to(root).as_posix()
    if rel in SELF_EXEMPT:
        return []
    if p.suffix.lower() not in TEXT_SUFFIXES and p.name not in (
            ".gitignore", ".gitattributes"):
        return []
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    hits, folded = [], [(fold(n), n) for n in needles]
    for i, line in enumerate(text.splitlines(), 1):
        low = fold(line)
        for low_needle, needle in folded:
            if low_needle in low:
                hits.append((i, needle, line.strip()[:160]))
    return hits


def scan_paths(root: pathlib.Path, patterns):
    hits = []
    for p in iter_files(root):
        rel = p.relative_to(root).as_posix()
        low = fold(rel)
        for pat in patterns:
            if fold(pat) in low:
                hits.append(rel)
                break
    return hits


def staged_paths(root: pathlib.Path):
    """Paths git would add on the next commit.  None if not a repo."""
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            cwd=root, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return [line.strip() for line in out.stdout.splitlines() if line.strip()]


def run(root: pathlib.Path, staged: bool, needles, patterns) -> int:
    print("=" * 70)
    print("triad-audit leak scan")
    print("  root    : %s" % root)
    print("  mode    : %s" % ("staged only" if staged else "working tree"))
    print("  needles : %d content, %d path" % (len(needles), len(patterns)))
    print("=" * 70)

    limit = staged_paths(root) if staged else None
    if staged and limit is None:
        print("  not a git repository; falling back to the whole tree")
    elif limit is not None:
        print("  staged files: %d" % len(limit))

    content_violations, scanned = 0, 0
    for p in iter_files(root):
        rel = p.relative_to(root).as_posix()
        if limit is not None and rel not in limit:
            continue
        scanned += 1
        for lineno, needle, line in scan_text(p, root, needles):
            content_violations += 1
            print("  CONTENT %s:%d  %r" % (rel, lineno, needle))
            print("          %s" % line)

    path_violations = scan_paths(root, patterns)
    for rel in path_violations:
        print("  PATH    %s  (matches a withheld/forbidden name pattern)" % rel)

    print()
    print("  files scanned      : %d" % scanned)
    print("  content violations : %d" % content_violations)
    print("  path violations    : %d" % len(path_violations))
    total = content_violations + len(path_violations)
    print()
    if total:
        print("FAIL -- %d violation(s).  Fix the file; do not relax the rule."
              % total)
        return 1
    print("PASS -- clean.")
    return 0


def self_test() -> int:
    """Prove the scanner can fail.  A scanner that cannot fail is decoration."""
    print("=" * 70)
    print("self-test: plant a violation, assert the scanner catches it")
    print("=" * 70)
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        (root / "docs").mkdir()
        (root / "docs" / "innocent.md").write_text(
            "A line that names the audited stack: " + SELFTEST_NEEDLE + "\n",
            encoding="utf-8")
        rc = run(root, staged=False, needles=[SELFTEST_NEEDLE],
                 patterns=["zz-withheld-demo-zz"])
    print()
    if rc == 1:
        print("SELF-TEST PASS -- the scanner detected the planted violation.")
        return 0
    print("SELF-TEST FAIL -- the scanner did NOT detect a planted violation.")
    print("The scan is not doing what it claims; treat the tree as unscanned.")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".", help="repository root (default: .)")
    ap.add_argument("--staged", action="store_true",
                    help="scan only files staged for commit")
    ap.add_argument("--self-test", action="store_true",
                    help="verify the scanner can detect a planted violation")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    root = pathlib.Path(args.root).resolve()
    if not root.is_dir():
        print("error: not a directory: %s" % root, file=sys.stderr)
        return 2

    nf = root / NEEDLE_FILE
    if not nf.exists():
        print("error: %s not found in %s" % (NEEDLE_FILE, root), file=sys.stderr)
        print()
        print("The scan did NOT run.  Do not read this as a pass.")
        print("Copy tools/leaks.local.example to %s and fill it in." % NEEDLE_FILE)
        print("This failure is deliberate: a scan that reports success while")
        print("unconfigured manufactures confidence rather than providing it.")
        return 2

    needles, patterns = parse_needle_file(nf)
    if not needles and not patterns:
        print("error: %s lists no needles; nothing would be checked."
              % NEEDLE_FILE, file=sys.stderr)
        return 2
    return run(root, args.staged, needles, patterns)


if __name__ == "__main__":
    sys.exit(main())
