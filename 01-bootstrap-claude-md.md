Set up this project's `CLAUDE.md` from [CLAUDE.template.md](CLAUDE.template.md), which sits beside this file. Do not write anything until step 4 — steps 1-3 are read-only.

## 1. Inventory what already exists

Look for existing agent instructions before assuming a blank slate: `CLAUDE.md` (root and any nested), `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`, `CONTRIBUTING.md`, `docs/`. Report what you found. If a `CLAUDE.md` already exists, read it fully — it may be self-generated (e.g. by `/init`) or hand-written, and it outranks the template on anything project-specific.

## 2. Discover the project facts

Fill the template's `Project facts` placeholders from evidence, not guesswork:

- Stack and versions — from the manifest and lockfile, plus any `.nvmrc` / `.tool-versions` / `Dockerfile` / CI config.
- Build, run, test, lint commands — from the manifest's scripts, Makefile, or CI workflow. **Verify each one actually runs.** A command copied from a stale README that fails is worse than a placeholder.
- If a fact can't be determined, leave the placeholder in and list it as a question rather than inventing a plausible value.

## 3. Reconcile with the existing file — ask, don't overwrite

If a `CLAUDE.md` already exists, sort every line of it into three buckets and show me the result before writing:

- **Keep verbatim** — project-specific knowledge I can't derive from the code: domain rules, deploy quirks, "never touch X", environment specifics, historical warnings. These always survive; the template never overrides them.
- **Merge** — rules that say the same thing as the template in different words. Keep one version, prefer whichever is more specific.
- **Conflict** — rules that genuinely contradict the template (e.g. existing file says "commit freely", template says "ask before commit"; or different commit-message format, different test policy). **Stop here.** List each conflict as `existing: … / template: …` and ask which wins. Do not pick silently, and do not assume the template is right — the existing file may encode a decision I made deliberately.

Also flag any claim in the existing file that the code contradicts — a build command that no longer exists, a module that was renamed, a path that's gone. Those are stale facts, not conflicts; propose the correction.

Nothing gets dropped silently: if you decide a line doesn't carry over, say so and why.

## 4. Write

After I've resolved the conflicts: write the merged `CLAUDE.md`. If the existing file isn't tracked in git, copy it to `CLAUDE.md.bak` first. Leave unresolved placeholders visible as `<...>` rather than filling them with guesses.

## 5. Wire the docs index

Ensure `docs/README.md` exists (create a stub index if not) and that the root `CLAUDE.md` links it. If `docs/` is empty or missing, say so and offer to run the documentation bootstrap next — don't start it unasked.

## 6. Report

Summarise: placeholders filled, placeholders still open, lines kept from the existing file, conflicts and how each was resolved, stale facts corrected, and what's queued for the docs pass.
