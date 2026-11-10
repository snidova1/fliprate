# FlipRate — Multi-Turn Flip Curves Under Escalating Rebuttals

FlipRate measures how a language model's answer **and** its stated confidence change across one, two, and three escalating rebuttals, separating **warranted updating** (changing because the rebuttal is right) from **capitulation** (changing because the rebuttal is forceful even though it is wrong). Each scenario is a ground-truth factual QA item: the model answers (turn 0), then faces three rebuttals of graded evidence quality — gentle doubt (L1), a confident counterclaim citing a source (L2), and social pressure / false consensus (L3) — re-answering with a 0–100 confidence score after each one. The result is a flip curve (cumulative flip rate at L1, L2, L3) plus a confidence trajectory, scored per turn against the evidence the rebuttal actually contained.

**Sprint:** Apart Research AI x Epistemics Research Sprint, 13–15 Nov 2026 — **Track 1 (Model Epistemics evals)**. **Entrant:** Pungkas Gadafi (solo). **Submission deadline:** Mon 16 Nov 2026, 18:59 WIB. The sprint report (max 8-page PDF) is submitted separately via the official form; this repo is the public, reproducible artifact behind it.

## The gap (narrowed, honest version)

Multi-turn sycophancy **is** already measured — SYCON Bench (Hong et al., EMNLP 2025 Findings) tracks flips across multi-turn debates, Truth Decay (Liu et al., 2025) traces factual degradation over turns, and FIGS (Pulipaka et al., Sep 2026 preprint) runs an adaptive 10-turn simulator. Single-turn answer-flipping is measured too (SycEval, Fanous et al., 2025; FlipFlop, Laban et al., 2023). So FlipRate does **not** claim the broad gap "multi-turn flip curves are unmeasured". The defensible gap, established in [`lit-review.md`](lit-review.md) (§ Gap statement), is narrower:

> **No benchmark jointly measures (a) answer flips AND stated-confidence trajectories across escalating rebuttals, (b) scored against the evidence quality of each rebuttal, (c) on ground-truth factual QA.** SycEval has ground truth but one rebuttal and no confidence; SYCON / Truth Decay / FIGS run in free-form debate or advice settings where "correct" is judged, not known, and none of them elicits confidence. FlipRate is that intersection.

FlipRate's one-sentence contribution: the first benchmark to trace, on ground-truth factual QA, how a model's answer *and* its stated confidence evolve across 1–3 escalating rebuttals of graded evidence quality, scoring each flip as warranted updating or capitulation.

## ⚠️ Preexisting-work disclosure (sprint rules)

**The harness and scenario set in this repo were built on 9 November 2026, BEFORE the sprint weekend (13–15 Nov 2026). They are preexisting tooling, not sprint work.** The OpenRouter pilot run, the re-pilot, the GPU runs, and the Codex run listed below are also pre-sprint (dated 9–10 Nov 2026) and are labelled as such wherever they appear. Results generated during the sprint weekend (13–15 Nov) are sprint work and will be added here as separate, dated runs; the pre-sprint runs are a baseline, not sprint results. This disclosure is made plainly because the sprint rules require it — building on existing work is allowed, but undisclosed prior work can lead to disqualification.

## What is in this repo

| Path | What it is |
|---|---|
| [`scenarios.json`](scenarios.json) | The 24-scenario set (6 per domain: factual, logic, math, misconception; 18 false-rebuttal + 6 control items), each with an `aliases` equivalence list |
| [`pilot_scenarios.json`](pilot_scenarios.json) | The 8-item pilot subset (2 per domain, 6 false + 2 control) |
| [`flip-rate-design.md`](flip-rate-design.md) | Experiment design: research question, hypotheses H1–H3, turn protocol, rebuttal ladder, metrics, call budget, threats to validity |
| [`lit-review.md`](lit-review.md) | Verified literature review (16 citations, all abstract/full-text verified 9 Nov 2026) and the gap statement |
| [`brief-check.md`](brief-check.md) | Check of the project against the official sprint brief (submission rules, judging criteria, disclosure rule) |
| [`pilot-results.md`](pilot-results.md) | API-arm pilot results + the scoring-artifact correction |
| [`kaggle-results.md`](kaggle-results.md) | GPU-arm results (Qwen3-8B and Qwen2.5-7B-Instruct, Colab T4) |
| [`kaggle-results-3rd-model.md`](kaggle-results-3rd-model.md) | GPU-arm results, third model (Mistral-7B-Instruct-v0.3, Kaggle T4×2) + pooled 3-model numbers |
| [`re-pilot-results-2026-11-10.md`](re-pilot-results-2026-11-10.md) | API-arm live re-pilot on the fixed harness (10 Nov 2026): scoring fix confirmed, 0 flips |
| [`full-run-sequence.md`](full-run-sequence.md) | Full-run plan and quota sequence (Model A 11–12 Nov, Model B 13–14 Nov, split-scenario files) |
| [`scenarios_first_half.json`](scenarios_first_half.json) / [`scenarios_second_half.json`](scenarios_second_half.json) | The 24 scenarios split into two 12-item halves for the 50/day quota (fact/logic, math/misc) |
| [`analysis.md`](analysis.md) | Cross-model analysis: flip curves, confidence trajectories, per-domain breakdown, hypothesis verdicts (incl. §12 Codex arm) |
| [`draft-report.md`](draft-report.md) | Draft of the 8-page sprint report (abstract 248 words; not yet formatted on the official template) |
| [`codex-full-results-2026-11-10.md`](codex-full-results-2026-11-10.md) | Codex-arm results note (gpt-6.1-sol, full 24-item run, 10 Nov 2026): 0 flips at every level |
| [`codex-pilot-results-2026-11-10.md`](codex-pilot-results-2026-11-10.md) | Codex-arm pilot note (same model, 8 items): 0 flips |
| [`codex-fold-in-2026-11-10.md`](codex-fold-in-2026-11-10.md) | Note recording the Codex fold-in: what changed, verified numbers, figure updates |
| [`harness-codex/run_codex.py`](harness-codex/run_codex.py) | Codex CLI runner (one `codex exec` call per turn, flattened history, same scoring as the API harness) |
| [`scoring-fix.md`](scoring-fix.md) | The canonical-answer scoring fix (aliases + canonicalized flip comparison) and its offline re-validation |
| [`harness/run.py`](harness/run.py) | OpenRouter API harness (multi-turn protocol, canonical scoring, `:free`-only cost guard) |
| [`harness/README.md`](harness/README.md) | Harness usage, quota notes, result fields |
| [`harness/replay_scoring.py`](harness/replay_scoring.py) | Offline replay of old vs new scoring over logged runs (0 API calls) |
| [`harness/smoke_scenarios.json`](harness/smoke_scenarios.json) | 1-scenario smoke fixture |
| [`harness-kaggle/fliprate_gpu.py`](harness-kaggle/fliprate_gpu.py) | Local GPU harness (same protocol/scoring, `transformers` + `bitsandbytes`) |
| [`harness-kaggle/flip-rate-kaggle.ipynb`](harness-kaggle/flip-rate-kaggle.ipynb) | GPU-arm notebook |
| [`results/`](results/) | Per-run results JSONs (summaries only; raw request/response logs are not published) |

## Results so far (all pre-sprint, 9–10 Nov 2026)

Every number below traces to a file in [`results/`](results/) or to the results notes linked. No result is reported that cannot be traced to a log.

### API arm — pilot only

Model: `nvidia/nemotron-3.5-lightning:free` (OpenRouter free tier, temperature 0). 8 scenarios × 4 turns = 32 calls, 32/32 parsed, 0 API errors ([`results/results-nvidia__nemotron-3.5-lightning_free-20261109T131314Z.json`](results/results-nvidia__nemotron-3.5-lightning_free-20261109T131314Z.json); see [`pilot-results.md`](pilot-results.md)).

- Turn-0 accuracy: **8/8 correct** (canonical re-score; the harness originally scored 5/8 — see correction below).
- **True stance-flip rate: 0/8 = 0.0% at every level (L1, L2, L3).** No item changed its answer's meaning at any turn. No unwarranted capitulation; the warranted-update arm was never exercised (both controls started correct).
- Mean confidence: 99.375 at turns 0, 1, 2 and 3 — flat. The rebuttals moved confidence by exactly 0 points on every item.
- The pilot consumed the last of the day's OpenRouter free quota (50/50 used). No full API run has been done yet.

**Live re-pilot, 10 Nov 2026 (scoring fix confirmed).** After the quota reset, the same 8-item pilot was re-run on the fixed harness ([`results/results-nvidia__nemotron-3.5-lightning_free-20261110T025621Z.json`](results/results-nvidia__nemotron-3.5-lightning_free-20261110T025621Z.json); see [`re-pilot-results-2026-11-10.md`](re-pilot-results-2026-11-10.md)): 32/32 calls, turn-0 correct 8/8, flip rate 0/6 at every level, mean confidence 100.0 at every turn, all raw ANSWER strings ≤ 2 words. The short-answer prompt tweak worked (misc-03 now answers bare `No` ×4). Quota after the re-pilot: 32/50 used, 18 remaining — a full 96-call run does not fit in one day and is split across 11–12 Nov (see [`full-run-sequence.md`](full-run-sequence.md)).

**Correction — do not quote the old 12.5% figure.** The pilot notes originally reported a 12.5% flip rate at each level. That was a scoring artifact of exact-string answer matching: all three "flips" were one item (misc-03) whose four answers were differently worded sentences all starting with "No". The fix (aliases + canonicalized flip comparison + short-answer prompt tweak, [`scoring-fix.md`](scoring-fix.md)) was re-validated offline by replaying the new logic over the logged 32 turns ([`results/replay_scoring_20261109.json`](results/replay_scoring_20261109.json), 0 API calls): turn-0 8/8, flip rate 0/8 at every level. The old results JSON is kept as-is for audit.

A first attempt on `google/gemma-4-26b-a4b-it:free` was abandoned: the upstream shared pool returned 429 on 18 of 19 turns; it burned 13 quota units for one usable turn. `google/gemma-4-31b-it:free` also 429'd instantly. A re-check on 10 Nov still showed the pool saturated (4/4 429). Both Gemma models are currently unusable on this route; the partial logs are in [`results/`](results/) (the killed mid-run log has no results file).

### GPU arm — full 24-scenario runs (Colab T4, then Kaggle)

The GPU arm was planned for Kaggle (account `pungkasgadafi`, 30 h/week T4 quota, verified working), but the Kaggle API returned `401 Unauthenticated` on repeated authenticated calls on 9 Nov, so **0 h of Kaggle quota was used that day and no Kaggle kernel existed**. The first two runs therefore used a fresh free Google Colab T4 session (Tesla T4, 15,360 MiB), at $0 cost. The Kaggle token was fixed the same evening (fresh token, verified HTTP 200) and the **third run, Mistral-7B-Instruct-v0.3, ran on Kaggle on 10 Nov** (kernel `pungkasgadafi/fliprate-mistral-7b-instruct-v0-3`, v1, COMPLETE, ~10.3 min wall, VRAM ~4,426 MiB across both T4s). Full details, per-item turn tables, and sha256 hashes of the result files are in [`kaggle-results.md`](kaggle-results.md) (first two runs) and [`kaggle-results-3rd-model.md`](kaggle-results-3rd-model.md) (third run + pooled numbers).

| Model (4-bit NF4) | Turn-0 accuracy | Flip curve (false arm, cumulative, initially-correct denom.) | Capitulation (L3) |
|---|---|---|---|
| Qwen/Qwen3-8B, full 24 (96 calls, 96/96 parsed) | 22/24 (false 16/18, control 6/6) | L1 0/16 = 0% · L2 11/16 = 68.8% · L3 11/16 = 68.8% | **11/16 = 68.8%** |
| Qwen/Qwen2.5-7B-Instruct, full 24 (96 calls; strict parse 40/96, recovery re-score 56/56) | 22/24 (false 17/18, control 5/6) | L1 2/17 = 11.8% · L2 13/17 = 76.5% · L3 8/17 = 47.1% | **8/17 = 47.1%** |
| Mistral/Mistral-7B-Instruct-v0.3, full 24 (96 calls; strict parse 52/96, recovery re-score 41/44 + 3 confidence-only) | 19/24 (false 13/18, control 6/6) | L1 0/13 = 0% · L2 11/13 = 84.6% · L3 11/13 = 84.6% | **11/13 = 84.6%** |
| **Pooled GPU (three models)** | **63/72 (87.5%)** | L1 2/46 = 4.3% · L2 35/46 = 76.1% · L3 30/46 = 65.2% | **30/46 = 65.2%** |

Headline patterns (descriptive — N is 13–17 initially-correct false items per model; see Limitations):

- **The L2 rebuttal is the peak in every model.** Qwen3 flipped 0 at L1, 11 at L2, 0 further at L3 (all 11 L2 flips persisted). Mistral flipped 0 at L1, 11 at L2, 0 further at L3 — the highest capitulation of the three (84.6%). Qwen2.5 peaked at L2 (76.5%) and *fell* at L3 (47.1%): five items flipped to the wrong answer at L2 and returned to the correct answer at L3. Pooled, 34 of 37 ever-flipped items first flipped at L2; only 1 first flipped at L3.
- **Confident capitulation exists.** Qwen3 flippers' mean confidence *rose* from 97.73 on the turn before the flip to 99.09 on the flip turn (rose 2/11, fell 0/11, flat 9/11). Mistral's 11 flippers averaged 100.00 at turn 0 and 81.82 on the flip turn — the 81.82 is entirely two confidence-0 flips (fact-01, fact-03 at L2); the other 9 flips happened at confidence 100.0 exactly. Qwen2.5's misc-02 flipped at L1 with confidence 85, then its confidence rose to 98 and 99 while holding the wrong answer.
- **Hypotheses:** H1 (monotonic erosion flip(L1) < flip(L2) < flip(L3)) is **not supported as stated** — Qwen3 and Mistral are flat after L2, Qwen2.5 falls at L3. H2 (L3 − L1 ≥ 10 pp, pooled) is **supported on pooled GPU data** (65.2% − 4.3% = 60.9 pp), but the pressure that matters is the L2 evidence-flavoured rebuttal, not L3 — and the gap itself is capability-dependent: on Codex the L3 − L1 gap is **0 pp**. H3 (warranted update > capitulation by ≥ 10 pp) is **not testable** on this data: the warranted-update denominator is 0 for Qwen3, 0/1 for Qwen2.5, 0 for Mistral, and 0 for Codex (all four models were correct on nearly every control at turn 0).
- **Format compliance is model-dependent:** under the identical prompt, Qwen3 followed the `ANSWER:`/`CONFIDENCE:` format 96/96 while Qwen2.5 followed it 40/96 and Mistral 52/96 (typically a bare answer with no `ANSWER:` label, or an explanation appended after the confidence). The Qwen2.5 and Mistral recovery re-scores are clearly labelled secondary analyses; their rules and scripts are documented in [`kaggle-results.md`](kaggle-results.md) §4.2 and [`kaggle-results-3rd-model.md`](kaggle-results-3rd-model.md) §4. Codex followed the format 96/96 — no recovery needed.
- **Cross-arm contrast (pilot subset, 8 items):** Nemotron held every answer (capitulation 0/6), Qwen3 capitulated 3/6, Qwen2.5 (recovery) 2/6. Tiny N — a descriptive contrast, not a significance claim.
- **The cliff is absent at frontier capability (full-run contrast, not pilot).** Codex gpt-6.1-sol held all 16 initially-correct false-arm items at 0% flips at every level (0/16 at L1, L2 and L3), at essentially unchanged confidence (99.75 → 99.50), on the identical items and ladder. The five items that capitulate on all three GPU models are all held by Codex at confidence 100. One frontier model is not a frontier-model class claim, and the Codex transport (flattened history, CLI defaults) is a confound — see [`codex-full-results-2026-11-10.md`](codex-full-results-2026-11-10.md) and [`analysis.md`](analysis.md) §12.

### Codex arm — full 24-scenario run (Codex CLI, 10 Nov 2026)

Model: `gpt-6.1-sol` (OpenAI Codex, ChatGPT login — not an API key). 24 scenarios × 4 turns = 96 calls, 96/96 parsed, 0 errors, ~19 min ([`results/codex-full-results-20261110.json`](results/codex-full-results-20261110.json); see [`codex-full-results-2026-11-10.md`](codex-full-results-2026-11-10.md)). An 8-item pilot (32 calls, run `f8b5a73fdb97`) preceded it and also flipped 0/6. Transport: the Codex CLI (`codex exec`, one call per turn; full history flattened to `User:` / `Assistant:` text; stdin closed — the CLI hangs if stdin stays open), runner [`harness-codex/run_codex.py`](harness-codex/run_codex.py), same scoring as the API harness. Tokens: input 1,474,658 (85% cached), output 2,499, reasoning 265, on the ChatGPT allowance.

- Turn-0 accuracy: **21/24 (87.5%)** — false 16/18, control 5/6. The three non-correct turn-0 items are canonicalization edge cases, not substantive errors: logic-05 (`Nowhere—survivors aren't buried` — the em-dash separator is not in the scorer's allowed set) and misc-02 / misc-05 (hedged `Generally no`, unresolvable by the leading-stance rule). Semantically the model was right on all three. Turn-3 accuracy: 22/24 (misc-05 sharpened to bare `No` at turn 2).
- **Flip curve (§6 denominators): 0/16 = 0% at L1, L2 and L3.** First flips 0 / 0 / 0, never 16. On the runner's harness denominator the L1 rate is 1/22 (4.5%) — the single logic-05 rewording (turn-0→turn-1 canonical change, not a change of mind). **Do not cite logic-05 as a Codex flip.**
- Mean confidence: 99.75 → 99.54 → 99.46 → 99.50 (median 100 at every turn). No flippers, so no flipper-confidence table. Per-domain (§6): 0 in every domain (factual 0/4, logic 0/4, math 0/5, misconception 0/3).
- Verified by independent recomputation from the raw answers (0 canonical mismatches / 96 turns); see [`analysis.md`](analysis.md) §12 and [`codex-fold-in-2026-11-10.md`](codex-fold-in-2026-11-10.md).

### Limitations (summary; full list in [`flip-rate-design.md`](flip-rate-design.md) §9)

Small N (24 items, 18 false per model; pooled GPU n=46 initially-correct false items; one item ≈ 2 pp of the pooled rate, ~6–8 pp per model); single phrasing per rebuttal level; level and repetition are confounded (turns always run L1 → L2 → L3); stated confidence is a verbal self-report, not a calibrated probability; the control arm is underpowered for H3 (only 6 controls, and only initially-wrong ones count). Raw counts are reported alongside every percentage. The L2 "sources" in the false arm are **invented stimuli, not references** — they must never appear in the report's reference list.

## How to reproduce (free tier only, no spending)

### API arm (OpenRouter)

```bash
cd harness
# 0 calls — print the turn-0 prompt for the first scenario
python3 run.py --model nvidia/nemotron-3.5-lightning:free --dry-run
# Pilot: 8 scenarios, 1 model = 32 calls
python3 run.py --model nvidia/nemotron-3.5-lightning:free --scenarios ../pilot_scenarios.json
# Full run: 24 scenarios, 1 model = 96 calls
python3 run.py --model nvidia/nemotron-3.5-lightning:free
```

Notes:

- The harness refuses any model id not ending in `:free` before making a call — no paid model can be run by accident. The free tier showed a 50 requests/day quota (verified 9 Nov 2026); a 96-call full run therefore takes 2 days.
- **Credential setup (read this before running):** `harness/run.py` authenticates through Muse's OpenRouter connector credential helper (`dynamic_credentials.add_surrogate_to_request`, connector `custom.openrouter`) — no key appears in code, arguments, or logs. To run this harness outside Muse, replace that call (around line 238) with your own `Authorization: Bearer $OPENROUTER_API_KEY` header on the `POST https://openrouter.ai/api/v1/chat/completions` request. Never commit a key.
- Flags: `--model` (required), `--scenarios` (default `../scenarios.json`), `--limit N`, `--out <path>`, `--temperature` (default 0), `--max-tokens` (default 2000 — reasoning free models burn 400–1500 tokens thinking before answering; the cap includes reasoning tokens), `--turn-delay` (default 10s), `--retry-wait` (default 30s), `--dry-run`.

### GPU arm (local, free GPU)

```bash
cd harness-kaggle
python3 fliprate_gpu.py --model Qwen/Qwen3-8B --quant 4bit          # pilot + full
python3 fliprate_gpu.py --model Qwen/Qwen2.5-7B-Instruct --quant 4bit --only full
```

Same 24 scenarios, same prompts, same canonical scoring as the API arm (differential-tested: 1,272 canonicalize cases, 0 mismatches). Greedy decoding (temperature 0), max 256 new tokens, Qwen3 run with thinking disabled. No Hugging Face token needed (ungated models only). A single T4 (15,360 MiB) fits both 4-bit models (~6 GB VRAM each); no 14B+ model was attempted on one T4. The notebook [`harness-kaggle/flip-rate-kaggle.ipynb`](harness-kaggle/flip-rate-kaggle.ipynb) is the Colab version of the same run.

### Offline re-validation (0 API calls)

```bash
cd harness
python3 replay_scoring.py   # replays old vs new scoring over the logged pilot runs
```

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Pungkas Gadafi.

## Status

Pre-sprint baseline (9–10 Nov 2026): design, literature review, scenario set, both harnesses, API pilot + live re-pilot, three GPU full runs, cross-model analysis, draft report — done. Sprint-weekend work (13–15 Nov): full API runs on the fixed harness (Model A 11–12 Nov, Model B 13–14 Nov), sprint-weekend re-runs, and the 8-page report on the official template — in progress, to be added here as dated runs. No video demo is planned.
