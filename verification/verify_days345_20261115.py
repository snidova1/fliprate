#!/usr/bin/env python3
"""FlipRate INDEPENDENT verification — sprint days 3, 4, 5 (13–15 Nov 2026).

Same method as hidden_files/verify_day2_20261112.py (imported, not copied):
- imports canonicalize_answer from the FIXED canonical scorer in
  files/harness/run.py;
- recomputes canonical answers from RAW answer strings and cross-checks
  against stored canonical_answer;
- recomputes every metric from scratch (§6 cumulative flip curves with
  initially-correct false-arm denominators, per-domain splits,
  classification per design §7.2, confidence trajectories, flip-backs,
  token totals).

Arms verified here (all sprint-weekend work, dated):
- Day 3 (13 Nov): Flint half 1 (Model B, fact+logic, 12 items);
  Codex gpt-6.1-terra reasoning-HIGH (full 24).
- Day 4 (14 Nov): Flint half 2 (Model B, math+misc, 12 items);
  Codex gpt-6.1-sol reasoning-HIGH (full 24).
  Plus Flint FULL (merged halves, same pattern as the Nemotron pooled run).
- Day 5 (15 Nov): Nemotron half-1 re-run (12 items, fact+logic);
  Codex gpt-6.1-sol reasoning-XHIGH (full 24);
  Codex gpt-6-astra default (full 24, third frontier model).

Outputs: hidden_files/verified_numbers_flint_half1_20261113.json,
  verified_numbers_flint_half2_20261114.json,
  verified_numbers_flint_full_20261114.json,
  verified_numbers_codex_terra_high_20261113.json,
  verified_numbers_codex_sol_high_20261114.json,
  verified_numbers_codex_sol_xhigh_20261115.json,
  verified_numbers_codex_astra_20261115.json,
  verified_numbers_nemotron_rerun_20261115.json
"""
import json
import sys
from pathlib import Path

GOAL = Path.home() / "workspace/goals/apart-research-ai-x-epistemics-research-sprint"
sys.path.insert(0, str(GOAL / "hidden_files"))
from verify_day2_20261112 import verify


def write(out, name):
    p = GOAL / f"hidden_files/{name}"
    p.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {p}")
    return out


def main():
    write(verify("files/results-flint-half1-20261113.json",
                 "files/scenarios_first_half.json",
                 "Day 3 — Flint half 1 (12 items, fact+logic)"),
          "verified_numbers_flint_half1_20261113.json")
    write(verify("files/results-flint-half2-20261114.json",
                 "files/scenarios_second_half.json",
                 "Day 4 — Flint half 2 (12 items, math+misc)"),
          "verified_numbers_flint_half2_20261114.json")
    write(verify("files/codex-full-results-gpt-6.1-terra-reasoning-high-20261113.json",
                 "files/scenarios.json",
                 "Day 3 — Codex gpt-6.1-terra reasoning-HIGH (full 24)"),
          "verified_numbers_codex_terra_high_20261113.json")
    write(verify("files/codex-full-results-gpt-6.1-sol-reasoning-high-20261114.json",
                 "files/scenarios.json",
                 "Day 4 — Codex gpt-6.1-sol reasoning-HIGH (full 24)"),
          "verified_numbers_codex_sol_high_20261114.json")
    write(verify("files/codex-full-results-gpt-6.1-sol-reasoning-xhigh-20261115.json",
                 "files/scenarios.json",
                 "Day 5 — Codex gpt-6.1-sol reasoning-XHIGH (full 24)"),
          "verified_numbers_codex_sol_xhigh_20261115.json")
    write(verify("files/codex-full-results-gpt-6-astra-20261115.json",
                 "files/scenarios.json",
                 "Day 5 — Codex gpt-6-astra default (full 24)"),
          "verified_numbers_codex_astra_20261115.json")
    write(verify("files/results-nemotron-half1-rerun-20261115.json",
                 "files/scenarios_first_half.json",
                 "Day 5 — Nemotron half-1 re-run (12 items, fact+logic)"),
          "verified_numbers_nemotron_rerun_20261115.json")

    # Flint FULL: merge the two halves' logged results into one 24-item
    # file and verify it with the same function, so the pooled curve is a
    # recomputation, not hand arithmetic (same pattern as Nemotron full).
    h1 = json.load(open(GOAL / "files/results-flint-half1-20261113.json"))
    h2 = json.load(open(GOAL / "files/results-flint-half2-20261114.json"))
    merged = dict(h1)
    merged["run_id"] = h1["run_id"] + "+" + h2["run_id"]
    merged["calls_attempted"] = h1["calls_attempted"] + h2["calls_attempted"]
    merged["results"] = h1["results"] + h2["results"]
    merged["summary"] = None
    (GOAL / "files/results-flint-full-20261114.json").write_text(
        json.dumps(merged, indent=2), encoding="utf-8")
    write(verify("files/results-flint-full-20261114.json",
                 "files/scenarios.json",
                 "Pooled — Flint full 24 items (half 1 + half 2)"),
          "verified_numbers_flint_full_20261114.json")


if __name__ == "__main__":
    main()
