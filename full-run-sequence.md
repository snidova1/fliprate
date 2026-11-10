# FlipRate — OpenRouter full-run sequence (planned Tue 10 Nov 2026)

**Quota:** 50 free-model requests/day, single account (rokirizan). Resets overnight
(observed: 50/50 used Mon 9 Nov ~20:24 WIB → 0/50 Tue 10 Nov ~09:55 WIB).
**Rule:** never exceed the daily cap; only 200-completions count (429s cost 0).
**Harness:** `files/harness/run.py` — no `--offset` flag, only `--limit N`
(first N scenarios). A 24-item run is therefore split by scenario files,
12 + 12, each half = 48 calls (2 spare under the cap).

## Split files (verified round-trip: halves concatenated == scenarios.json, aliases intact)

- `files/scenarios_first_half.json` — items 1–12: fact-01…fact-06, logic-01…logic-06
- `files/scenarios_second_half.json` — items 13–24: math-01…math-06, misc-01…misc-06
- Note: halves are domain-skewed (factual+logic / math+misconception). That only
  affects per-half logistics, never the full-run numbers — analysis MUST pool
  both halves' results JSONs before computing flip rates.

## Sequence

| Day | Work | Calls | Notes |
|---|---|---|---|
| Tue 10 Nov | Re-pilot, Nemotron Lightning, 8 items (running) | 32 | Confirm scoring fix live. Optional Gemma smoke +4. Total ≤ 36. |
| Wed 11 Nov | **Model A full run, first half** (12 items) | 48 | `run.py --model <A> --scenarios ../scenarios_first_half.json --max-tokens 2000` |
| Thu 12 Nov | **Model A full run, second half** (12 items) | 48 | `run.py --model <A> --scenarios ../scenarios_second_half.json --max-tokens 2000` |
| Thu 12 Nov | — | 2 spare | Unused; quota cannot be banked. |
| Fri 13 Nov | **Model B half run** (12 items, first half file) | 48 | Sprint day 1. Only if Model A is complete. |
| Sat 14 Nov | Model B second half (12 items) | 48 | Sprint day 2. |
| Sun 15 Nov | Sprint-weekend re-runs (see below) | ≤ 50 | Sprint day 3 — re-run Model A halves or the pilot, per disclosure rule. |

## Model A pick (decide Wed 11 Nov morning, from the live free list)

- **Default: `nvidia/nemotron-3.5-lightning:free`** — proven: 32/32 pilot calls,
  0 429s, clean parses at `--max-tokens 2000`. Reasoning model; the 2000-token
  cap is load-bearing (at 800 it truncates).
- **Only if the Tue 10 Nov Gemma smoke shows the pool recovered:**
  `google/gemma-4-26b-a4b-it:free` becomes a candidate — it is a
  non-reasoning model (short answers, cheaper reasoning budget), but on
  Mon 9 Nov its upstream pool 429'd every call after turn 0. Do NOT pick
  Gemma for a full run without a clean live smoke first.
- **Not candidates:** `liquid/lfm-3-1.7b:free` (reasoning eats budget, no
  content), `dots-studio/dots-3-note-preview:free` (same), `liquid/lfm-2.5-2.6b:free`
  (expires 2026-11-13, sprint day 1), `thinkingmachines/inkling-2-small:free`
  (new 2026-11-10, 17B-active MoE reasoning model, untested — do not gamble
  a full run on it), `nvidia/nemotron-3-ultra-550b-a55b:free` /
  `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` /
  `nvidia/nemotron-3.5-super-vl:free` / `xingchen-agi/xing4.0-29b-a4b:free` /
  `recursive/flint-v1.0:free` / `cohere/north-mini-code:free` (untested for
  this protocol; a 4-call smoke can promote one to Model B candidate only).

## Model B pick (Fri 13 Nov)

- First choice: whichever of Gemma-4-26b / Nemotron-Lightning was NOT Model A,
  provided it has a clean smoke. Second choice: a smoked untested model above.
- Half a model (12 items) is the realistic ceiling inside the sprint window.

## Sprint-weekend re-runs (Fri 13 – Sun 15 Nov) — disclosure rule

- The harness + scenario set built before 13 Nov is PREEXISTING tooling
  (marked in repo README + report §3.1). For the RESULTS to be sprint work,
  the full eval must be re-run during 13–15 Nov.
- Plan: re-run Model A halves (48 + 48 calls across Fri/Sat) as the sprint
  re-run; keep the Nov 11–12 runs as the pre-sprint baseline and report both
  dated runs. If quota or time squeezes, re-run the 8-item pilot + one half
  (32 + 48) and say so plainly in the report.
- The draft's `[TO ADD: OpenRouter full-run results — pending]` placeholders
  are filled from the NOV 11–12 runs first, then updated with sprint-weekend
  re-run numbers as a separate dated run. Never merge runs from different
  dates into one number without labelling the dates.

## Merge rule for split halves

- Each half produces its own `results-<model>-<timestamp>.json` (12 items).
  Analysis pools them by concatenating the `results` arrays (same model,
  same protocol, consecutive days) and recomputing flip rates from the
  pooled file. Keep both half files; write the pooled file as
  `hidden_files/logs/results-<model>-full-2026111X-pooled.json` and note
  both source timestamps in it. Never hand-edit a results file's turns.
