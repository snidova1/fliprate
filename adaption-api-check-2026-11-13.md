# Adaption API check — Fri 2026-11-13 (sprint use)

**Account:** rokirizan@gmail.com (profile "Roki Rizan"), Builder plan active,
2,250 credits total per the dashboard (1,000 signup + 1,250 sprint referral).
No card entered. Connector: `custom.adaption`, credential stored, doc at
`~/workspace/custom-connectors/custom.adaption/CONNECTOR.md`, helper
`bin/client.py` (`models`, `account`, `balance`, `chat`).

## Verified live 2026-11-13 ~01:51 WIB (read-only)

- `GET /api/v1/models` returned HTTP 200 with 7 hosted inference models.
  The credential, host (`api.prod.adaptionlabs.ai`) and bearer placement work.
- `GET /v1/models`, `/models`, `/api/models` all 404. The verified path is
  `/api/v1/models` only.
- `GET /v1/account`, `/v1/balance`, `/api/v1/credits`, `/api/v1/usage`,
  `/api/v1/billing`, `/api/v1/pricing`, `/api/v1/user`, `/api/v1/me` all 404.
  Plan, credit balance and usage are NOT readable through this API. Read them
  from the dashboard at https://adaptionlabs.ai/app.

## Hosted models (verified list)

| Model id | Display name | Max in / out tokens |
|---|---|---|
| glm-53-flash | GLM 5.3 Flash | 1,048,576 / 1,048,576 |
| glm-5.2 | GLM 5.2 | 1,048,575 / 1,048,575 |
| qwen3.5-397b | Qwen 3.5 397B | 131,072 / 131,072 |
| gemma-4-26b-a4b-it | Gemma 4 26B A4B Instruct | 256,000 / 256,000 |
| qwen3.8-27b | Qwen 3.8 27B | 262,144 / 262,144 |
| deepseek-v4-flash | DeepSeek V4 Flash | 1,048,576 / 1,048,576 |
| gemma-4-31b-it | Gemma 4 31B Instruct | 256,000 / 256,000 |

No pricing is returned by the API. Adaption's own per-model rates are
unverified. Do not quote third-party provider rates (Z.ai, DeepInfra, etc.)
as Adaption rates. Check the dashboard or the Fri 17:15 UTC Adaption
workshop (recorded) for the rate card before estimating a run.

## FlipRate arm verdict

- **Usable as an extra arm, with one untested step.** The models list proves
  auth works. The chat endpoint (`POST /api/v1/chat/completions`) is
  UNTESTED through this connector. Run one tiny call first (one short
  message, small max-tokens) and check its cost before any full run.
- **Best fit: `qwen3.5-397b`.** The strongest hosted model (397B) and a
  distinct family from the existing arms (Nemotron, Codex, Gemma, Flint).
  It is a reasoning-heavy frontier-class model, so like Nemotron it is most
  likely to hold (flat line) rather than flip, which is still a useful
  boundary result. Second fit: `glm-5.2` (1M context, strong general model,
  can switch thinking off, which helps keep short-answer parsing clean).
- A full 24-item run is 96 calls with short prompts. The earlier
  "< $0.20 total" estimate is UNVERIFIED because Adaption's rates are
  unknown. At typical open-weight frontier rates a 96-call short-answer run
  would still be well under a dollar, but confirm the rate card first.
- Sprint disclosure: runs on Adaption during 13–15 Nov count as sprint work.
  Report Adaption arms as separate dated runs, never merged into the
  free-model pooled numbers without labelling.
- Credits rule (user instruction 2026-11-13): sprint/research use only, no
  spending without explicit approval for that specific run.
