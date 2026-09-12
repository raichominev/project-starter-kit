Set up this project's plan, ledger and ruling register. Run this step after `01` and `02`, because it needs `CLAUDE.md` and `docs/`. Steps 1 and 2 are read-only.

## 1. Inventory what already exists

Look for existing plans and records: `PLAN*`, `ROADMAP*`, `TODO*`, `CHANGELOG*`, `HANDOFF*`, `REMEDIATION*`, `docs/sessions/`, release notes, a `.tsv` **that records decisions or measurements** (a regenerated data extract is not one — check what it holds before treating it as a ledger), and any issue tracker that the docs name. Report what you found.

An existing plan outranks the template on content. Move its content into the new structure and keep all of it.

**And if the existing plan is already doing the job, leave it alone.** A project whose plan and archive already carry status, dated closures and a ranked queue does not need restructuring into this shape — say that it already satisfies the step, note anything genuinely missing, and stop. Reformatting a working instrument into the template's layout is churn, and it costs the owner the familiarity they already have with it.

## 2. Collect the open work from evidence

Take candidate items from these sources:

- The owner's request.
- **Any existing plan, remediation list, roadmap or ranked queue the project already keeps** — including one inside a handoff. This is where the open work usually is, and section 1 already told you to keep all of it.
- `docs/QUESTIONS-FOR-OWNER.md`.
- The gaps in `docs/TEST-COVERAGE.md`, or in `VERIFICATION.md` if the project has that instead.
- `TODO` and `FIXME` lines in the code. Cite `file:line`.
- Open issues.

Do not invent items from anywhere else. If all of these are empty, say so — **a project with no open work should not be given a plan**, and manufacturing phases to fill the template is worse than leaving it out.

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

Create `PLAN-ARCHIVE.md` now. **If the project has already finished phases of work, write them in** — section 1 said to keep all of an existing plan's content, and that includes the part that is done. For each: what it delivered, what it was checked against, and where it departed from what was expected. A title-only archive is correct only for a project with no history. Nothing may depend on the archive, because it holds history only.

## 5. Create `LEDGER.tsv` from `LEDGER.template.tsv`

The ledger records what was done, so that no session does it again or measures it again. Add one row for each measurement and each run, a failed or invalid run too. Also add one row for each dead end with its reason, each decision, each release and each retraction.

| Column | What it holds |
|---|---|
| `date` | `YYYY-MM-DD` |
| `id` | `L-<n>`. An id is never used again. |
| `parent_id` | The row this row relates to, **with the relation named in `change`**: *extends*, *corrects*, *retracts* or *supersedes*. A bare id cannot carry that, and the difference matters: a row that extends its parent leaves the parent standing, a row that retracts it does not. Empty if there is none. |
| `kind` | `measurement`, `run`, `decision`, `release` or `retraction` |
| `change` | What was done or tried, in one line |
| `result` | The number or the outcome |
| `verdict` | Which one depends on the `kind`. `measurement` → `KEPT` (the number stands) or `WITHDRAWN` (it was wrong). `run` → `DONE` (it worked), `REJECTED` (the approach does not work — this is the row that blocks a retry) or `INVALID` (the run itself was broken, so it measured nothing). `decision` → `DONE` or `SUPERSEDED`. `release` → `DONE`, or `WITHDRAWN` if it was rolled back. `retraction` → `KEPT`, since the retraction itself stands. |
| `evidence` | The command, test or file that produced the result |
| `commit` | The commit that the result belongs to. **If the project is not a git repository**, use a dated evidence anchor instead — a date plus the runbook, output file or quarantine folder that fixes the result in time — and say in `CLAUDE.md` that the column means that here |
| `detail` | The doc that holds the detail |

Rules:

- Add rows only. To correct a row, add a new row that names it in `parent_id`. Then set the old row's verdict to `SUPERSEDED` or `WITHDRAWN`. The old row stays.
- A number needs its evidence and its commit. A number without them does not go into the ledger or into a doc.
- Read the ledger before you propose work. A `REJECTED` row blocks a retry. Only new evidence reopens it, and the new row gives that evidence.
- When you retract a claim, correct every doc that repeated it, in the same commit.
- **A retraction row is only useful if it records what would have caught the mistake.** Write: the single scoped claim that was wrong, the action or checkpoint it preceded, **the exact probe or file comparison with its inputs**, the observation that rejected it, and a pointer to the raw evidence. If you cannot supply the probe — because the claim was interpretive, or the evidence no longer exists — say so in the row rather than leaving a readable account that looks complete. Measured: of 36 real retraction rows, 14 yielded no runnable check, and each of those was missing the invocation, the discriminating witness, or evidence that no longer existed.
- ⚠ **Do not expect a later tool to reconstruct the check from the prose.** In a blinded test, a capable model proposed a plausible-looking check for a third of statements that had never been wrong at all, so a check "recovered" from a badly written row is as likely to be invention as recall.

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

Link `PLAN.md`, `LEDGER.tsv`, `PLAN-ARCHIVE.md`, `docs/QUESTIONS-FOR-OWNER.md` and `docs/sessions/README.md` from `CLAUDE.md` and from `docs/README.md`.

**A link is not an explanation.** Check that `CLAUDE.md` also carries the *usage* rules for what you just created — append-only, `parent_id` for corrections, a number needs its evidence and its anchor, `Done YYYY-MM-DD`, nothing depends on the archive, a `REJECTED` row blocks a retry. Those rules live in `CLAUDE.template.md`'s **Plan, ledger and rulings** section, which is `01`'s territory — so **if `01` was not run, or ran before these files existed, they are missing**, and the project now links to instruments nobody has been told how to use. Add the section, and say that you did.

**Check the names against the project's own vocabulary.** A project whose domain already contains a "ledger", a "plan" or a "register" will read `LEDGER.tsv` as one of its own. Say so in the index line if it does, so the two are not confused.

Report the phases and steps in the plan, the open decisions, the ledger rows that you added, and what you could not determine.

## Next

Nothing chains automatically. Report, then stop and wait.

Tell me: the phases and steps now in the plan, the open decisions, the ledger rows you added, and
what you could not determine. Then offer — and wait for an answer — to close the loop by running the
first `Verify:` line in the plan, so the plan's first claim is tested rather than assumed.
