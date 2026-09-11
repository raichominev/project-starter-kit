# project-starter-kit

Instructions and templates that give an existing project a `CLAUDE.md`, a real `docs/` folder, a plan and a ledger. The same rules keep them current as the work goes on.

The files here are **instructions, not documentation**. They are meant to be handed to Claude Code (or any coding agent) and executed against a target project.

## The files

| File | Role |
|---|---|
| [CLAUDE.template.md](CLAUDE.template.md) | The generic `CLAUDE.md`: behavioural guardrails, the rules for the plan, the ledger and handoffs, and `<...>` placeholders for project facts. Copied into the target project, never edited in place here. |
| [PLAN.template.md](PLAN.template.md) | The plan skeleton: status header, goal, settled rulings, phases with `Verify:` lines and stop points, risks, open decisions. |
| [LEDGER.template.tsv](LEDGER.template.tsv) | The ledger's header row. One row per measurement, run, decision, release or retraction. |
| [01-bootstrap-claude-md.md](01-bootstrap-claude-md.md) | Step 1. Fills the template's placeholders from evidence, and reconciles it against any `CLAUDE.md` the project already has. Stops and asks on genuine conflicts. |
| [02-bootstrap-docs.md](02-bootstrap-docs.md) | Step 2. Builds `docs/` from the actual source — environment, architecture, modules, API, data model, glossary, open questions, test-coverage gaps — and wires the index back into `CLAUDE.md`. |
| [03-bootstrap-plan.md](03-bootstrap-plan.md) | Step 3. Builds `PLAN.md`, `PLAN-ARCHIVE.md` and `LEDGER.tsv` from evidence, makes the open-questions doc the ruling register, creates `docs/sessions/` for handoffs, and wires them into `CLAUDE.md`. |

## Order

1. **`01`** — read-only discovery, then reconcile, then write `CLAUDE.md`. It halts for a decision whenever an existing rule contradicts the template; the existing file wins on anything project-specific.
2. **`02`** — only after `CLAUDE.md` is settled. Ends by writing `docs/README.md` and linking it from `CLAUDE.md`.
3. **`03`** — only after `docs/` exists. Ends by linking the plan, the ledger, the ruling register and the handoff folder from `CLAUDE.md`.

No step chains into the next on its own. Each one offers the next step and waits.

## What the kit sets up

Each of these instruments has caught real problems in real projects:

- **A plan that holds open work only.** Each step has a `Verify:` line, and each phase ends at a stop point for the owner. A closed step carries its date and where the work departed from the plan. A finished phase moves to an archive, and nothing depends on the archive.
- **An append-only ledger.** Every measurement, failed run, decision, release and retraction gets a row, with the command and the commit that produced it. It stops a session from redoing rejected work, and it keeps numbers from drifting between docs.
- **A ruling register.** The owner's answers are numbered for good, dated and in the owner's own words. The settled ones are not raised again.
- **Handoffs with a paste-ready continuation prompt**, in one folder. Durable facts move to their home docs before a handoff is written.
- **Checks that fail when a rule breaks.** A check is trusted only after it has caught a planted defect, and a trap that bites twice becomes a check. A golden file pins behaviour that no test covers.
- **Safety rules for live data.** A write runs on a scratch copy first, and a rollback runs on a copy before anyone needs it. A removed file goes to a quarantine folder. A deploy ends with a read-back of the deployed commit.
- **Rules for concurrent sessions**: a worktree per session, commits with a pathspec, and a check before a session uses a shared resource.

## Run it

Paste this into a chat opened in the target project:

```text
Bootstrap this project using G:\prj\project-starter-kit.

Read its README.md for the order, then run 01-bootstrap-claude-md.md against
this repo, using CLAUDE.template.md as the template. Honour its stop points —
show me the conflicts and wait rather than deciding for me.

When CLAUDE.md is settled, run 02-bootstrap-docs.md. When docs/ exists,
run 03-bootstrap-plan.md.
```

## After the bootstrap

The template's own rules take over: docs are updated in the same change as the code, `docs/README.md` stays indexed, and a doc line contradicted by code gets fixed the moment it's found. When a step closes, the plan and the ledger change in the same commit.

## Companion plugins

Two Claude Code plugins in the `raicho-skills` marketplace write the handoffs that `docs/sessions/` holds:

- [deep-handoff](https://github.com/raichominev/session-handoff-skill) writes the session-close handoff and verifies it in rounds.
- [compaction-handoff](https://github.com/raichominev/compaction-handoff) writes a handoff before each auto-compaction and pastes its continuation prompt back afterwards. It installs deep-handoff too.

```text
/plugin marketplace add raichominev/concilium
/plugin install compaction-handoff@raicho-skills
```
