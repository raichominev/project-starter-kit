# project-starter-kit

A three-file process for giving an existing project a `CLAUDE.md` and a real `docs/` folder — and for keeping both alive as the code changes.

The files here are **instructions, not documentation**. They are meant to be handed to Claude Code (or any coding agent) and executed against a target project.

## The files

| File | Role |
|---|---|
| [CLAUDE.template.md](CLAUDE.template.md) | The generic `CLAUDE.md` — behavioural guardrails plus `<...>` placeholders for project facts. Copied into the target project, never edited in place here. |
| [01-bootstrap-claude-md.md](01-bootstrap-claude-md.md) | Step 1. Fills the template's placeholders from evidence, and reconciles it against any `CLAUDE.md` the project already has. Stops and asks on genuine conflicts. |
| [02-bootstrap-docs.md](02-bootstrap-docs.md) | Step 2. Builds `docs/` from the actual source — environment, architecture, modules, API, data model, glossary, open questions, test-coverage gaps — and wires the index back into `CLAUDE.md`. |

## Order

1. **`01`** — read-only discovery, then reconcile, then write `CLAUDE.md`. It halts for a decision whenever an existing rule contradicts the template; the existing file wins on anything project-specific.
2. **`02`** — only after `CLAUDE.md` is settled. Ends by writing `docs/README.md` and linking it from `CLAUDE.md`.

Step 1 deliberately does not chain into step 2 on its own — it offers, and waits.

## Run it

Paste this into a chat opened in the target project:

```text
Bootstrap this project using G:\prj\project-starter-kit.

Read its README.md for the order, then run 01-bootstrap-claude-md.md against
this repo, using CLAUDE.template.md as the template. Honour its stop points —
show me the conflicts and wait rather than deciding for me.

When CLAUDE.md is settled, run 02-bootstrap-docs.md.
```

## After the bootstrap

The template's own rules take over: docs are updated in the same change as the code, `docs/README.md` stays indexed, and a doc line contradicted by code gets fixed the moment it's found.
