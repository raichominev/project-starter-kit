Set up this project's `CLAUDE.md` from [CLAUDE.template.md](CLAUDE.template.md), which sits beside this file. Do not write anything until step 4 — steps 1-3 are read-only.

## 1. Inventory what already exists

Look for existing agent instructions before assuming a blank slate: `CLAUDE.md` (root and any nested), `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`, `CONTRIBUTING.md`, `docs/`. Report what you found. If a `CLAUDE.md` already exists, read it fully — it may be self-generated (e.g. by `/init`) or hand-written, and it outranks the template on anything project-specific.

**Look up and sideways, not only down.** Every entry above names something *inside* the project, and that is the single most reliable way this step misses the file that actually governs the work:

- **Walk the parent directories to the drive root.** Claude Code auto-loads `CLAUDE.md` from ancestors of the working directory, and **it does not stop at a git boundary** — so a file one level up governs this project and loads *before* anything the project itself contains. A project can be a true blank slate and still be fully governed from above. Report every ancestor file you find, with its path.
- **Look at siblings.** A knowledge base, a research corpus or a shared docs repository next to the project is part of its real input even though no path inside the project points at it.

**Two existing files at different scopes is the normal case, not an edge case**, and the buckets below assume one. When an ancestor file and a project file both exist, do not merge them: decide, per rule, which scope owns it — a rule that governs several projects stays in the ancestor, a rule about this project moves down — and **write the split into your report as a decision, not a silent choice.** If the ancestor contradicts the project file, that is a conflict for the owner, exactly like a template conflict.

Check whether `docs/` (or any subdirectory) is itself a separate git repository nested inside this one, with its own remote — possibly excluded from the parent's `.gitignore` entirely. If so, say so: it has its own commit history and its own dirty/clean state, independent of the project repository's, and later steps' "same commit" and ledger-`commit`-column conventions apply per repository, not to the project as a single whole.

## 2. Discover the project facts

Fill the template's `Project facts` placeholders from evidence, not guesswork:

- Stack and versions — from the **package manifest** (`package.json`, `pyproject.toml`, `pom.xml`, `composer.json`, `go.mod`, `Cargo.toml`…) and its lockfile, plus any `.nvmrc` / `.tool-versions` / `Dockerfile` / CI config. A file merely *named* `manifest.*` is not necessarily one. If there is no package manifest, say so and take the stack from the docs or the source, marking it as such.
- Build, run, test, lint commands — from the manifest's scripts, Makefile, or CI workflow. **If the project has none, write `none`** — that is a fact, not a gap, and leaving `<...>` implies work that does not exist.
- **Verify each command — but only if it is read-only and local.** A command copied from a stale README that fails is worse than a placeholder. Run `--help`, `--version` and dry-run flags freely. **Do not run anything that writes, uploads, downloads, mutates state, or reaches a live service**, even when it is the documented way to use the project; steps 1–3 are read-only, and a documented command that pulls a mirror or overwrites an inventory file breaks that. For those, record the command, say it was **not executed**, and say why.
- Working setup — the integration branch that session worktrees start from. List the shared resources (databases, test databases, servers) that two sessions must not use at the same time. These fill the `Concurrent sessions` section. If only one session works at a time, say so and delete that section.
- If a fact can't be determined, leave the placeholder in and list it as a question rather than inventing a plausible value.

## 3. Reconcile with the existing file — ask, don't overwrite

If a `CLAUDE.md` already exists, sort it into the buckets below and show me the result before writing.

**Sort by rule, not by physical line.** A rule is one instruction with its explanation — usually a bullet and its continuation lines. Cite the line range (`44–48`), but do not emit one verdict per line: a literal line-by-line partition of a 200-line file produces a few hundred verdicts, buries the decisions, and makes the deliverable unusable as the thing I have to act on. Headings, blank lines and formatting are not rules and are not sorted.

- **Keep verbatim** — project-specific knowledge I can't derive from the code: domain rules, deploy quirks, "never touch X", environment specifics, historical warnings. These always survive; the template never overrides them.
- **Merge** — rules that say the same thing as the template in different words. Keep one version, prefer whichever is more specific.
- **Conflict** — rules that genuinely contradict the template (e.g. existing file says "commit freely", template says "ask before commit"; or different commit-message format, different test policy). **Stop here.** List each conflict as `existing: … / template: …` and ask which wins. Do not pick silently, and do not assume the template is right — the existing file may encode a decision I made deliberately.

- **Stale** — a claim the project contradicts. A build command that no longer exists, a module that was renamed, a path that's gone, a status that has since changed. **These are not conflicts** and they are not kept verbatim either; they are corrections. Propose the corrected wording and the evidence for it. This is a fourth bucket, not a footnote — on a project with real history it is often the largest one.

**A rule that names an external source of truth is neither of the four.** If the existing file says a section is a managed mirror of something outside the project (a global preferences file, an org-wide template) kept in sync by hand, don't resolve a conflict by editing the copy in place — that breaks the sync it declares. Propose the change against the named source instead, and mirror the result back once it's settled.

**Check the project's documents against each other, not only against the code.** The template says "code is ground truth", and on a documentation-heavy project that is not enough: the contradiction will be between two documents, both written in good faith, with nothing in the source to arbitrate. So:

- When two documents disagree, **the newest measured evidence wins** — not the newest file, not the most detailed one.
- **Check the date of anything you measure from.** A database dump, an exported inventory, a mirror or a captured response answers for the day it was taken. Querying a stale extract to ask whether something is still true returns a confident, wrong answer, and it is the most common way a false claim survives a careful review.
- Say which documents repeat a stale claim. Correcting one copy and leaving three is worse than correcting none, because the disagreement now looks settled.

Nothing gets dropped silently: if you decide a rule doesn't carry over, say so and why.

## 4. Write

**Write it where the project already keeps it.** Claude Code auto-loads `./CLAUDE.md` *and* `./.claude/CLAUDE.md`, so if the project's file lives in `.claude/`, editing it in place is right and creating a root one is wrong — you would leave two memory files that both load and immediately drift. Only put it at the root when there is no existing file anywhere. Say which location you wrote to.

**If the project pairs `CLAUDE.md` with an identical `AGENTS.md`, keep the pair identical.** That pairing is deliberate: `AGENTS.md` is what codex and several other agents auto-load, so it is how a non-Claude session gets the same rules. Check with a hash, not by eye. If they have already drifted, that is a finding — report which is newer and ask which wins, rather than picking.

After I've resolved the conflicts: write the merged `CLAUDE.md`. If the existing file isn't tracked in git, **copy it to `quarantine/<YYYY-MM-DD>/` first** — the same rule the template applies to every other removed file, so there is one mechanism and not two. Leave unresolved placeholders visible as `<...>` rather than filling them with guesses.

## 5. Wire the docs index

Ensure `docs/README.md` exists (create a stub index if not) and that `CLAUDE.md` links it — the one you actually wrote, at whichever location the project keeps it, not necessarily the root. If `docs/` is empty or missing, say so and offer to run the documentation bootstrap next — don't start it unasked. After `02`, [03-bootstrap-plan.md](03-bootstrap-plan.md) sets up the plan, the ledger and the ruling register.

## 6. Report

Summarise: placeholders filled, placeholders still open, rules kept from the existing file, stale facts corrected, and what's queued for the docs pass.

**If you stopped at section 3 and the conflicts are still open, that is the expected state** — section 3 forbids resolving them. Report them as unresolved and say so; do not invent resolutions to fill this section. "How each was resolved" applies only to a run that got past section 4.
