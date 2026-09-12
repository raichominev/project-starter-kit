#!/usr/bin/env python3
"""Report artefacts that are meant to be invoked and that nothing references.

An orphan has in-degree zero in the repository's reference graph: no document,
no index, no other file names it. The session that built it is the one that
cannot see it, so this runs at a checkpoint — a session close — and not during
the work.

    python orphan_sweep.py <root> [--exclude GLOB]... [--by-dir] [--quiet]

Exit code 1 when it finds an orphan, so a CI step or a hook can gate on it.

It is deliberately biased to UNDER-report. A reference is any mention of the
artefact's file name in any other text file, which is crude and will call some
real orphans "referenced". That is the safer error: a check that cries wolf is
a check nobody runs.

Vendored trees, virtualenvs and git worktrees are pruned, because every file in
them looks like an orphan and none of them is one. Virtualenvs are found by
their `pyvenv.cfg`, and worktrees by `.git` being a file rather than a
directory. Anything else a project vendors needs `--exclude`; run `--by-dir`
first to see where the noise is concentrated.
"""

import argparse
import fnmatch
import os
import sys
import urllib.parse
from collections import Counter
from pathlib import Path

SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__", "venv", ".venv",
    "env", "dist", "build", "vendor", "site-packages", ".tox", ".mypy_cache",
    ".pytest_cache", ".idea", ".vscode", "target", "worktrees",
}

SCRIPT_SUFFIXES = {".sh", ".ps1", ".bat", ".cmd"}
TEXT_SUFFIXES = {
    ".md", ".txt", ".rst", ".py", ".sh", ".ps1", ".bat", ".cmd", ".yml",
    ".yaml", ".json", ".toml", ".ini", ".cfg", ".tsv", ".csv", ".js", ".ts",
    ".tsx", ".jsx", ".php", ".rb", ".go", ".rs", ".java", ".xml", ".html",
}
NO_SUFFIX_TEXT = {"Makefile", "makefile", "Dockerfile", "Justfile", "justfile"}

MAX_READ_BYTES = 2_000_000


def is_pruned_tree(dirpath, names):
    """A virtualenv or a git worktree. Every file inside looks orphaned."""
    if "pyvenv.cfg" in names:
        return True
    return ".git" in names and os.path.isfile(os.path.join(dirpath, ".git"))


def walk(root, excludes):
    for dirpath, dirnames, filenames in os.walk(root):
        if is_pruned_tree(dirpath, set(dirnames) | set(filenames)):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            path = Path(dirpath) / name
            rel = path.relative_to(root).as_posix()
            if any(fnmatch.fnmatch(rel, pat) for pat in excludes):
                continue
            yield path


def read(path):
    try:
        if path.stat().st_size > MAX_READ_BYTES:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def has_entry_point(path, text):
    if path.suffix in SCRIPT_SUFFIXES:
        return True
    if path.suffix != ".py":
        return False
    return "__main__" in text or "argparse" in text or "sys.argv" in text


def is_text(path):
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in NO_SUFFIX_TEXT


def sweep(root, excludes):
    files = list(walk(root, excludes))
    texts = {}
    for path in files:
        if is_text(path):
            texts[path] = read(path)

    owners = {}
    for path in files:
        if has_entry_point(path, texts.get(path, "")):
            owners.setdefault(path.name, set()).add(path)

    # Markdown escapes a space as %20, so a link to "my tool.py" never matches
    # a plain search for the file name. Both forms are searched.
    forms = {n: (n, urllib.parse.quote(n)) for n in owners}

    referenced = set()
    for path, text in texts.items():
        if not text:
            continue
        for name, (plain, quoted) in forms.items():
            if plain in text or quoted in text:
                referenced.update(o for o in owners[name] if o != path)

    candidates = [p for group in owners.values() for p in group]
    orphans = sorted(p for p in candidates if p not in referenced)
    return files, candidates, orphans


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", type=Path)
    ap.add_argument("--exclude", action="append", default=[], metavar="GLOB",
                    help="repo-relative glob to skip; repeatable")
    ap.add_argument("--by-dir", action="store_true",
                    help="summarise orphans per directory instead of listing them")
    ap.add_argument("--quiet", action="store_true", help="print only the orphans")
    args = ap.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        ap.error(f"not a directory: {root}")

    files, candidates, orphans = sweep(root, args.exclude)

    if not args.quiet:
        print(f"scanned {len(files)} files under {root}")
        print(f"invocable artefacts: {len(candidates)}  "
              f"referenced: {len(candidates) - len(orphans)}  "
              f"orphans: {len(orphans)}")
        print()

    if not orphans:
        if not args.quiet:
            print("No orphans. Every invocable artefact is named somewhere.")
        return 0

    if args.by_dir:
        tally = Counter(
            str(Path(p.relative_to(root)).parent) for p in orphans
        )
        print("ORPHANS per directory - use --exclude on the vendored ones:")
        for directory, count in tally.most_common():
            print(f"  {count:5d}  {directory}")
    else:
        print("ORPHANS - nothing in this repository names these:")
        for path in orphans:
            print(f"  {path.relative_to(root).as_posix()}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
