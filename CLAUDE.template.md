# <PROJECT> — CLAUDE.md

Template. Replace `<...>` placeholders. The sections below are behavioural guardrails — they do not replace project-specific architecture or style rules; put those under Project facts.

## Project facts

- Stack: `<language/runtime + versions, framework>`
- Build: `<command>`
- Run locally: `<command>`
- Test: `<command>` — run the relevant tests after every code change.
- Lint/format: `<command>`
- Docs index: [docs/README.md](docs/README.md)

## Documentation — mandatory

- `docs/` holds the project's living documentation; every module/subsystem gets its own md file. If `docs/` is missing, create it plus `docs/README.md` before any other doc work.
- `docs/README.md` is the index: one line per doc with a short description. Update it whenever a doc is added, removed or renamed.
- Any change touching documented behaviour updates its doc **in the same change** — a change isn't done until its docs are.
- New feature/module → new doc file → add to the index.
- One-home rule: each topic lives in exactly one doc; everywhere else links to it, never copies it.
- **Code is ground truth.** A doc line contradicted by code gets fixed the moment it's found, not noted for later.
- Prune stale lines; don't only append.
- Keep this file current too, and keep the docs-index link above wired.

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
- Destructive or irreversible operations (data deletion, schema change, mass update, force push) need a stated rollback plan before execution.
- Ask permission before `git commit` / `git push`.
- Commit message format: numbered list, one change per line — heading plus a 1-2 sentence description each.

## Exceptions

- Emergency fix: smallest verified correction beats extensive planning.
- Exploratory prototype: relax the caution, but keep assumptions and verification explicit.
