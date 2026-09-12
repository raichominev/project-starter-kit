# <PROJECT> — CLAUDE.md

Template. Replace `<...>` placeholders, and **delete this paragraph** once you do — it is an instruction to the person filling the template in, and it is false in the finished file.

The sections below are behavioural guardrails. They do not replace project-specific architecture or style rules: those go under **Project rules** and **Critical cautions**, which exist for exactly that and which outrank the generic sections whenever the two disagree.

## Project facts

- Stack: `<language/runtime + versions, framework>`
- Build: `<command>`
- Run locally: `<command>`
- Test: `<command>` — run the relevant tests after every code change.
- Lint/format: `<command>`
- Docs index: [docs/README.md](docs/README.md)
- Plan: [PLAN.md](PLAN.md) · Ledger: [LEDGER.tsv](LEDGER.tsv) · Rulings: [docs/QUESTIONS-FOR-OWNER.md](docs/QUESTIONS-FOR-OWNER.md) · Handoffs: [docs/sessions/](docs/sessions/README.md)

> **These four are created by `03`, not by `01`.** If you are writing this file during `01`, they do
> not exist yet, and shipping the line as-is gives the project four dead links. Either omit the line
> until `03` runs, or keep it and say in the same breath that the files are pending. Delete this note
> once they exist.

## Project rules

Everything specific to *this* project that a session must obey: the domain rules, the API and schema
quirks, the "never touch X", the deploy peculiarities, the things that look wrong and are correct.
The behavioural sections further down are generic; **this section is where the project's own
knowledge lives**, and it outranks them on any conflict.

- `<rule — what to do, and what happens if you don't>`

## Critical cautions

The subset of the above that **causes damage** when a session does not know it. One line each,
stated as the wrong belief and its consequence, not as a neutral fact. If this section is empty on a
project with any history, you have not looked hard enough.

- `<the trap, and the damage it causes>`

## Documentation — mandatory

- `docs/` holds the project's living documentation; every module/subsystem gets its own md file. If `docs/` is missing, create it plus `docs/README.md` before any other doc work.
- `docs/README.md` is the index: one line per doc with a short description. Update it whenever a doc is added, removed or renamed.
- Any change touching documented behaviour updates its doc **in the same change** — a change isn't done until its docs are.
  ⚠ **If `docs/` is a separate repository, "the same change" is impossible** and saying it anyway trains sessions to ignore the rule. Measured on two of five projects: one with `docs/` nested and separately versioned, one with `docs/` as a sibling repo carrying its own GitHub remote, 332 commits and its own branch. There, the obligation is *the same session*, plus a named way to tell that the docs repo has fallen behind — not a shared commit that cannot exist. Say which of the two regimes this project is under.
- New feature/module → new doc file → add to the index.
- One-home rule: each topic lives in exactly one doc; everywhere else links to it, never copies it.
- **Code is ground truth.** A doc line contradicted by code gets fixed the moment it's found, not noted for later.
- Prune stale lines; don't only append.
- Keep this file current too, and keep the docs-index link above wired.
- This file holds standing rules. Counts, dated narrative and current status go to their home docs, and this file points to them.
- A rule belongs in this file when a session that does not know it can damage something. Everything else is a pointer to its home doc.

## Plan, ledger and rulings — delete this section (and the matching Project-facts line) if `03` will not be run

- `PLAN.md` holds open work only: phases, steps with `Verify:` lines, open decisions and the Settled list. Each item points to the file that holds its result. "Open work only" governs what the plan is *for* — a step closed as `Done YYYY-MM-DD` stays until its phase is archived, and a `Closed` list of one-line pointers to archived phases is not a violation of it.
- Before you start work, read `PLAN.md` and `LEDGER.tsv`. Nobody raises a Settled item again. A `REJECTED` ledger row is not retried without new evidence.
- Close a step in this order: run its `Verify:` line, move its durable facts to their home docs, then rewrite the step to `Done YYYY-MM-DD` with any departure from the plan. Move a finished phase to `PLAN-ARCHIVE.md`. Change the plan's status header in the same commit as the work.
- `LEDGER.tsv` is append-only. Add a row for each measurement, failed or invalid run, decision, release and retraction. A correction is a new row that names the old one in `parent_id`.
- Every number, in the ledger or in a doc, has its evidence (the command or file) and its commit. Do not use a number without them.
- When a claim is retracted, correct every doc that repeated it, in the same commit.
- `docs/QUESTIONS-FOR-OWNER.md` is the ruling register. A question keeps its number. Each answer has its date and the owner's own words. A superseded answer stays, with a pointer to the new one.

## Checks and traps

- A trap that cost time or caused damage goes into this file as one line: the rule, and the wrong result that it produced. When a trap bites a second time, turn it into a check.
- A check is a script or test that fails when its rule breaks. A check counts only after it has caught a planted defect. Run a control first, and make a partial run fail.
- Establish the state by measurement. To find out whether a change is in a copy, compare the copy with the authoritative one, by a diff or a hash. A missing record does not show that nobody made the change. Before you conclude how production behaves, read its deployed data and configuration.
- Before you change behaviour that no test covers, pin it. Keep the current output for real input as a golden file. After the change, compare the new output with it. Compare field by field. A check of headers or counts alone can hide a shifted column.
- A finding from a second model or a subagent is a proposal. Confirm it by running it before you act on it.

## Sessions and handoffs

- At a session close, write a handoff in `docs/sessions/` with a paste-ready continuation prompt. Move its durable facts to their home docs first. Resume from a handoff, and read the current state from the home docs.
- The `deep-handoff` plugin writes the session-close handoff. The `compaction-handoff` plugin writes one before each auto-compaction and pastes its continuation prompt back afterwards.
- Native memory holds only what the repo cannot hold: the owner's preferences and quirks of the environment. It holds no project state.

## Concurrent sessions — delete this section only if nothing else touches the tree

⚠ **`git worktree list` is not the test.** It counts concurrent *Claude Code sessions* and is blind
to everything else that writes to the same files: the owner editing directly, a sync client such as
OneDrive or Dropbox, another editor, another tool. Measured on a project whose worktree count stayed
at exactly **1** while a real concurrent edit landed mid-session. Before deleting this section, check
for a sync client on the path and for file mtimes newer than `HEAD`, not only for worktrees.

- Start each session in its own git worktree and branch. Set `worktree.baseRef` in `.claude/settings.json` to the integration branch, `<branch>`.
- In a checkout that other sessions share, commit with a pathspec: `git commit -- <paths>`. A plain `git add` followed by `git commit` can take another session's staged work.
- Before you use a shared resource (`<database, test database, server>`), check that no other session is using it. If it is busy, use a private copy.

## Think before coding

- State assumptions explicitly. If uncertain, ask.
- Multiple interpretations → present them, don't pick one silently.
- A simpler approach exists → say so. Push back when warranted.
- Unclear → stop, name exactly what is confusing, ask. Don't hide confusion behind a guess.

## Simplicity

- Minimum code that solves the stated problem.
- No features beyond what was asked. No abstraction for single-use code. No unrequested configurability. No error handling for impossible states.
- Skip comments/docstrings unless the logic is non-obvious.
- Early returns over nested conditionals; small single-purpose functions.
- Gut-check: "would a senior engineer call this overcomplicated?" If yes, rewrite — 200 lines that could be 50 gets rewritten.

## Surgical changes

- Every changed line traces directly to the request.
- Don't improve adjacent code, comments or formatting. Don't refactor what isn't broken.
- Match existing style even where you'd do it differently.
- Unrelated dead code: mention it, don't delete it.
- Do remove imports/variables/functions that *your* change orphaned.

## Goal-driven execution

- Turn the task into a verifiable goal before starting: "add validation" → "tests for invalid inputs, then make them pass"; "fix the bug" → "test reproducing it, then make it pass"; "refactor X" → "tests pass before and after".
- Multi-step work: state the plan first, each step with its own check.
  ```
  1. [step] -> verify: [check]
  2. [step] -> verify: [check]
  ```
- "Docs updated" is part of the success criteria, not a follow-up.
- If something breaks unexpectedly, stop and re-plan rather than pushing through.

## Operational safety

- Never hardcode credentials, hosts or environment-specific values — they belong in per-environment config, outside version control.
- Destructive or irreversible operations (data deletion, schema change, mass update, force push) need a stated rollback plan before execution. Try the rollback on a copy first, because a rollback that has not run can miss data.
- Move a file that you remove to a dated quarantine folder. The owner deletes it.
- Run a change that writes data on a scratch copy of that data first. Run it on the live data only after the copy shows the expected result.
- Never regenerate a file over hand edits. If a generated file has hand edits, stop and ask.
- When you ship a build, build it from the integration branch. Compare the built artifact with the previous release, test that artifact, and ship that exact file.
- After a deploy, read back the deployed commit hash. Compare it with the commit that you meant to ship.
- Ask permission before `git commit` / `git push`.
- Commit message format: numbered list, one change per line — heading plus a 1-2 sentence description each. End with a `Verified` item that says how the change was checked. A commit that corrects an earlier one adds a `RETRACTION` item that names it.

## Exceptions

- Emergency fix: smallest verified correction beats extensive planning.
- Exploratory prototype: relax the caution, but keep assumptions and verification explicit.
