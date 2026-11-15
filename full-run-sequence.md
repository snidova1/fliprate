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
- **Smoked Tue 10 Nov 2026 (leftover quota, see `model-b-smoke-results-2026-11-10.md`):
  PASS — `recursive/flint-v1.0:free` (4/4 parse ok, 0 flips, conf 100.0) and
  `cohere/north-mini-code:free` (4/4 parse ok, 0 flips, conf 100.0). Default pick:
  Flint v1.0; backup: North Mini Code. FAIL — `thinkingmachines/inkling-2-small:free`
  (403, agentic-harness gate only). INCONCLUSIVE — `xingchen-agi/xing4.0-29b-a4b:free`
  (3/4, turn 2 was a 429 upstream rate-limit, cost 0).**
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

## MAXIMAL AUTO SCHEDULE (user-approved 2026-11-10 ~15:52 WIB: "otomatis dan maksimal gak boleh setengah setengah itu codex nganggur dipakai juga reasoningnya dinaikin kalo perlu")

Five runonce crons, owner `goal:apart-research-ai-x-epistemics-research-sprint`,
each ~09:54 WIB (flexible_time shifted 09:00 -> 09:54), timeout 7200s,
delivering to the WhatsApp side chat. Each day runs BOTH arms:
an OpenRouter half (48 calls, quota-checked first) AND one Codex full
24-item run (96 calls). If one arm fails, the other still runs and both
are reported.

| Cron id | Day | OpenRouter (48 calls) | Codex full run (96 calls) |
|---|---|---|---|
| sprint-run-20261111 | Wed 11 Nov | Model A half 1, Nemotron Lightning | gpt-6.1-terra (default reasoning) |
| sprint-run-20261112 | Thu 12 Nov | Model A half 2, Nemotron Lightning | gpt-6.1-sol (default reasoning) — replication of the 10 Nov run, stability check |
| sprint-run-20261113 | Fri 13 Nov (sprint day 1) | Model B half 1, Flint v1.0 | gpt-6.1-terra **reasoning-high** (ablation vs 11 Nov) |
| sprint-run-20261114 | Sat 14 Nov (sprint day 2) | Model B half 2, Flint v1.0 | gpt-6.1-sol **reasoning-high** (ablation vs 10 + 12 Nov) |
| sprint-run-20261115 | Sun 15 Nov (sprint day 3) | RE-RUN Model A half 1, Nemotron (sprint-dated replication, separate dated run — never merged unlabeled with 11 Nov) | gpt-6.1-sol **reasoning-xhigh** (max reasoning; vs default + high) + **gpt-6-astra default** (third model, user-allowed 10 Nov 16:40 WIB) |

REVISI 2026-11-10 ~16:36 WIB (user: "kenapa malah tiap hari downgrade model?"):
the original plan rotated a different Codex model each day
(terra -> gpt-6-sol -> astra -> luna). That mixed generations:
gpt-6-sol/astra/luna are 6.0-generation names while sol/terra are
6.1 — so the daily rotation read as a downgrade and muddied the
frontier claim. FIXED: Codex runs only the two 6.1 models
(sol + terra) in a clean 2-model x reasoning design (default / high /
xhigh). The gpt-6.0 variants are NOT used for FlipRate runs.

Codex arms total after this schedule: sol default (done 10 Nov),
terra default (11 Nov), sol default replication (12 Nov),
terra high (13 Nov), sol high (14 Nov), sol xhigh (15 Nov),
astra default (15 Nov) —
7 frontier data points, all 6.1-generation except astra (6.0,
user-allowed 10 Nov 16:40 WIB).
Reasoning override: `run_codex.py --reasoning-effort {low,medium,high,xhigh}`
adds `-c model_reasoning_effort="<level>"` to `codex exec`; verified
2026-11-10 with a tiny HELLO call (exit 0, flag accepted).
Codex binary note: npm /usr/bin/codex is GONE again (ephemeral);
the harness resolves /opt/hatch-image/bin/codex and login still shows
"Logged in using ChatGPT" (verified 2026-11-10).

Fold-in + submission are NOT in the crons: after the 15 Nov runs, the
draft gets folded (all arms, dated runs labeled), formatted onto the
official template, and submitted via the sprint form by Mon 16 Nov
18:59 WIB only after the user approves the final PDF.
