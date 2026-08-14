Document this existing web project into `docs/`, working bottom-up from the actual code. Never document a feature you haven't seen in source.

If the repo is large, go module by module rather than in one pass — finish and index each doc before starting the next.

## 1. Environment — `docs/ENVIRONMENT.md`

Language/runtime versions, package manager, framework(s), build tool, deploy target (container/serverless/VM/static), config sources and env var **names and purpose only — never values**, external services (DB, cache, queue, auth provider, third-party APIs). End with a local dev runbook: the exact commands to install, build, run and test.

## 2. Architecture — `docs/ARCHITECTURE.md`

Major modules/layers (frontend, API, workers, data access, jobs) and how they communicate (HTTP/RPC/events/direct import). Walk one representative request end to end — login or the main CRUD path — from entry point to response. Note the auth/session model. Diagram in words or mermaid.

## 3. Module inventory — `docs/MODULES.md`

One entry per top-level module: purpose, key files, public interface (exported functions / routes / components), what calls it, what it calls. Split per module if it outgrows a screen or two, and index the split.

## 4. API surface — `docs/API.md`

Every route/endpoint: method, path, auth requirement, request shape, response shape, error cases. Include background jobs and webhooks if present.

## 5. Data model — `docs/DATA-MODEL.md`

Entities, fields, relations, constraints, indexes, migration mechanism. Where schema and code disagree, say which one the runtime actually uses.

## 6. Domain glossary — `docs/CONCEPTS.md`

Domain terms, entity names, status/enum codes, and business rules that are encoded in code but not obvious from naming.

## 7. Open questions — `docs/QUESTIONS-FOR-OWNER.md`

Where code is ambiguous, business logic undocumented, error handling unclear, or intent not inferable from source — write a numbered question. Never guess in the docs.

## 8. Tests — `docs/TEST-COVERAGE.md`

Inventory the existing tests and the framework/runner in use. Map coverage against the modules and flows from steps 2-5 and list what is uncovered. For each gap propose concrete cases: happy path, edge cases, error/failure modes. Rank gaps by risk. Then ask which to implement and write those tests — including a regression test for any bug you uncover while reading.

## 9. Index and wiring — `docs/README.md`

One line per doc file with a short description. Link `docs/README.md` from the root `CLAUDE.md` so the index is reachable from the project's agent instructions.

## Rules

- Cite `file:line` for non-obvious claims so they can be checked.
- One topic, one home file — everywhere else links, never duplicates.
- Docs chase code: a doc claim later contradicted by source gets fixed in that same session.
- Report what you could not determine rather than filling the gap with a plausible guess.
