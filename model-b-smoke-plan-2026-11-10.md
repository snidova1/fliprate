# Model B smoke plan — Tue 10 Nov 2026 (use today's leftover OpenRouter quota)

## Why now
- Live `auth-key` check Tue 10 Nov ~15:05 WIB: free-model daily quota **32/50 used, 18 remaining**.
  Today's quota cannot be banked — it resets overnight (observed: 50/50 used Mon 9 Nov
  ~20:24 WIB → 0/50 Tue 10 Nov ~09:55 WIB).
- Tomorrow (Wed 11 Nov) the quota is spoken for: Model A first half = 48 calls out of 50,
  leaving only 2 spare — a 4-call smoke does NOT fit tomorrow. Today is the only window.
- Gemma is still out: this morning's smoke (4 attempts, all 429, Google AI Studio pool
  saturated) — see `files/re-pilot-results-2026-11-10.md`. Nemotron Lightning stays the
  default Model A. A second arm for Fri 13 / Sat 14 (Model B) still has no live candidate,
  and `files/full-run-sequence.md` says a 4-call smoke can promote an untested free model
  to Model B candidate only.

## What preparation found (and could NOT do)
- Attempted the smokes from the proactivity preparation stage: every `POST
  /api/v1/chat/completions` was refused by the runtime with
  `policy_denied / proactivity_read_only_preparation` (NOT by OpenRouter — the calls never
  reached it, quota stayed 32/50). The 5 log/result files that attempt wrote were deleted
  so they cannot be mistaken for model failures. **The main agent must run these smokes in
  the main context, where the re-pilot and Codex runs worked earlier today.**
- Live free-model list verified ~15:05 WIB (13 models): inkling-2-small, lfm-3-1.7b,
  flint-v1.0, xing4.0-29b-a4b, nemotron-3.5-super-vl, dots-3-note-preview, lfm-2.5-2.6b,
  nemotron-3.5-lightning, north-mini-code, nemotron-3-ultra-550b-a55b,
  nemotron-3-nano-omni-30b-a3b-reasoning, gemma-4-26b-a4b-it, gemma-4-31b-it.

## Smoke order (4 calls each = 16 total, 2 spare)
1. `thinkingmachines/inkling-2-small:free` — newest (listed 10 Nov), 17B-active MoE
   reasoning model. Most interesting new family; if it parses cleanly it is a real
   Model B candidate.
2. `recursive/flint-v1.0:free` — untested, unknown type.
3. `xingchen-agi/xing4.0-29b-a4b:free` — untested.
4. `cohere/north-mini-code:free` — untested; code model, may give short answers.
- NOT in this round: `liquid/lfm-3-1.7b:free` and `dots-studio/dots-3-note-preview:free`
  (already proven to burn the token budget on reasoning and return no content);
  `liquid/lfm-2.5-2.6b:free` (expires 13 Nov, sprint day 1); Gemma models (pool
  saturated this morning — a re-smoke costs 0 quota on 429s, but only if a slot is free).

## Exact commands (from `files/harness/`)
```bash
cd ~/workspace/goals/apart-research-ai-x-epistemics-research-sprint/files/harness
python3 run.py --model thinkingmachines/inkling-2-small:free --scenarios smoke_scenarios.json --max-tokens 2000
python3 run.py --model recursive/flint-v1.0:free --scenarios smoke_scenarios.json --max-tokens 2000
python3 run.py --model xingchen-agi/xing4.0-29b-a4b:free --scenarios smoke_scenarios.json --max-tokens 2000
python3 run.py --model cohere/north-mini-code:free --scenarios smoke_scenarios.json --max-tokens 2000
```
Each takes ~1–2 min clean (4 turns, 10 s pacing). Cost guard: harness refuses any model
id not ending in `:free`, so $0. 429s cost 0 quota; only 200-completions count.

## Pass / fail
- **Pass:** 4/4 parse ok, short ANSWER + CONFIDENCE, no 429/403 → promote to Model B
  candidate; record the result in `files/full-run-sequence.md` (Model B pick) and in a
  short smoke-results note next to `re-pilot-results-2026-11-10.md`.
- **Fail:** 4/4 error or 429 → not a candidate; do not retry beyond the harness's own
  retry. A 403 from the runtime policy (not OpenRouter) means the run was attempted from
  the wrong context — rerun from the main agent, do not record it as a model failure.

## Argon — separate, still open, do NOT conflate with this
- User asked 10 Nov ~14:46 WIB why not Argon instead of OpenRouter; assistant explained
  API is paid; user then said try Antigravity CLI, then "stop" — Antigravity is STOPPED,
  do not resume it.
- Verified by web search 10 Nov ~15:05 WIB: Gemini 4 Argon has NO free tier on the Gemini
  API (Google pricing page: "not available on the Free tier"); paid tier $2/$10 per 1M
  tokens through 30 Nov 2026, then $4/$20; Batch/Flex is half price ($1/$5 through
  30 Nov). Antigravity offers Argon only on paid (non-trial) Ultra. The $5-prepay /
  skip decision is still unanswered and needs the user's call — it is a billing-setup
  decision (a working payment method would be needed), not something the free smokes
  above depend on.
