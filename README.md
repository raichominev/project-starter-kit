# project-starter-kit

Instructions and templates that give an existing project a `CLAUDE.md`, a real `docs/` folder, a plan and a ledger. The same rules keep them current as the work goes on.

The files here are **instructions, not documentation**. They are meant to be handed to Claude Code (or any coding agent) and executed against a target project.

## Install

This repository holds the **`raicho-kit`** marketplace, which carries the kit as a plugin:

```text
/plugin marketplace add raichominev/project-starter-kit
/plugin install project-starter-kit@raicho-kit
```

Then say "bootstrap this project", or invoke `/project-starter-kit`, in a chat opened in the target
project. The skill carries the order and the stop points, and the three step files travel with it.

**Or clone it.** The kit is plain Markdown and needs no install. See [Run it](#run-it) below.

## The files

| File | Role |
|---|---|
| [SKILL.md](SKILL.md) | The plugin entry point: the order, the stop points, and the rules that govern all three steps. Points at the step files rather than repeating them. |
| [CLAUDE.template.md](CLAUDE.template.md) | The generic `CLAUDE.md`: behavioural guardrails, the rules for the plan, the ledger and handoffs, and `<...>` placeholders for project facts. Copied into the target project, never edited in place here. |
| [PLAN.template.md](PLAN.template.md) | The plan skeleton: status header, goal, settled rulings, phases with `Verify:` lines and stop points, risks, open decisions. |
| [LEDGER.template.tsv](LEDGER.template.tsv) | The ledger's header row. One row per measurement, run, decision, release or retraction. |
| [01-bootstrap-claude-md.md](01-bootstrap-claude-md.md) | Step 1. Fills the template's placeholders from evidence, and reconciles it against any `CLAUDE.md` the project already has. Stops and asks on genuine conflicts. |
| [02-bootstrap-docs.md](02-bootstrap-docs.md) | Step 2. Builds `docs/` from the actual source — environment, architecture, modules, API, data model, glossary, open questions, test-coverage gaps — and wires the index back into `CLAUDE.md`. |
| [03-bootstrap-plan.md](03-bootstrap-plan.md) | Step 3. Builds `PLAN.md`, `PLAN-ARCHIVE.md` and `LEDGER.tsv` from evidence, makes the open-questions doc the ruling register, creates `docs/sessions/` for handoffs, and wires them into `CLAUDE.md`. |

## What the target project needs

Check these before starting. The kit works without them, but several instructions become
meaningless and you should know which.

| Requirement | If absent |
|---|---|
| **A git repository** | The template's worktree, pathspec-commit, integration-branch and deployed-commit rules have no referent, and `LEDGER.tsv`'s `commit` column cannot be filled. Delete those rules and use the column as a dated **evidence anchor** instead — a date plus the runbook, output file or quarantine folder that fixes the result in time. Say in `CLAUDE.md` that the project is not a repository, so no session assumes otherwise. |
| **A package manifest** | Leave `Build` / `Run` / `Test` / `Lint` as `none` rather than as `<...>`. A project can legitimately have none of them. |
| **One** package manifest | Two that disagree are worse than none, because each looks authoritative alone. Measured: a `pyproject.toml` declaring 3 dependencies plus 2 *optional* extras beside a `requirements.txt` pinning 37 packages including both extras unconditionally — and the launcher installed the second. **Find which one the project actually runs**, record that, and note the disagreement. |
| **One** test runner | `pytest --collect-only` finding tests does not mean it finds *the* tests. Measured: 29 collected, all from one file, while 9 of 10 `test_*.py` files held no test functions at all and were standalone scripts, several reaching live services by default. Inventory the test files, not just the runner's output. |
| **Executable tests** | `02`'s `TEST-COVERAGE.md` does not apply. Write `VERIFICATION.md` instead: the checks that do exist, what each proves, what it does not, and the gaps ranked by risk. |
| **Any open work** | `03` should be refused, not forced — see its own step 2: "a project with no open work should not be given a plan, and manufacturing phases to fill the template is worse than leaving it out." Say so in `CLAUDE.md`. Omit the `03`-created files' line in Project facts and the whole "Plan, ledger and rulings" section (both now conditional — see `CLAUDE.template.md`) rather than leaving them pointing at files that don't exist and won't. |

None of these is a blocker. All of them change what the steps should produce.

## Order

1. **`01`** — read-only discovery, then reconcile, then write `CLAUDE.md`. It halts for a decision whenever an existing rule contradicts the template; the existing file wins on anything project-specific.
2. **`02`** — only after `CLAUDE.md` is settled. Ends by writing `docs/README.md` and linking it from `CLAUDE.md`.
3. **`03`** — only after `docs/` exists. Ends by linking the plan, the ledger, the ruling register and the handoff folder from `CLAUDE.md`.

No step chains into the next on its own. Each one offers the next step and waits.

## What the kit sets up

What each instrument is for, and what it is measurably good at.

**Be clear about the claim.** Tested against four past mistakes on a real legacy project, the kit's
own instruments would have cleanly caught **one**, and that one was a cross-model review round —
a practice alongside the kit, not part of it. What they demonstrably *do* is turn a mistake that has
already happened into a standing rule that stops the second occurrence. That is worth a great deal,
and it is not the same as catching the first one.

- **A plan that holds open work only.** Each step has a `Verify:` line, and each phase ends at a stop point for the owner. A closed step carries its date and where the work departed from the plan. A finished phase moves to an archive, and nothing depends on the archive.
- **An append-only ledger.** Every measurement, failed run, decision, release and retraction gets a row, with the command and the commit that produced it. It stops a session from redoing rejected work, and it keeps numbers from drifting between docs.
- **A ruling register.** The owner's answers are numbered for good, dated and in the owner's own words. The settled ones are not raised again.
- **Handoffs with a paste-ready continuation prompt**, in one folder. Durable facts move to their home docs before a handoff is written.
- **Checks that fail when a rule breaks.** A check is trusted only after it has caught a planted defect, and a trap that bites twice becomes a check. A golden file pins behaviour that no test covers.
- **Safety rules for live data.** A write runs on a scratch copy first, and a rollback runs on a copy before anyone needs it. A removed file goes to a quarantine folder. A deploy ends with a read-back of the deployed commit.
- **Rules for concurrent sessions**: a worktree per session, commits with a pathspec, and a check before a session uses a shared resource.

## Run it

With the plugin installed, say "bootstrap this project" or invoke `/project-starter-kit`. Nothing else
is needed.

Without it, paste this into a chat opened in the target project, and replace `<KIT>` with wherever you
cloned this.

```text
Bootstrap this project using <KIT>.

Read its README.md for the order, then run 01-bootstrap-claude-md.md against
this repo, using CLAUDE.template.md as the template. Honour its stop points —
show me the conflicts and wait rather than deciding for me.

When CLAUDE.md is settled, run 02-bootstrap-docs.md. When docs/ exists,
run 03-bootstrap-plan.md.
```

## After the bootstrap

The template's own rules take over: docs are updated in the same change as the code, `docs/README.md` stays indexed, and a doc line contradicted by code gets fixed the moment it's found. When a step closes, the plan and the ledger change in the same commit.

## Companion plugins

Two Claude Code plugins write the handoffs that `docs/sessions/` holds:

- [deep-handoff](https://github.com/raichominev/session-handoff-skill) writes the session-close handoff and verifies it in rounds.
- [compaction-handoff](https://github.com/raichominev/compaction-handoff) writes a handoff before each auto-compaction and pastes its continuation prompt back afterwards.

Both are in the **`raicho-handoffs`** marketplace, whose manifest is in the `compaction-handoff`
repository:

```text
/plugin marketplace add raichominev/compaction-handoff
/plugin install compaction-handoff@raicho-handoffs
```

Installing `compaction-handoff` brings `deep-handoff` with it; you do not need to install both.
