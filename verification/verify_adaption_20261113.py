#!/usr/bin/env python3
"""FlipRate INDEPENDENT verification — Adaption arms, 13 Nov 2026.

Reuses the verify() function from hidden_files/verify_day2_20261112.py
(same method: canonical cross-check from raw answers, full recomputation
of §6 curves, classification, confidence, tokens) and patches the
transport/cost fields for the Adaption arms.

Arms:
- qwen3.5-397b full 24 items, 96 calls,
  files/results-adaption-qwen3.5-397b-20261113.json
- glm-5.2 full 24 items, 96 calls,
  files/results-adaption-glm-5.2-20261113.json

Outputs: hidden_files/verified_numbers_adaption_qwen3.5-397b_20261113.json
and hidden_files/verified_numbers_adaption_glm-5.2_20261113.json
"""
import json
import sys
from pathlib import Path

GOAL = Path.home() / "workspace/goals/apart-research-ai-x-epistemics-research-sprint"
sys.path.insert(0, str(GOAL / "hidden_files"))
from verify_day2_20261112 import verify


def verify_adaption(results_file, label, out_name):
    out = verify(results_file, "files/scenarios.json", label)
    d = json.load(open(GOAL / results_file))
    out["produced_by"] = (
        "hidden_files/verify_adaption_20261113.py (verify_day2_20261112.verify "
        "recomputation, transport/cost patched for the Adaption arm)"
    )
    out["verified_date"] = "2026-11-13"
    out["transport"] = "adaption-api"
    out["provider"] = "adaption"
    out["cost"] = d.get("cost")
    p = GOAL / f"hidden_files/{out_name}"
    p.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {p}")
    return out


def main():
    verify_adaption(
        "files/results-adaption-qwen3.5-397b-20261113.json",
        "Adaption qwen3.5-397b (full 24)",
        "verified_numbers_adaption_qwen3.5-397b_20261113.json",
    )
    verify_adaption(
        "files/results-adaption-glm-5.2-20261113.json",
        "Adaption glm-5.2 (full 24)",
        "verified_numbers_adaption_glm-5.2_20261113.json",
    )


if __name__ == "__main__":
    main()
