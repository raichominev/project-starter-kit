---
name: project-starter-kit
description: Bootstrap an existing project's agent documentation - a CLAUDE.md reconciled against whatever the project already has, a docs/ folder built bottom-up from the source, and a plan, an append-only ledger and a numbered ruling register. Use when the user says "bootstrap this project", "set up CLAUDE.md", "run the starter kit", "generate the project docs", "give this repo a plan and a ledger", or asks to document an existing codebase so an agent can work in it.
---

# Project starter kit

Three steps, in order. Each step writes real files into the **target project**, not into this kit.

| Step | File | Produces |
|---|---|---|
| 1 | `01-bootstrap-claude-md.md` | `CLAUDE.md`, reconciled with any file the project already has |
| 2 | `02-bootstrap-docs.md` | `docs/`, built from the source |
| 3 | `03-bootstrap-plan.md` | `PLAN.md`, `PLAN-ARCHIVE.md`, `LEDGER.tsv`, the ruling register, `docs/sessions/` |

The templates are `CLAUDE.template.md`, `PLAN.template.md` and `LEDGER.template.tsv`. Copy a template
into the target project. Never edit one in place here.

## Before the first step

Read `README.md`. It holds the table of what the target project needs, and what each step must produce
differently when one of those things is absent. The kit runs without them. Several instructions become
meaningless, and you must know which ones.

Then report a **census** of what the project already has. Do not check a list of expected paths. That
instinct is wrong often enough that `01` bans it, and section 1 of `01` gives the scans to run.

## Rules that govern all three steps

- **No step starts the next one.** A step ends, offers the next step, and waits for an answer.
- **Stop at a conflict.** When an existing rule contradicts the template, show both as
  `existing: … / template: …` and ask which one wins. Do not decide, and do not assume the template is
  right.
- **The existing file outranks the template** on anything project-specific.
- **Do not create a document with no referent.** An empty `API.md` is worse than no `API.md`, because
  the index then promises something the project does not have.
- **Do not force a plan onto a project with no open work.** `03` refuses that case. Manufacturing
  phases to fill the template is worse than leaving the plan out.
- **Read-only until the step says to write.** Sections 1 to 3 of `01` are read-only. Sections 1 and 2
  of `03` are read-only.
- **Report what you could not determine.** Leave an unresolved placeholder visible as `<...>`. Do not
  fill it with a plausible value.

## After the bootstrap

The template's own rules take over. Docs change in the same commit as the code. A doc claim that the
source contradicts gets fixed in the session that finds it. When a step closes, the plan and the
ledger change together.
