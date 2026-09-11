Set up this project's plan, ledger and ruling register. Run this step after `01` and `02`, because it needs `CLAUDE.md` and `docs/`. Steps 1 and 2 are read-only.

## 1. Inventory what already exists

Look for existing plans and records: `PLAN*`, `ROADMAP*`, `TODO*`, `CHANGELOG*`, `HANDOFF*`, `*.tsv`, `docs/sessions/`, release notes, and any issue tracker that the docs name. Report what you found.

An existing plan outranks the template on content. Move its content into the new structure and keep all of it.

## 2. Collect the open work from evidence

Take candidate items only from these sources:

- The owner's request.
- `docs/QUESTIONS-FOR-OWNER.md`.
- The gaps in `docs/TEST-COVERAGE.md`.
- `TODO` and `FIXME` lines in the code. Cite `file:line`.
- Open issues.

Show the list. Ask the owner which items go into the plan, and in which order.

## 3. Write `PLAN.md` from `PLAN.template.md`

Fill each section:

- **Status header**: a revision number, the date and one line on where the work stands. Change it in the same commit as the work that it describes.
- **Goal**: what the plan delivers, and what is out of scope.
- **Settled**: the owner's decisions that apply to all work. Each has its date and the owner's own words. Nobody raises a Settled item again.
- **Phases**, in order. Each phase has a goal, numbered steps and a stop point. Each step has a `Verify:` line: the command, test or file that shows the step is done. At the stop point, the owner reviews the phase before the next one starts.
- **Risks**: each with the signal that would show it early.
- **Open decisions**: each with the options, the evidence and the person who decides. A step that depends on an open decision does not start.

`PLAN.md` holds open work only. Each item points to the file that holds its result.

## 4. Close steps, and archive finished phases

Close a step in this order:

1. Run its `Verify:` line and look at the result.
2. Move each durable fact that the step produced to its home doc.
3. Rewrite the step's line to `Done YYYY-MM-DD`. Add one line on where the work departed from the plan.
4. When all steps of a phase are done, move the phase to `PLAN-ARCHIVE.md`. Leave one dated line in `PLAN.md` that points to it.

Create `PLAN-ARCHIVE.md` now, with only its title. Nothing may depend on the archive, because it holds history only.

## 5. Create `LEDGER.tsv` from `LEDGER.template.tsv`

The ledger records what was done, so that no session does it again or measures it again. Add one row for each measurement and each run, a failed or invalid run too. Also add one row for each dead end with its reason, each decision, each release and each retraction.

| Column | What it holds |
|---|---|
| `date` | `YYYY-MM-DD` |
| `id` | `L-<n>`. An id is never used again. |
| `parent_id` | The row that this row corrects or continues. Empty if there is none. |
| `kind` | `measurement`, `run`, `decision`, `release` or `retraction` |
| `change` | What was done or tried, in one line |
| `result` | The number or the outcome |
| `verdict` | `KEPT`, `REJECTED`, `INVALID`, `DONE`, `SUPERSEDED` or `WITHDRAWN` |
| `evidence` | The command, test or file that produced the result |
| `commit` | The commit that the result belongs to |
| `detail` | The doc that holds the detail |

Rules:

- Add rows only. To correct a row, add a new row that names it in `parent_id`. Then set the old row's verdict to `SUPERSEDED` or `WITHDRAWN`. The old row stays.
- A number needs its evidence and its commit. A number without them does not go into the ledger or into a doc.
- Read the ledger before you propose work. A `REJECTED` row blocks a retry. Only new evidence reopens it, and the new row gives that evidence.
- When you retract a claim, correct every doc that repeated it, in the same commit.

## 6. Make `docs/QUESTIONS-FOR-OWNER.md` the ruling register

- A question keeps its number. Other docs cite it as `#N`.
- An answer has its date and the owner's own words.
- A superseded answer stays, with a pointer to the answer that replaces it.
- A ruling that applies to all work also goes into the Settled list of `PLAN.md`.

## 7. Create the handoff folder

Create `docs/sessions/README.md` with the rules below and an empty index. At each session close, add `SESSION-CLOSE-YYYY-MM-DD-<topic>.md` with a paste-ready continuation prompt.

- Before you write a handoff, move its durable facts to their home docs.
- A handoff holds the read order, the state by topic, a ranked queue and the open questions. It also lists what not to retry, each with its reason and its ledger row.
- Before you hand off, recompute each number, check each link and run each command that the handoff names. Mark a claim that you cannot check as `unverified`.
- A handoff is a dated snapshot. Resume from it, and read the current state from the home docs.
- The `deep-handoff` and `compaction-handoff` plugins write these handoffs.

## 8. Wire and report

Link `PLAN.md`, `LEDGER.tsv`, `docs/QUESTIONS-FOR-OWNER.md` and `docs/sessions/README.md` from `CLAUDE.md` and from `docs/README.md`.

Report the phases and steps in the plan, the open decisions, the ledger rows that you added, and what you could not determine.
