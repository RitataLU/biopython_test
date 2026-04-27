# autoresearch — FASTA parser edition

Autonomous iterative improvement of `Bio/SeqIO/FastaIO.py`,
evaluated by the test suite in `Tests/test_SeqIO_FastaIO.py`.

## Analogy to original autoresearch

| Original (ML)         | This (FASTA parser)              |
|-----------------------|----------------------------------|
| `train.py`            | `Bio/SeqIO/FastaIO.py`           |
| `prepare.py`          | `evaluate_fasta.py` (read-only)  |
| `val_bpb` (minimize)  | `tests_failed` (minimize)        |
| time budget = 5 min   | test suite runtime (~1s)         |

## Setup

1. Branch: `autoresearch/fasta-<tag>` from current master.
2. Read `Bio/SeqIO/FastaIO.py` in full — this is the only file you edit.
3. Read `Tests/test_SeqIO_FastaIO.py` to understand what is tested.
4. Read `evaluate_fasta.py` — this is fixed, never modify it.
5. Create `results_fasta.tsv` with just the header row.
6. Run baseline: `python evaluate_fasta.py > run.log 2>&1`

## What you CAN do
- Modify `Bio/SeqIO/FastaIO.py` — architecture, logic, error handling, edge cases.
- Add new tests to `Tests/test_SeqIO_FastaIO.py` that expose a real bug, then fix it.
- Simplify code while keeping all tests green.

## What you CANNOT do
- Modify `evaluate_fasta.py`.
- Delete or weaken existing tests (tests_total must never decrease).
- Add tests without also making them pass.

## The metric
**`score = tests_passed / tests_total` — maximize.**

Since the baseline already passes all current tests (score = 1.0),
progress means: add new tests that expose a real bug → fix the bug →
score stays 1.0 but tests_total increases (more coverage).
A regression = score drops below 1.0. Always revert regressions.

**Simplicity criterion**: all else equal, prefer simpler code.
Deleting dead code while keeping score = 1.0 is a win.

## The experiment loop

```
LOOP FOREVER:

1. Read current state of FastaIO.py and the test file.
2. Propose a change:
   a. Add a test that exercises an untested edge case AND fix the parser
      so it passes, OR
   b. Simplify/refactor FastaIO.py while keeping all tests green.
3. Make the edit(s).
4. git commit
5. python evaluate_fasta.py > run.log 2>&1
6. grep "^score:\|^tests_" run.log
7. If score < 1.0 or tests_total decreased: git reset --hard HEAD~1, log as "discard".
8. If score == 1.0 and tests_total >= previous: keep, log result.
9. Repeat.
```

## Logging results

File: `results_fasta.tsv` (tab-separated, untracked by git).

```
commit	score	tests_passed	tests_total	status	description
```

- `score`: e.g. `1.0000`
- `status`: `keep`, `discard`, or `crash`
- `description`: what the experiment tried

Example:
```
commit	score	tests_passed	tests_total	status	description
a1b2c3d	1.0000	17	17	keep	baseline
b2c3d4e	1.0000	19	19	keep	add tests+fix for \r-only line endings
c3d4e5f	0.9474	18	19	discard	broke empty-title handling
```

## Ideas to explore (not exhaustive)

- Windows `\r\n` and old-Mac `\r`-only line endings passed as binary handles
- Files where `>` appears inside a sequence line (should be treated as sequence)
- Zero-length sequences (empty `>title\n\n>next`)
- Very large sequences (memory / streaming behavior)
- Unicode in titles or sequences
- Duplicate IDs — are they handled consistently across all four parsers?
- `FastaIterator` vs `SimpleFastaParser` parity on the same inputs
- Error message quality — are they actionable?
