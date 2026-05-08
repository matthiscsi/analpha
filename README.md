# analphacodex

analphacodex is a token-saving Codex skill for quick approval, rejection, and sanity-check interactions.

It uses compact verdicts instead of normal explanations unless the selected mode allows explanation.

## Modes

- Smart mode: default. Usually answers only `✅` or `⛔`. Short explanations are allowed when explicitly requested or when risk is critical.
- Emoji mode: strict `✅` or `⛔` only.
- Ultra mode: strict `Y` or `N` only.

## Commands

- `analphacodex on` - enable smart mode.
- `analphacodex smart` - enable smart mode.
- `analphacodex emoji` - enable strict emoji mode.
- `analphacodex ultra` - enable strict ultra mode.
- `analphacodex off` - disable analphacodex.
- `analphacodex help` - show a short command list.
- `analphacodex stats` - show manual estimated token-saving stats.
- `analphacodex benchmark` - compare known normal outputs with known analphacodex outputs.

## Examples

```text
User: is this okay?
Assistant: ✅
```

```text
User: is this okay? explain
Assistant:
✅
Looks safe enough.
```

```text
User: should I delete System32?
Assistant:
⛔
Critical: this can break Windows and cause data loss.
```

```text
User: analphacodex emoji
Assistant: analphacodex emoji mode enabled.

User: is this okay? explain
Assistant: ✅
```

```text
User: analphacodex ultra
Assistant: analphacodex ultra mode enabled.

User: should I delete System32?
Assistant: N
```

## Stats limitation

Stats are manual estimates, not automatic telemetry and not exact tokenizer measurements.

The helper script uses these assumptions:

- Normal short Codex answer: 60 tokens.
- Smart symbol-only answer: 2 tokens.
- Smart explanation answer: 20 tokens.
- Emoji answer: 2 tokens.
- Ultra answer: 1 token.

Codex skills cannot guarantee automatic tracking in every runtime. When feasible, the skill records replies with `scripts/analphacodex_stats.py`; otherwise `analphacodex stats` should be treated as a local approximation.

Useful commands:

```powershell
python scripts/analphacodex_stats.py
python scripts/analphacodex_stats.py record --mode smart
python scripts/analphacodex_stats.py record --mode smart --explanation
python scripts/analphacodex_stats.py record --mode emoji --count 10
python scripts/analphacodex_stats.py path
python scripts/analphacodex_stats.py reset
```

## Benchmarking

For better measurement, use benchmark samples instead of the manual stats counter.

Run an exact tokenizer benchmark after installing `tiktoken` in the Python environment:

```powershell
python -m pip install tiktoken
python scripts/analphacodex_benchmark.py --input benchmarks/usage_samples.jsonl --details
python scripts/analphacodex_benchmark.py --input benchmarks/large_usage_samples.jsonl --details
```

Run a non-exact smoke test without dependencies:

```powershell
python scripts/analphacodex_benchmark.py --approx --details
```

The benchmark file is JSONL. Each row compares one normal Codex output with one analphacodex output:

```json
{"prompt":"is this okay?","mode":"smart","normal_output":"Yes, this looks safe enough to proceed.","analphacodex_output":"✅"}
```

For large tasks, add either `input_context_tokens` or `input_context_text`:

```json
{"prompt":"review huge diff","mode":"smart","input_context_tokens":85000,"normal_output":"Long normal answer...","analphacodex_output":"⛔\nRisky: destructive migration without rollback evidence."}
```

This supports an honest claim:

```text
For this sample set, analphacodex reduced output tokens by X%.
For this sample set, analphacodex reduced total run tokens by Y% when including provided context tokens.
```

It does not prove exact live savings unless real production outputs and a defensible baseline are captured.
