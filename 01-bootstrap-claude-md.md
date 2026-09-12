Set up this project's `CLAUDE.md` from [CLAUDE.template.md](CLAUDE.template.md), which sits beside this file. Do not write anything until step 4 — steps 1-3 are read-only.

## 1. Inventory what already exists

**Enumerate. Do not check a list.** The instinct is to test a handful of expected paths and stop, and it is wrong often enough to be worth banning outright. Measured across five projects, a checklist answered "no CLAUDE.md" four times for a project that had one, and gave the repository count of one project as 1, then 3, then 6, before classification settled it at **8 repositories, 2 worktrees and 1 stub**, alongside 3 agent-instruction files.

So run the scans, and report a **census** rather than a yes/no per expected path:

- **Every agent-instruction file inside the project**, by search and not by guess: `CLAUDE.md`, `.claude/CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`, `CONTRIBUTING.md`, at any depth.
- **Ancestors, but only for the files the runtime actually loads.** Claude Code walks up from the working directory for `CLAUDE.md` / `CLAUDE.local.md` and **does not stop at a git boundary**, so a project can be a blank slate and still be governed from above. Walk up and **report what you find, with its path** — do not ancestor-walk the other filenames, which are not auto-loaded, and do not treat a hit as project scope automatically. ⚠ On a machine where many projects sit under one parent, or a CI checkout under `…/org/repo`, the ancestors will hold other people's and other products' rules. **Report; do not absorb, and never rewrite an ancestor file.**
- ⚠ **Loading earlier is not authority.** The files are concatenated from the root down, so the *closest* file is read last and is the more specific one. An ancestor supplies context; it does not outrank the project on anything project-specific.
- **Every git repository in the tree** — but `find -name .git` is itself too crude, and gets the count wrong in three different ways. Measured on one project, where successive answers were 1, 3, 6, 9, then finally **8 repositories, 2 worktrees and 1 stub**:
  - **`.git` as a *file*, not a directory, is a worktree**, not a repository. It contains `gitdir: …`. Counting it as a repo inflates the total and invents components that cannot be live or dead on their own. Settle it with `git worktree list` from the parent repo — that project had **15** worktrees.
  - **A near-empty `.git` directory is a stub.** Every `git` command there fails, and it defeats a naive `isdir('.git')` check — which is how the same project first appeared to *be* a repository when it was not.
  - **Vendor clones and gitignored sub-clones** are repositories but not *this project's* repositories. Say which is which.

  So: list candidates by search, then **classify each one** as repository / worktree / stub / vendor, and only then count.
- **Siblings — include one only when something names it.** A knowledge base, research corpus or docs repository beside the project can be a real input that nothing inside points at, so look. But a directory is not in scope merely for being adjacent: include it when the project's files, its remotes, its docs or the owner name it, and otherwise **list it as a question**. Absorbing a neighbour on sight is how another client's tree, or the wrong corpus, ends up in the documentation.

Read every instruction file you find, fully. Each outranks the template on anything project-specific.

**Then reconcile what you found.** More than one instruction file, at different scopes, is common enough to plan for. The buckets in section 3 assume one. When more than one exists, do not merge them; decide **per rule** which scope owns it — a rule governing several projects stays in the ancestor, a rule about this project moves down — and write the split into your report as a decision, not a silent choice. An ancestor contradicting the project file is a conflict for the owner, exactly like a template conflict. Expect at least: a live file, possibly an auto-synced mirror, possibly a stale backup copy, and possibly module-scoped files.

**Check whether the project already automates an invariant before prescribing discipline for it.** If an identical `AGENTS.md` is kept in sync by a hook rather than by hand, say so — the pair cannot drift, and warning about drift there is noise. Same for anything else the kit tells a human to remember.

Check whether `docs/` (or any subdirectory) is itself a separate git repository nested inside this one, with its own remote — possibly excluded from the parent's `.gitignore` entirely. If so, say so: it has its own commit history and its own dirty/clean state, independent of the project repository's, and later steps' "same commit" and ledger-`commit`-column conventions apply per repository, not to the project as a single whole.

## 2. Discover the project facts

Fill the template's `Project facts` placeholders from evidence, not guesswork:

- Stack and versions — from the **package manifest** (`package.json`, `pyproject.toml`, `pom.xml`, `composer.json`, `go.mod`, `Cargo.toml`…) and its lockfile, plus any `.nvmrc` / `.tool-versions` / `Dockerfile` / CI config. A file merely *named* `manifest.*` is not necessarily one. If there is no package manifest, say so and take the stack from the docs or the source, marking it as such.
- Build, run, test, lint commands — from the manifest's scripts, Makefile, or CI workflow. **If the project has none, write `none`** — that is a fact, not a gap, and leaving `<...>` implies work that does not exist.
- **Verify each command, within one limit.** A command copied from a stale README that fails is worse than a placeholder, so run `--help`, `--version`, dry-run and collect-only flags freely.
  **Never run anything that reaches a live service, deploys, touches production, or is otherwise irreversible** — a command that pulls a mirror, overwrites an inventory file or writes to a server breaks the read-only contract of steps 1–3. Record those, say they were **not executed**, and say why.
  **Local, reversible writes are fine, and sometimes necessary.** A test suite writes caches and temp files; a compile writes objects. The template asks for a `Test:` command and you cannot confirm one without running it — so run it, in a scratch or temp location where you can, and say what it wrote.
- Working setup — the integration branch that session worktrees start from. List the shared resources (databases, test databases, servers) that two sessions must not use at the same time. These fill the `Concurrent sessions` section. If only one session works at a time, say so and delete that section.
- If a fact can't be determined, leave the placeholder in and list it as a question rather than inventing a plausible value.

## 3. Reconcile with the existing file — ask, don't overwrite

If a `CLAUDE.md` already exists, sort it into the buckets below and show me the result before writing.

**Sort by rule, not by physical line.** A rule is one instruction with its explanation — usually a bullet and its continuation lines. Cite the line range (`44–48`), but do not emit one verdict per line: a literal line-by-line partition of a 200-line file produces a few hundred verdicts, buries the decisions, and makes the deliverable unusable as the thing I have to act on. Headings, blank lines and formatting are not rules and are not sorted.

- **Keep verbatim** — project-specific knowledge I can't derive from the code: domain rules, deploy quirks, "never touch X", environment specifics, historical warnings. These always survive; the template never overrides them.
- **Merge** — rules that say the same thing as the template in different words. Keep one version, prefer whichever is more specific.
- **Conflict** — rules that genuinely contradict the template (e.g. existing file says "commit freely", template says "ask before commit"; or different commit-message format, different test policy). **Stop here.** List each conflict as `existing: … / template: …` and ask which wins. Do not pick silently, and do not assume the template is right — the existing file may encode a decision I made deliberately.

- **Stale** — a claim the project contradicts. A build command that no longer exists, a module that was renamed, a path that's gone, a status that has since changed. **These are not conflicts** and they are not kept verbatim either; they are corrections. Propose the corrected wording and the evidence for it. This is a fourth bucket, not a footnote; on a project with real history, expect it to be populated.

**A rule that names an external source of truth is neither of the four.** If the existing file says a section is a managed mirror of something outside the project (a global preferences file, an org-wide template) kept in sync by hand, don't resolve a conflict by editing the copy in place — that breaks the sync it declares. Propose the change against the named source instead, and mirror the result back once it's settled.

**Check the project's documents against each other, not only against the code.** The template says "code is ground truth", and on a documentation-heavy project that is not enough: the contradiction will be between two documents, both written in good faith, with nothing in the source to arbitrate. So:

- When two documents disagree, **the newest measured evidence wins** — not the newest file, not the most detailed one.
- **Check the date of anything you measure from.** A database dump, an exported inventory, a mirror or a captured response answers for the day it was taken. Querying a stale extract to ask whether something is still true returns a confident, wrong answer — measured on one project, where four documents asserted a condition that two others recorded as resolved, because everyone reached for an export that predated the fix.
- Say which documents repeat a stale claim. Correcting one copy and leaving three is worse than correcting none, because the disagreement now looks settled.

Nothing gets dropped silently: if you decide a rule doesn't carry over, say so and why.

## 4. Write

**Write it where the project already keeps it.** Claude Code auto-loads `./CLAUDE.md` *and* `./.claude/CLAUDE.md`, so if the project's file lives in `.claude/`, editing it in place is right and creating a root one is wrong — you would leave two memory files that both load and immediately drift. Put it at the root only when there is no existing file **at the project's own scope**. An ancestor file, or a module-scoped one deeper in, does **not** substitute for a project-wide home — Claude Code is designed to layer a project file under an ancestor, and skipping it because something governs from above leaves the project with no home of its own. Say which location you wrote to, and why.

**If the project pairs `CLAUDE.md` with an identical `AGENTS.md`, keep the pair identical.** That pairing is deliberate: `AGENTS.md` is what codex and several other agents auto-load, so it is how a non-Claude session gets the same rules. Check with a hash, not by eye. If they have already drifted, that is a finding — report which is newer and ask which wins, rather than picking.

After I've resolved the conflicts: write the merged `CLAUDE.md`. If the existing file isn't tracked in git, **copy it to `quarantine/<YYYY-MM-DD>/` first** — the same rule the template applies to every other removed file, so there is one mechanism and not two. Leave unresolved placeholders visible as `<...>` rather than filling them with guesses.

## 5. Wire the docs index

Ensure `docs/README.md` exists (create a stub index if not) and that `CLAUDE.md` links it — the one you actually wrote, at whichever location the project keeps it, not necessarily the root. If `docs/` is empty or missing, say so and offer to run the documentation bootstrap next — don't start it unasked. After `02`, [03-bootstrap-plan.md](03-bootstrap-plan.md) sets up the plan, the ledger and the ruling register.

## 6. Report

Summarise: placeholders filled, placeholders still open, rules kept from the existing file, stale facts corrected, and what's queued for the docs pass.

**If you stopped at section 3 and the conflicts are still open, that is the expected state** — section 3 forbids resolving them. Report them as unresolved and say so; do not invent resolutions to fill this section. "How each was resolved" applies only to a run that got past section 4.
