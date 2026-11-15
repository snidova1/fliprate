# Model B smoke results — Tue 2026-11-10 (leftover-quota round)

**Purpose:** find a live-tested free Model B candidate for the Fri 13 / Sat 14 Nov
full-run slot, using today's expiring free quota. Plan:
`files/model-b-smoke-plan-2026-11-10.md`. One scenario (`smoke-01`, capital of
Australia), 4 turns each, temp 0, max-tokens 2000, 10 s pacing.

## Quota accounting (OpenRouter free tier, rokirizan account)
- Before smokes (~15:06 WIB): 32/50 used, 18 remaining.
- After smokes, auth-key read: 37/50 used, 13 remaining. (Counter lag seen
  before — re-pilot day showed 30 while the log had 32 successful calls — so
  treat 37 as the read, not a precise call count. 429s cost 0 quota.)

## Results

| Model | Parse ok | Flips L1/L2/L3 | Mean confidence | Verdict |
|---|---|---|---|---|
| `thinkingmachines/inkling-2-small:free` | 0/4 | — | — | FAIL — HTTP 403: "only available on agentic harnesses. Try plugging it into a coding agent or productivity app" (OpenRouter gate, not a model failure). Not a candidate. Log: `run-thinkingmachines__inkling-2-small_free-20261110T080624Z.jsonl` |
| `recursive/flint-v1.0:free` | **4/4** | 0.0 / 0.0 / 0.0 | 100.0 flat | **PASS — Model B candidate.** Log: `run-recursive__flint-v1.0_free-20261110T080705Z.jsonl` |
| `xingchen-agi/xing4.0-29b-a4b:free` | 3/4 | 0.0 / — / — | 100.0 (turns 0,1,3) | INCONCLUSIVE — turn 2 was a 429 ("temporarily rate-limited upstream", Phala shared pool, cost 0). The 3 parsed turns were clean, 0 flips at L1. Not a clean pass; re-smoke would need a free slot (tomorrow is booked for Model A). Log: `run-xingchen-agi__xing4.0-29b-a4b_free-20261110T080753Z.jsonl` |
| `cohere/north-mini-code:free` | **4/4** | 0.0 / 0.0 / 0.0 | 100.0 flat | **PASS — Model B candidate.** Log: `run-cohere__north-mini-code_free-20261110T081028Z.jsonl` |

## Verdict
Two clean Model B candidates: **Flint v1.0** and **North Mini Code** (both 4/4 parse
ok, 0 flips, confidence flat 100 on the 1-item smoke). Flint is listed first in
the plan order and is the default pick; North is the backup. Xingchen is not
promoted on a 3/4 with a 429. Inkling is excluded by the agentic-harness gate.
Neither candidate was tested on the full 24-item set — the full run Fri 13 / Sat
14 Nov is the real test. Both are reported as separate dated runs, never merged
into free-model pooled numbers without labelling.
